import streamlit as st
import random

# --- DATA: Common Ions for Edexcel IAL Chemistry ---
# Values are a list of acceptable answers.
# The first name in the list is the primary/preferred answer for feedback.
IONS = {
    # Positive Ions (Cations)
    "H^+": ["hydrogen"],
    "Na^+": ["sodium"],
    "K^+": ["potassium"],
    "Mg^{2+}": ["magnesium"],
    "Ca^{2+}": ["calcium"],
    "Al^{3+}": ["aluminium", "aluminum"],
    "Ag^+": ["silver"],
    "Zn^{2+}": ["zinc"],
    "NH_4^+": ["ammonium"],
    "Fe^{2+}": ["iron(II)"],
    "Fe^{3+}": ["iron(III)"],
    "Cu^+": ["copper(I)"],
    "Cu^{2+}": ["copper(II)"],
    "Pb^{2+}": ["lead(II)"],

    # Negative Ions (Anions)
    "Cl^-": ["chloride"],
    "Br^-": ["bromide"],
    "I^-": ["iodide"],
    "O^{2-}": ["oxide"],
    "S^{2-}": ["sulfide", "sulphide"],
    "OH^-": ["hydroxide"],
    "NO_3^-": ["nitrate"],
    "CO_3^{2-}": ["carbonate"],
    "SO_4^{2-}": ["sulfate", "sulphate"],
    "PO_4^{3-}": ["phosphate"],
    "HCO_3^-": ["hydrogencarbonate"],
    "HSO_4^-": ["hydrogensulfate", "hydrogensulphate"],
    "CrO_4^{2-}": ["chromate"],
    "Cr_2O_7^{2-}": ["dichromate"],
    # CHANGED: "permanganate" is now the primary name as requested.
    "MnO_4^-": ["permanganate", "manganate(VII)"],
}


def initialize_quiz():
    """Sets up or resets the quiz state in the session."""
    st.session_state.ions_list = list(IONS.keys())
    random.shuffle(st.session_state.ions_list)
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.total_answered = 0
    st.session_state.feedback = None

# --- STREAMLIT APP LAYOUT ---

st.set_page_config(page_title="Ion Naming Quiz", layout="centered")

st.title("🧪 Edexcel IAL Ion Naming Practice")
st.write("""
Test your knowledge of common ion names. Type your answer in the box and press Enter or click Submit.
Pay close attention to spelling and Roman numerals! Some common name variations are accepted.
""")

# --- INITIALIZATION & RESET ---

if 'ions_list' not in st.session_state:
    initialize_quiz()

if st.button("🔄 Start New Quiz"):
    initialize_quiz()
    st.rerun()

# --- QUIZ COMPLETION ---

if st.session_state.current_question_index >= len(st.session_state.ions_list):
    st.success(f"🎉 **Quiz Complete!** 🎉")
    st.balloons()
    final_score = st.session_state.score
    total_questions = len(st.session_state.ions_list)
    st.metric(label="Your Final Score", value=f"{final_score} / {total_questions}")
    percentage = (final_score / total_questions) * 100 if total_questions > 0 else 0
    st.write(f"You scored **{percentage:.1f}%**.")
    st.info("Click 'Start New Quiz' to try again with a new set of questions.")
    st.stop()

# --- MAIN QUIZ INTERFACE ---

col1, col2 = st.columns([3, 1])
with col1:
    progress_percent = st.session_state.total_answered / len(IONS)
    st.progress(progress_percent, text=f"Progress: {st.session_state.total_answered} / {len(IONS)}")
with col2:
    st.metric(label="Score", value=f"{st.session_state.score} / {st.session_state.total_answered}")

if st.session_state.feedback:
    st.info(st.session_state.feedback)
    st.session_state.feedback = None

# Get the current question's details
current_ion_formula = st.session_state.ions_list[st.session_state.current_question_index]
correct_answers_list = IONS[current_ion_formula]
primary_answer = correct_answers_list[0]

st.header("What is the name of this ion?")
# CHANGED: Use \mathrm{...} to display the formula in an upright font (no italics).
# The f-string with double braces {{...}} correctly formats the LaTeX string.
st.latex(f"\\mathrm{{{current_ion_formula}}}")


# --- ANSWER FORM ---
with st.form(key="answer_form", clear_on_submit=True):
    user_answer = st.text_input("Your Answer:", placeholder="e.g., sulfate", key="user_input")
    submitted = st.form_submit_button("Submit Answer")

    if submitted:
        normalized_user_answer = user_answer.strip().lower()
        normalized_correct_answers = [ans.lower() for ans in correct_answers_list]

        is_correct = normalized_user_answer in normalized_correct_answers

        st.session_state.total_answered += 1
        if is_correct:
            st.session_state.score += 1
            st.session_state.feedback = f"✅ Correct! Well done."
        else:
            # The backticks ` ` around the formula will display it correctly in the feedback.
            st.session_state.feedback = (
                f"❌ Not quite. The correct answer for `{current_ion_formula}` is **{primary_answer}**."
            )

        st.session_state.current_question_index += 1
        st.rerun()