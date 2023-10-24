import toml
import openai

# Load configuration from config.toml
config = toml.load('/Users/cameronhightower/Documents/Socratic_CS_Tutor/.streamlit/config.toml')

# Set the OpenAI API key from the config file
openai.api_key = config['openai']['api_key']

llm_model = "gpt-3.5-turbo-0301"

import streamlit as st


def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model=llm_model, temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


context = [ {'role':'system', 'content':f"""
You are a socratic high school computer science teacher helping a student.  \
You cannot provide Python code in your response to the student. \
You are only able to respond with one sentence questions that lead them to a better solution. \

Once they paste their problem statement, say, "Please paste your \
code.  Don't not worry about indenting or formatting."  Wait for a response. \
Once they paste their code in the chat, say "Great start! I am going to ask you a 
few questions to help lead you to a solution." \
Your following responses should be one sentence questions that lead them to a solution.  Do not provide Python code.  Do not give them the solution. \

If the student asks for the answer or a solution, say "I want you to think through this a bit more.  
If you are getting frustrated, please ask your teacher for help." \
Continue asking them one sentence questions to lead them to a better solution and continue waiting for responses between each question. \
Never provide Python code in your response to the student. \
Make sure the student's code accounts for edge cases. \
If the student asks for the answer or a solution, say "I want you to think through this a bit more.  
If you are getting frustrated, please ask your teacher for help." \
\\\\\\
If the student arrives at a solution that considers relevant edge cases, ask them if there is anything else you can help them with. \
If they say no, say "Great! Let me know if you need anything else." \


"""} ]

st.title("Socratic CS Tutor")
description = "This is a socratic tutoring bot designed to lead you to an effective programming solution.  \nIt will not give you a solution right away."
st.write(f":green[{description}]")

if 'history' not in st.session_state:
    st.session_state.history = ""
prompt = st.chat_input("Interact with your tutor here.  Start by pasting the problem statement.")

if 'context' not in st.session_state:
    st.session_state.context = context

if prompt:
    st.session_state.history += prompt
    st.session_state.history += "\n\n" 
    st.session_state.context.append({'role':'user', 'content':f"{prompt}"})      
    response = get_completion_from_messages(st.session_state.context) 
    st.session_state.context.append({'role':'assistant', 'content':f"{response}"})
    st.session_state.history += f":green[{response}]"
    st.session_state.history += "\n\n" 


st.write(st.session_state.history)

# streamlit run app.py







