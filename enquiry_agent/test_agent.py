"""Offline tests: no API key or mail server needed. Run: python -m unittest test_agent.py"""

import unittest
from pathlib import Path

import agent

SAMPLES = Path(__file__).parent / "samples"


def decision(**kw):
    base = dict(
        category="programme_information", route="auto_reply", confidence=0.95, urgency="low",
        customer_name="Mei Ling", organisation="", summary="Asks about duration.",
        reason="Fully answered by KB.", unanswered_questions=[], reply_subject="Re: Course",
        reply_body="Dear Mei Ling, ...", suggested_reply_for_owner="",
    )
    base.update(kw)
    return agent.Decision(**base)


class FakeClassifier:
    def __init__(self, d):
        self.d = d
        self.calls = 0

    def classify(self, msg):
        self.calls += 1
        return self.d.model_copy()


class FakeMailer:
    def __init__(self):
        self.sent = []

    def send(self, m):
        self.sent.append(m)


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.cfg = agent.Config()
        self.cfg.agent_email = "enquiry@yourdomain.com"
        self.cfg.escalation_email = "zainal@evocoleadership.com"
        self.state = agent.State(Path("__no_state__"))
        self.mailer = FakeMailer()
        self.info = agent.parse_email((SAMPLES / "info_request.eml").read_bytes())

    def run_with(self, d, msg=None):
        return agent.handle(msg or self.info, self.cfg, FakeClassifier(d), self.mailer, self.state)

    def test_info_request_gets_auto_reply_only(self):
        rec = self.run_with(decision())
        self.assertEqual(rec["action"], "auto_reply")
        self.assertEqual(len(self.mailer.sent), 1)
        reply = self.mailer.sent[0]
        self.assertIn("meiling.tan@example.com", reply["To"])
        self.assertEqual(reply["In-Reply-To"], "<sample-info-001@example.com>")
        self.assertEqual(reply["Auto-Submitted"], "auto-replied")

    def test_escalation_forwards_to_owner_and_acks_customer(self):
        rec = self.run_with(decision(route="escalate", category="quotation_or_proposal_request",
                                     reply_body="Thank you, our team will be in touch.",
                                     suggested_reply_for_owner="Draft..."))
        self.assertEqual(rec["action"], "escalate")
        to = [m["To"] for m in self.mailer.sent]
        self.assertTrue(any("meiling.tan@example.com" in t for t in to))
        fwd = [m for m in self.mailer.sent if m["To"] == "zainal@evocoleadership.com"][0]
        self.assertIn("[ACTION NEEDED]", fwd["Subject"])
        self.assertIn("meiling.tan@example.com", fwd["Reply-To"])
        self.assertTrue(any(p.get_content_type() == "message/rfc822" for p in fwd.iter_attachments()))

    def test_low_confidence_is_escalated(self):
        rec = self.run_with(decision(confidence=0.5))
        self.assertEqual(rec["action"], "escalate")

    def test_unanswered_questions_are_escalated(self):
        rec = self.run_with(decision(unanswered_questions=["Is SkillsFuture claimable?"]))
        self.assertEqual(rec["action"], "escalate")

    def test_daily_auto_reply_limit(self):
        actions = [self.run_with(decision())["action"] for _ in range(3)]
        self.assertEqual(actions, ["auto_reply", "auto_reply", "escalate"])

    def test_out_of_office_is_skipped_without_calling_model(self):
        msg = agent.parse_email((SAMPLES / "out_of_office.eml").read_bytes())
        clf = FakeClassifier(decision())
        rec = agent.handle(msg, self.cfg, clf, self.mailer, self.state)
        self.assertEqual(rec["action"], "skipped")
        self.assertEqual(clf.calls, 0)
        self.assertEqual(self.mailer.sent, [])

    def test_own_address_is_skipped(self):
        raw = b"From: zainal@evocoleadership.com\r\nSubject: hi\r\n\r\nbody"
        rec = agent.handle(agent.parse_email(raw), self.cfg, FakeClassifier(decision()), self.mailer, self.state)
        self.assertEqual(rec["action"], "skipped")

    def test_ignore_sends_nothing(self):
        rec = self.run_with(decision(route="ignore", category="spam_or_marketing", reply_body=""))
        self.assertEqual(rec["action"], "ignore")
        self.assertEqual(self.mailer.sent, [])

    def test_api_failure_escalates_without_customer_ack(self):
        class Broken:
            def classify(self, msg):
                raise agent.anthropic.APIConnectionError(request=None)
        rec = agent.handle(self.info, self.cfg, Broken(), self.mailer, self.state)
        self.assertEqual(rec["action"], "escalate")
        self.assertEqual([m["To"] for m in self.mailer.sent], ["zainal@evocoleadership.com"])

    def test_html_body_is_converted_to_text(self):
        raw = (b"From: A <a@example.com>\r\nSubject: x\r\nContent-Type: text/html\r\n\r\n"
               b"<p>Hello<br>World</p><script>evil()</script>")
        body = agent.parse_email(raw).body
        self.assertIn("Hello", body)
        self.assertNotIn("evil", body)


if __name__ == "__main__":
    unittest.main()
