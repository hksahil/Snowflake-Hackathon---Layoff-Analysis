import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from annotated_text import annotated_text
import openai
openai.api_key=st.secrets['secret_key']

# Configure Page Title and Icon
st.set_page_config(page_title='Track my Job',page_icon='📊')

st.title('Layoffs :red[Tracker] 💼🚪 ')

# Navigation buttons    
col1, col2 = st.columns([.1,1])

with col1:
    back = st.button("⬅️",help='Previous Page')

if back:
     switch_page("Playground for Analysis")

annotated_text(
    "💡 Enter your Job to get the",
    (" trends ",'',"#faa"),
    (' and know the'),
    (" impact of AI",'',"#faa"),
    ('on your Industry')
)

user_input=st.text_input("")
clicked=st.button("Get data-backed analysis")

prompt_for_Layoff_Trends="Give  1 point backed by report and data which should tell the trends in " + user_input + "field in 2022,2023 of maximum 3 sentences" 
prompt_for_AI_Trends="Give  1 point backed by report and data which should tell will the job of " + user_input + "get affected by AI? of maximum 3 sentences"

if user_input and clicked:
    try:
        output1=openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt_for_Layoff_Trends,
        max_tokens=200,
        temperature=0
        )
        output2=openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt_for_AI_Trends,
        max_tokens=200,
        temperature=0
        )

        output_text1=output1['choices'][0]['text']
        output_text2=output2['choices'][0]['text']

        # ------ Backend Script Ends
        st.success(f"Trends in **{user_input}** field")
        st.write(output_text1)

        st.error(f"Impact of AI on **{user_input}** field")
        st.write(output_text2)
    except:
        st.error('Appologies, this service is unavailable at this moment !!')

