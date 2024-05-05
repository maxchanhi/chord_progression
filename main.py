import streamlit as st
from notation import fun_emoji_list
import random
from question import lilypond_generation,question_generation,display_options,chord_accompany,audio_generation
from progression import main_generation,key_generation
from streamlit_extras.let_it_rain import rain
ss=st.session_state
def new_question(choosen_range="Major"):
    choosen_key=key_generation(choosen_range)
    ss["question_data"] = main_generation(choosen_key)
    score_melody = ss["question_data"]["melody"]
    correct_option = ss["question_data"]["chord"]
    key_signature = ss["question_data"]["key"]
    accom_part=chord_accompany(key_signature,correct_option)
    lilypond_generation(score_melody, "question",key_signature,accom_part)
    correct_index,options=question_generation(correct_option)
    options= display_options(options)
    ss["button_pressed"]=False
    return correct_index,options,key_signature
def button_pressed():
    ss["button_pressed"]=True
    return ss["button_pressed"]
st.set_page_config(page_title="Harmonise melody")

st.title("Identify the Correct Harmonic Pattern")
choosen_range = st.multiselect("Select the keys:",["Major","minor"],default=["Major"])

if choosen_range is None:
    st.warning("Please select a key.")
new_score = st.button("Generate Score")

if new_score and choosen_range:
    ss["question_data"]=new_question(choosen_range)
if "question_data" not in ss:
    print(choosen_range)
    ss["question_data"]=new_question(choosen_range)

correct_index,options,key_signature=ss["question_data"]
print(ss["question_data"])
st.image("static/cropped_score_question.png", use_column_width=True)
user_ans = st.radio(f"Select the correct harmonic pattern in {key_signature}:",options)

if st.button("Submit",on_click=button_pressed,disabled=ss["button_pressed"]):
    if options.index(user_ans) == correct_index:
        emoji= random.choice(fun_emoji_list)
        st.success(f"Correct!{emoji}")
        rain(emoji=emoji,animation_length=1)
        st.balloons()
        audio_generation()
        st.audio("static/question.mp3")
    else:
        st.warning(f"Incorrect! The answer is {options[correct_index]}")





