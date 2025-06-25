import streamlit as st
import random

# --- DATA: Common Ions for Edexcel IAL Chemistry ---
# The keys are LaTeX formatted for st.latex() display.
# The values are the expected string answers.
IONS = {
    # Positive Ions (Cations)
    "H^+": "hydrogen",
    "Na^+": "sodium",
    "K^+": "potassium",
    "Mg^{2+}": "magnesium",
    "Ca^{2+}": "calcium",
    "Al^{3+}": "aluminium",
    "Ag^+": "silver",
    "Zn^{2+}": "zinc",
    "NH_4^+": "ammonium",
    "Fe^{2+}": "iron(II)",
    "Fe^{3+}": "iron(III)",
    "Cu^+": "copper(I)",
    "Cu^{2+}": "copper(II)",
    "Pb^{2+}": "lead(II)",

    # Negative Ions (Anions)
    "Cl^-": "chloride",
    "Br^-": "bromide",
    "I^-": "iodide",
    "O^{2-}": "oxide",
    "S^{2-}": "sulfide",
    "OH^-": "hydroxide",
    "NO_3^-": "nitrate",
    "CO_3^{2-}": "carbonate",
    "SO_4^{2-}": "sulfate",
    "PO_4^{3-}": "phosphate",
    "HCO_3^-": "hydrogencarbonate",
    "HSO_4^-": "hydrogensulfate",
    "CrO_4^{2-}": "chromate",
    "Cr_2O_7^{2-}": "dichromate",
    "MnO_4^-": "manganate(VII)", # Also known as permanganate, but (VII) is more specific for A-level
}

# --- FUNCTIONS ---

def initialize_quiz():
    """Sets up or resets the quiz state in the session."""
    st.session_state.ions_list = list(IONS.keys())
    random.shuffle(st.session_state.ions_list)
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.total_answered = 0
    # 'feedback' will store the message from the last answer to show on the next run
    st.session_state.feedback = None

# --- STREAMLIT APP LAYOUT ---

st.set_page_config(page_title="Ion Naming Quiz", layout="centered")

st.title("🧪 IAL Ion Naming Practice")
st.write("""
Test your knowledge of common ion names. Type your answer in the box and press Enter or click Submit.
Pay close attention to **spelling** and **Roman numerals** for transition metals!
""")

# --- INITIALIZATION & RESET ---

# Initialize the quiz state if it's the first run
if 'ions_list' not in st.session_state:
    initialize_quiz()

# Provide a button to restart the quiz at any time
if st.button("🔄 Start New Quiz"):
    initialize_quiz()
    st.rerun()

# --- QUIZ COMPLETION ---

# Check if the quiz is over
if st.session_state.current_question_index >= len(st.session_state.ions_list):
    st.success(f"🎉 **Quiz Complete!** 🎉")
    st.balloons()
    final_score = st.session_state.score
    total_questions = len(st.session_state.ions_list)
    st.metric(label="Your Final Score", value=f"{final_score} / {total_questions}")
    percentage = (final_score / total_questions) * 100 if total_questions > 0 else 0
    st.write(f"You scored **{percentage:.1f}%**.")
    st.info("Click 'Start New Quiz' to try again with a new set of questions.")
    # Stop the script here to prevent the form from showing
    st.stop()

# --- MAIN QUIZ INTERFACE ---

# Display Score and Progress
col1, col2 = st.columns([3, 1])
with col1:
    progress_percent = st.session_state.total_answered / len(IONS)
    st.progress(progress_percent, text=f"Progress: {st.session_state.total_answered} / {len(IONS)}")
with col2:
    st.metric(label="Score", value=f"{st.session_state.score} / {st.session_state.total_answered}")


# Display feedback from the previous question (if any)
if st.session_state.feedback:
    st.info(st.session_state.feedback)
    st.session_state.feedback = None  # Clear feedback after showing it

# Get the current question's details
current_ion_formula = st.session_state.ions_list[st.session_state.current_question_index]
correct_answer = IONS[current_ion_formula]

# Display the question
st.header("What is the name of this ion?")
# Use a large font and proper LaTeX formatting for the ion
st.latex(current_ion_formula)

# --- ANSWER FORM ---
# Using a form ensures that the whole page doesn't rerun when the user types.
# It only reruns on submission. clear_on_submit=True clears the input box for the next question.
with st.form(key="answer_form", clear_on_submit=True):
    user_answer = st.text_input("Your Answer:", placeholder="e.g., sulfate", key="user_input")
    submitted = st.form_submit_button("Submit Answer")

    if submitted:
        # Normalize both answers for a fair comparison (lowercase and remove whitespace)
        is_correct = user_answer.strip().lower() == correct_answer.lower()

        # Update stats
        st.session_state.total_answered += 1
        if is_correct:
            st.session_state.score += 1
            # Set feedback message for the *next* screen
            st.session_state.feedback = f"✅ Correct! Well done."
        else:
            # Set feedback message for the *next* screen
            st.session_state.feedback = (
                f"❌ Not quite. The correct answer for `{current_ion_formula}` is **{correct_answer}**."
            )

        # Move to the next question
        st.session_state.current_question_index += 1

        # Rerun the script to show the next question and the feedback
        st.rerun()