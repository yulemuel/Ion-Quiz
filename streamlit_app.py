import streamlit as st
import random

# --- DATA: Common Ions with Categories ---
IONS = {
    # Cations
    "H^+":        {'names': ["hydrogen"], 'tags': ['cation']},
    "Na^+":       {'names': ["sodium"], 'tags': ['cation']},
    "K^+":        {'names': ["potassium"], 'tags': ['cation']},
    "Mg^{2+}":    {'names': ["magnesium"], 'tags': ['cation']},
    "Ca^{2+}":    {'names': ["calcium"], 'tags': ['cation']},
    "Al^{3+}":    {'names': ["aluminium", "aluminum"], 'tags': ['cation']},
    "Ag^+":       {'names': ["silver"], 'tags': ['cation']},
    "Zn^{2+}":    {'names': ["zinc"], 'tags': ['cation']},
    "Fe^{2+}":    {'names': ["iron(II)"], 'tags': ['cation']},
    "Fe^{3+}":    {'names': ["iron(III)"], 'tags': ['cation']},
    "Cu^+":       {'names': ["copper(I)"], 'tags': ['cation']},
    "Cu^{2+}":    {'names': ["copper(II)"], 'tags': ['cation']},
    "Pb^{2+}":    {'names': ["lead(II)"], 'tags': ['cation']},
    "NH_4{}^+":   {'names': ["ammonium"], 'tags': ['cation', 'compound']},
    # Anions
    "Cl^-":       {'names': ["chloride"], 'tags': ['anion']},
    "Br^-":       {'names': ["bromide"], 'tags': ['anion']},
    "I^-":        {'names': ["iodide"], 'tags': ['anion']},
    "O^{2-}":     {'names': ["oxide"], 'tags': ['anion']},
    "S^{2-}":     {'names': ["sulfide", "sulphide"], 'tags': ['anion']},
    "OH^-":       {'names': ["hydroxide"], 'tags': ['anion', 'compound']},
    "NO_3{}^-":   {'names': ["nitrate"], 'tags': ['anion', 'compound']},
    "CO_3{}^{2-}":{'names': ["carbonate"], 'tags': ['anion', 'compound']},
    "SO_4{}^{2-}":{'names': ["sulfate", "sulphate"], 'tags': ['anion', 'compound']},
    "PO_4{}^{3-}":{'names': ["phosphate"], 'tags': ['anion', 'compound']},
    "HCO_3{}^-":  {'names': ["hydrogencarbonate"], 'tags': ['anion', 'compound']},
    "HSO_4{}^-":  {'names': ["hydrogensulfate", "hydrogensulphate"], 'tags': ['anion', 'compound']},
    "CrO_4{}^{2-}":{'names': ["chromate"], 'tags': ['anion', 'compound']},
    "Cr_2O_7{}^{2-}":{'names': ["dichromate"], 'tags': ['anion', 'compound']},
    "MnO_4{}^-":  {'names': ["permanganate", "manganate(VII)"], 'tags': ['anion', 'compound']},
}

# --- FUNCTIONS ---

def prepare_question_list(mode, num_questions='All'):
    """Filters ions, sets the number of questions, and initializes quiz state."""
    if mode == 'All Ions':
        potential_questions = list(IONS.keys())
    else:
        MODE_TO_TAG_MAP = {
            'Cations': 'cation',
            'Anions': 'anion',
            'Compound Ions': 'compound'
        }
        tag_to_filter = MODE_TO_TAG_MAP[mode]
        potential_questions = [ion for ion, data in IONS.items() if tag_to_filter in data['tags']]
    
    random.shuffle(potential_questions)
    
    if num_questions != 'All' and isinstance(num_questions, int):
        st.session_state.ions_list = potential_questions[:num_questions]
    else:
        st.session_state.ions_list = potential_questions
    
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.answer_history = []
    st.session_state.feedback = None

def select_mode(mode):
    """Handles the logic for when a user selects a quiz mode."""
    st.session_state.quiz_mode = mode
    if mode == 'All Ions':
        st.session_state.app_state = 'select_count'
    else:
        prepare_question_list(mode)
        st.session_state.app_state = 'quiz_active'

def start_quiz_with_count(num_questions):
    """Starts the 'All Ions' quiz with a selected number of questions."""
    prepare_question_list('All Ions', num_questions)
    st.session_state.app_state = 'quiz_active'

def reset_app():
    """Resets the entire app to the initial mode selection screen."""
    st.session_state.app_state = 'initial'
    keys_to_clear = ['quiz_mode', 'ions_list', 'current_question_index', 'score', 'answer_history', 'feedback']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# --- INITIALIZE STATE ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = 'initial'

# --- APP LAYOUT ---
# CHANGED: Added initial_sidebar_state="expanded" to make the sidebar open by default.
st.set_page_config(
    page_title="Ion Naming Quiz",
    layout="centered",
    initial_sidebar_state="expanded" 
)

st.title("🧪 Chemistry Ion Naming Practice")

# --- STATE 1: INITIAL MODE SELECTION ---
if st.session_state.app_state == 'initial':
    st.subheader("Choose a category to practice:")
    cols = st.columns(4)
    cols[0].button("Cations", on_click=select_mode, args=('Cations',), use_container_width=True)
    cols[1].button("Anions", on_click=select_mode, args=('Anions',), use_container_width=True)
    cols[2].button("Compound Ions", on_click=select_mode, args=('Compound Ions',), use_container_width=True)
    cols[3].button("All Ions", on_click=select_mode, args=('All Ions',), use_container_width=True)
    st.info("ℹ️ You might want to study the formulas and names of the ions before you start the quiz.")

# --- STATE 2: QUESTION COUNT SELECTION (For 'All Ions' mode only) ---
elif st.session_state.app_state == 'select_count':
    st.subheader("Mode: All Ions")
    st.write("How many questions would you like?")
    
    available_count = len(IONS)
    cols = st.columns(4)
    cols[0].button("5 Questions", on_click=start_quiz_with_count, args=(5,), use_container_width=True)
    cols[1].button("10 Questions", on_click=start_quiz_with_count, args=(10,), use_container_width=True)
    cols[2].button(f"All ({available_count})", on_click=start_quiz_with_count, args=('All',), use_container_width=True)
    cols[3].button("⬅️ Back", on_click=reset_app, use_container_width=True)

# --- STATE 3: QUIZ ACTIVE OR COMPLETE ---
elif st.session_state.app_state == 'quiz_active':
    with st.sidebar:
        st.header("📊 Your Progress") # Added an emoji to the header
        st.caption(f"Mode: {st.session_state.get('quiz_mode', 'N/A')}")
        st.write("---")
        if not st.session_state.get('answer_history', []):
            st.write("Your answers will appear here.")
        else:
            for item in st.session_state.answer_history:
                formula_latex = f"$\\mathrm{{{item['formula']}}}$"
                if item['is_correct']:
                    st.markdown(f"✅ {formula_latex}: You wrote *{item['user_answer']}*")
                else:
                    st.markdown(
                        f"❌ {formula_latex}: You wrote *{item['user_answer']}*. "
                        f"Correct: **{item['correct_answer']}**"
                    )
        st.write("---")
        st.button("End Quiz & Start Over", on_click=reset_app, use_container_width=True)

    if st.session_state.current_question_index >= len(st.session_state.ions_list):
        st.success(f"🎉 **Quiz Complete!** 🎉")
        st.balloons()
        final_score = st.session_state.score
        total_questions = len(st.session_state.ions_list)
        st.metric(label="Your Final Score", value=f"{final_score} / {total_questions}")
        st.info("See your full progress in the sidebar. Click 'End Quiz & Start Over' to play again.")
    else:
        total_questions_in_mode = len(st.session_state.ions_list)
        progress_text = f"Question {st.session_state.current_question_index + 1} of {total_questions_in_mode}"
        st.progress((st.session_state.current_question_index) / total_questions_in_mode, text=progress_text)

        if st.session_state.feedback:
            st.info(st.session_state.feedback)
            st.session_state.feedback = None

        current_ion_formula = st.session_state.ions_list[st.session_state.current_question_index]
        ion_data = IONS[current_ion_formula]
        primary_answer = ion_data['names'][0]

        st.header("What is the name of this ion?")
        st.latex(f"\\Huge \\mathrm{{{current_ion_formula}}}")

        with st.form(key="answer_form", clear_on_submit=True):
            user_answer = st.text_input("Your Answer:", placeholder="e.g., sulfate", key="user_input")
            submitted = st.form_submit_button("Submit Answer")

            if submitted and user_answer:
                normalized_user_answer = user_answer.strip().lower()
                normalized_correct_answers = [ans.lower() for ans in ion_data['names']]
                is_correct = normalized_user_answer in normalized_correct_answers
                
                st.session_state.feedback = "✅ Correct! Well done." if is_correct else f"❌ Not quite. The answer is **{primary_answer}**."
                if is_correct: st.session_state.score += 1
                
                history_item = {
                    'formula': current_ion_formula,
                    'user_answer': user_answer.strip(),
                    'is_correct': is_correct,
                    'correct_answer': primary_answer
                }
                st.session_state.answer_history.append(history_item)
                
                st.session_state.current_question_index += 1
                st.rerun()