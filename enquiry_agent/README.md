# Customer Enquiry Agent

An email agent for a training consultancy. It reads each new enquiry, sends an
automatic answer when the enquiry only seeks information that you have approved,
and forwards everything else to **zainal@evocoleadership.com** with a summary
and a suggested reply.

## How enquiries are routed

| Route | When | What happens |
|---|---|---|
| Auto-reply | Sender only wants information, and every question is answered by `knowledge_base.md` | Customer receives the answer |
| Escalate | Quotes, bookings, in-house or customised training, funding for a specific case, complaints, payments, partnerships, anything not in the knowledge base, or low confidence | You receive a forward with summary, reason, unanswered questions, a draft reply and the original email. The customer receives a short acknowledgement. |
| Ignore | Spam, cold sales pitches, newsletters | Nothing is sent |
| Skipped | Out-of-office, mailing lists, no-reply senders, your own addresses | Nothing is sent and Claude is not called |

Safety rules enforced in code, regardless of what the model says:

- An auto-reply below the confidence threshold is escalated instead.
- An auto-reply that leaves any question unanswered is escalated instead.
- Each sender gets at most two auto-replies per 24 hours. Further mail is escalated.
- If the Claude API fails or declines, the email is escalated with no customer acknowledgement.
- Outgoing replies carry the `Auto-Submitted` header so other systems do not reply back in a loop.
- `DRY_RUN=true` is the default. Nothing is sent and nothing is marked as read until you turn it off.

On an escalation email, pressing **Reply** goes straight to the customer.

## Setup

1. **Use a dedicated inbox** such as `enquiry@yourdomain.com`. Do not point the agent at your personal mailbox.
2. **Install** Python 3.10 or later, then:
   ```bash
   cd enquiry_agent
   pip install -r requirements.txt
   cp .env.example .env
   ```
3. **Fill in `.env`.** You need a Claude API key from console.anthropic.com, plus IMAP and SMTP details for the enquiry inbox.
   Many providers, including Google Workspace and Microsoft 365, restrict password sign-in for IMAP and SMTP. Check what your provider currently allows. You may need an app password, or an admin may need to enable IMAP and SMTP for that mailbox.
4. **Fill in `knowledge_base.md`.** This is the most important step. Replace every `[EDIT: ...]` line with approved facts. The agent cannot answer anything that is not in this file. Topics you leave blank are escalated to you.

## Test before going live

```bash
python -m unittest test_agent.py              # offline checks, no API key needed
python agent.py --test samples/info_request.eml
python agent.py --test samples/quote_request.eml
python agent.py --test samples/out_of_office.eml
```

`--test` prints the decision and the drafted reply without sending anything.
Save a few real past enquiries as `.eml` files and test them the same way.

Then run against the live inbox in dry-run mode:

```bash
python agent.py --once
```

Read `decisions.jsonl` to check every routing decision.

## Go live

1. Set `DRY_RUN=false` in `.env`.
2. Run continuously with `python agent.py --loop`, which polls every two minutes by default. Alternatively, schedule `python agent.py --once` with cron or Windows Task Scheduler.
3. Review `decisions.jsonl` daily for the first two weeks. Tighten the knowledge base wherever replies are weak, and raise `CONFIDENCE_THRESHOLD` if anything was auto-answered that should not have been.

## Settings

| Setting | Default | Purpose |
|---|---|---|
| `ESCALATION_EMAIL` | zainal@evocoleadership.com | Where enquiries needing action are sent |
| `DRY_RUN` | true | Log only. Sends nothing and leaves mail unread. |
| `CONFIDENCE_THRESHOLD` | 0.8 | Minimum confidence for an auto-reply |
| `MAX_AUTO_REPLIES_PER_SENDER_PER_DAY` | 2 | Protects against reply loops and repeated questions |
| `ACK_ON_ESCALATION` | true | Send the customer an acknowledgement when escalating |
| `CLAUDE_MODEL` | claude-opus-5-5 | Model used to classify and draft |
| `CLAUDE_EFFORT` | medium | Reasoning effort. `low` is cheaper and usually fine for simple enquiries. |

## Responsible use

- **You stay accountable for every reply.** The agent only states facts from your knowledge base. Keep that file accurate and current, especially fees, dates and funding.
- **Funding and subsidy questions** for a specific person or company are always escalated, because eligibility depends on details the agent cannot verify.
- **Personal data.** Enquiry emails are sent to the Claude API for processing. Check that this fits your privacy notice and your obligations under Singapore's Personal Data Protection Act (PDPA). The state file stores only hashed sender addresses. `decisions.jsonl` stores subjects and routing reasons, so treat it as confidential.
- **Prompt injection.** Email text is treated as untrusted data. An email that tries to instruct the agent is escalated to you.
