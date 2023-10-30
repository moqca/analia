import streamlit as st
from decouple import config
from botfunctions import functionDefinitions
from coderun import runCode
from agents import qagent
import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import re

response = False
prompt_tokens = 0
completion_tokes = 0
total_tokens_used = 0
cost_of_response = 0

API_KEY = config('OPENAI_API_KEY')
openai.api_key = API_KEY


def make_request(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7777777,
        top_p=0.5,
        functions=functionDefinitions,
    )
    return response


st.header("Do Analysts dream of electric snow?")

st.markdown("""---""")

question_input = st.text_input("Enter question")
rerun_button = st.button("Ask")
clear_messages = st.button("Reset history")

#we create the messages array to keep track of communication
#we read the systemprompt file

sysprompt = open('src/systemprompt.txt', 'r').read()

messages = [{"role": "system", "content": sysprompt},]

st.markdown("""---""")

if question_input:
    messages.append({'role': 'user', 'content':question_input})
    print(messages)
    response = make_request(messages)
else:
    pass

if rerun_button:
    messages = [{"role": "system", "content": sysprompt},]
else:
    pass


if clear_messages:
    messages = ''

if response:
    print(response)

    finish_reason = response["choices"][0]["finish_reason"]
    message = response["choices"][0]["message"]
    # st.markdown(finish_reason)

    if finish_reason == "function_call":
        func_name = message["function_call"]["name"]
        func_to_call  = 'Nothing here yet'
        funcargs = message["function_call"]["arguments"]
        if type(funcargs) == str:
            pass
        if type(funcargs) == dict:
            funcargs = funcargs["code"]
        r = qagent(funcargs)
        clean = r["choices"][0]["message"]["content"]

        code_match = re.search(r'```python(.*?)```', clean, re.DOTALL)

        if code_match:
            codevars = runCode(code_match.group(1))
        else:
            codevars = runCode(clean)

        df = codevars['df']
        fig = codevars['fig']
        plt = codevars['plt']
        with st.expander("Data Table:"):
            if isinstance(df, pd.DataFrame):
                st.markdown(df.to_markdown())

        if isinstance(plt, plt.Figure):
            st.pyplot(plt)
        if fig is not None:
            st.pyplot(fig)

    else:
        st.write("Response:")
        st.write(response["choices"][0]["message"]["content"])

    prompt_tokens = response["usage"]["prompt_tokens"]
    completion_tokes = response["usage"]["completion_tokens"]
    total_tokens_used = response["usage"]["total_tokens"]

    cost_of_response = total_tokens_used * 0.000002
else:
    pass


