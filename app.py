import streamlit as st

# --- CONFIGURATION & STATE MANAGEMENT ---
st.set_page_config(page_title="GenAI Prompting Academy", page_icon="🤖", layout="centered")

# Question Bank Database
QUESTION_BANK = {
    "Beginner": [
        {
            "scenario": "**Scenario 1 (New Professionals):** You need to draft a professional email updating your boss on a project delay. A poor prompt is: *'Write an email about a project delay.'*",
            "question": "Which addition provides the essential context GenAI needs to write a tailored draft?",
            "options": [
                "A) 'Write it quickly and make it formal.'",
                "B) 'Write a polite email to my manager explaining that the Q3 marketing campaign is delayed by 2 days due to an approval bottleneck, and outline our recovery steps.'",
                "C) 'Help me fix a project delay text.'"
            ],
            "correct": "B",
            "explanation": "GenAI tools thrive on specifics. Providing the project name (Q3 marketing), the exact duration (2 days), the specific cause (approval bottleneck), and the requested resolution helps it generate a perfect first draft."
        },
        {
            "scenario": "**Scenario 2 (Mid-Career Professionals):** You want to summarize a dense market analysis report to capture just the industry trends.",
            "question": "Which prompt moves beyond a basic 'summarize this' command to get a targeted output?",
            "options": [
                "A) 'Summarize this market report for me.'",
                "B) 'Give me a summary but focus only on the emerging technology trends and consumer behavior shifts mentioned in this text.'",
                "C) 'Make this shorter.'"
            ],
            "correct": "B",
            "explanation": "By explicitly declaring the lenses you care about (tech trends, consumer behavior), you filter out irrelevant data from the summary."
        },
        {
            "scenario": "**Scenario 3 (Retirees & Lifelong Learners):** You want to plan a 4-day leisure trip to Tokyo but have walking difficulties.",
            "question": "How should you structure a simple prompt to ensure the itinerary matches your physical pacing?",
            "options": [
                "A) 'Plan a Tokyo trip for 4 days.'",
                "B) 'What are things to do in Tokyo?'",
                "C) 'Create a relaxed 4-day Tokyo travel itinerary. Keep walking minimal, focus on cultural sites accessible by taxi, and include a rest break every afternoon.'"
            ],
            "correct": "C",
            "explanation": "Specifying physical constraints (minimal walking, taxi-accessible) and pace parameters (afternoon rest) keeps the AI from suggesting exhausting itineraries."
        }
    ],
    "Intermediate": [
        {
            "scenario": "**Scenario 1 (Mid-Career):** You need to prepare tough interview questions to screen candidates for a senior project manager role.",
            "question": "Which prompt uses the 'Persona' technique most effectively?",
            "options": [
                "A) 'Act as a veteran Chief Human Resources Officer with 20 years of experience. Generate 5 behavioral interview questions to test an applicant's agility under pressure.'",
                "B) 'Give me some good interview questions for a manager.'",
                "C) 'Pretend you are hiring someone and give me questions.'"
            ],
            "correct": "A",
            "explanation": "Assigning a specific high-level persona (Chief HR Officer) forces the AI to tap into advanced frameworks, giving you much deeper, psychometric questions."
        },
        {
            "scenario": "**Scenario 2 (Retirees / Personal Finance):** You want to understand a complex corporate investment prospectus or estate planning concept.",
            "question": "Which prompt instructs the AI to match your exact level of technical knowledge?",
            "options": [
                "A) 'Explain this financial document.'",
                "B) 'Act as a patient financial educator. Explain this investment prospectus clause to me like a beginner, using an everyday analogy instead of heavy jargon.'",
                "C) 'What does this investment document mean?'"
            ],
            "correct": "B",
            "explanation": "Combining a supportive persona ('patient educator') with a stylistic constraint ('everyday analogy, no jargon') makes complex data immediately digestible."
        },
        {
            "scenario": "**Scenario 3 (New Professionals):** You are drafting a pitch for a creative project but your writing feels flat and overly academic.",
            "question": "How do you direct the tone shift efficiently?",
            "options": [
                "A) 'Make my writing sound better.'",
                "B) 'Rewrite this text. Adopt the persona of an innovative startup founder pitching to venture capitalists. Use an energetic, persuasive, and visionary tone.'",
                "C) 'Change this draft to be exciting.'"
            ],
            "correct": "B",
            "explanation": "Clearly identifying the target audience (venture capitalists) and explicit tone descriptors (energetic, persuasive, visionary) yields dynamic copy."
        }
    ],
    "Advanced": [
        {
            "scenario": "**Scenario 1 (All Professionals):** You have a messy list of raw customer feedback data and need a clean analysis for an executive slide deck.",
            "question": "Which prompt enforces absolute formatting control and constraints?",
            "options": [
                "A) 'Analyze this feedback and put it in a nice format.'",
                "B) 'Summarize what customers are saying here.'",
                "C) 'Analyze the attached customer feedback text. Output your response strictly as a markdown table with three columns: [Theme, Frequency (High/Med/Low), Actionable Recommendation]. Exclude any introductory text.'"
            ],
            "correct": "C",
            "explanation": "Advanced prompting relies heavily on output constraints. Naming the exact column headers and banning pleasantries ('Exclude introductory text') makes the data ready for direct copy-pasting into your reports."
        },
        {
            "scenario": "**Scenario 2 (Corporate Navigation):** You are dealing with a complex cross-departmental conflict and want to run a multi-perspective strategy session with an AI.",
            "question": "Which prompt sets up an advanced interactive workflow?",
            "options": [
                "A) 'How do I resolve a conflict between engineering and sales?'",
                "B) 'I want you to roleplay as three distinct stakeholders: an empathetic HR Director, a data-driven CTO, and a protective Head of Sales. I will give you a workplace conflict scenario. Provide a combined response showing how each character views the issue, then offer a compromised roadmap.'",
                "C) 'Tell me what HR and Sales think about disputes.'"
            ],
            "correct": "B",
            "explanation": "Multi-persona prompting unlocks simulation-grade outputs. It forces the LLM to process structural tensions from diverse angles simultaneously."
        },
        {
            "scenario": "**Scenario 3 (Data / Tech Tools):** You want the AI to write a script or automate a task, but you need to eliminate its tendency to give incomplete snippets or explanations.",
            "question": "Which prompt sets up an optimal, bulletproof constraint framework?",
            "options": [
                "A) 'Write a script to clean Excel data.'",
                "B) 'Generate a Python script to merge two Excel sheets based on an ID column. Constraints: Use only the pandas library, comment every line of code to explain the logic, and do not write any conversational text before or after the code block.'",
                "C) 'Give me code for Excel automation and explain it.'"
            ],
            "correct": "B",
            "explanation": "By explicitly naming libraries, demanding inline documentation, and omitting conversational prose, you optimize the system's raw processing performance."
        }
    ]
}

# Initialize session state tracking
if "level" not in st.session_state:
    st.session_state.level = "Beginner"
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False

# --- HEADER UI ---
st.title("🤖 Enterprise Prompting Academy")
st.subheader("Interactive Upskilling Framework for Modern Professionals")
st.write("Advance through systematic micro-scenarios mapping user context, persona modeling, and architectural constraints.")
st.markdown("---")

# Progress Calculations
levels_list = ["Beginner", "Intermediate", "Advanced", "Complete"]
current_level = st.session_state.level

if current_level != "Complete":
    q_bank_level = QUESTION_BANK[current_level]
    total_questions_in_level = len(q_bank_level)
    current_q = q_bank_level[st.session_state.q_index]
    
    # Calculate overall progress bar metrics
    total_scenarios = 9
    completed_scenarios = (levels_list.index(current_level) * 3) + st.session_state.q_index
    st.progress(completed_scenarios / total_scenarios)
    
    st.markdown(f"**Current Tier:** `{current_level}` | **Scenario:** `{st.session_state.q_index + 1}/{total_questions_in_level}` | **Total Global Score:** `{st.session_state.score}/{total_scenarios}`")
    st.markdown("---")
    
    # --- DISPLAY SCENARIO & QUESTION ---
    st.markdown(current_q["scenario"])
    st.markdown(f"❓ **{current_q['question']}**")
    
    # Dynamic radio selection
    choice = st.radio("Select your prompting approach:", current_q["options"], index=None, key=f"radio_{current_level}_{st.session_state.q_index}")
    
    # Action buttons container
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("Submit Answer", disabled=st.session_state.answered):
            if choice:
                st.session_state.answered = True
                selected_letter = choice[0]
                if selected_letter == current_q["correct"]:
                    st.session_state.score += 1
                    st.session_state.is_correct = True
                else:
                    st.session_state.is_correct = False
                st.rerun()
            else:
                st.warning("Please select an option first.")
                
    with col2:
        if st.session_state.answered:
            if st.button("Proceed to Next Scenario"):
                # Move to next question or tier
                st.session_state.answered = False
                if st.session_state.q_index + 1 < total_questions_in_level:
                    st.session_state.q_index += 1
                else:
                    # Move to next major tier
                    next_idx = levels_list.index(current_level) + 1
                    st.session_state.level = levels_list[next_idx]
                    st.session_state.q_index = 0
                st.rerun()

    # --- SHOW CONDITIONAL FEEDBACK ---
    if st.session_state.answered:
        if st.session_state.is_correct:
            st.success(f"🎉 **Correct!**\n\n{current_q['explanation']}")
        else:
            st.error(f"❌ **Incorrect Approach.**\n\n{current_q['explanation']}")

# --- GRADUATION / COMPLETION SCREEN ---
else:
    st.balloons()
    st.header("🎓 Academy Curriculum Completed!")
    st.write(f"Fantastic job! You achieved a final score of **{st.session_state.score}/9**.")
    st.markdown("""
    ### Key Takeaways for your Workflow:
    1. **Context Initialization (Beginner):** Never type single-word concepts. Anchor the model with explicit goals, reasons, and target audiences.
    2. **Structural Personas (Intermediate):** Tell the system exactly who it represents (*'Act as an expert...'*). This triggers granular contextual behavior patterns.
    3. **Architectural Constraints (Advanced):** Explicitly demand output structural constraints (tables, counts, json format) and strip out conversational filler words.
    """)
    
    if st.button("Restart Complete Academy Course"):
        st.session_state.level = "Beginner"
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.is_correct = False
        st.rerun()