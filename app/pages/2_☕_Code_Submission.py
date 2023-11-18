import json
from time import sleep
import openai
import streamlit as st
import requests
from streamlit_ace import st_ace
from code_editor import code_editor

def create_submission(session, source_code, languag, stdin):
    lookup = {'python': 71,
              'cpp': 76,
              'java': 27
            }
    url = "https://judge0-ce.p.rapidapi.com/submissions"

    querystring = {"base64_encoded":"false",
                   "wait":"false",
                   "fields":"*"
                   }

    payload = {
        "language_id": lookup[language],
        "source_code": source_code,
        "stdin": stdin
    }
    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "xxx",
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
    }
    response = session.post(url, json=payload, headers=headers, params=querystring)
    return response.json()

def get_submission(session, token):
    url = f"https://judge0-ce.p.rapidapi.com/submissions/{token}"

    querystring = {"base64_encoded":"false","fields":"*"}

    headers = {
        "X-RapidAPI-Key": "xxx",
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
    }
    print(url)
    response = session.get(url, headers=headers, params=querystring)
    print(response)
    return response.json()

with open('./resources/example_custom_buttons_bar_alt.json') as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

# Load Info bar CSS from JSON file
with open('./resources/example_info_bar.json') as json_info_file:
    info_bar = json.load(json_info_file)

# Load Code Editor CSS from file
with open('./resources/example_code_editor_css.scss') as css_file:
    css_text = css_file.read()

with open('./resources/example_python_code.py') as python_file:
    demo_sample_python_code = python_file.read()

with open('./resources/example_js_code.js') as python_file:
    demo_sample_js_code = python_file.read()
    
# construct component props dictionary (->Code Editor)
comp_props = {"css": css_text, "globalCSS": ":root {\n  --streamlit-dark-font-family: monospace;\n}"}

mode_list = ["c_cpp", "golang","java", "javascript", "php", "python", "ruby"]

language="python"
theme="default"
shortcuts="vscode"
focus=False
wrap=True
btns = custom_buttons_alt

with st.sidebar:
    st.markdown('<h1><a href="https://github.com/bouzidanas/streamlit.io/tree/master/streamlit-code-editor">HSBC DevEscape</a> Demo</h1>', unsafe_allow_html=True)
    st.write("")
    language = st.selectbox("lang:", mode_list, index=mode_list.index("python"))
    theme = st.selectbox("theme:", ["nord_dark", "chrome", "github"])
    shortcuts = st.selectbox("shortcuts:", ["emacs", "vim", "vscode", "sublime"], index=2)
        
session = requests.Session()
with st.form("my_form"):

    content = st_ace(value=demo_sample_python_code,
                     language=language,
                    theme=theme,
                    keybinding=shortcuts,
                    min_lines=12,
                    max_lines=None,
                    font_size=14
                )
    st.info("Expected Output")
    stdin = st_ace(language=language,
                    theme=theme,
                    keybinding=shortcuts,
                    min_lines=12,
                    max_lines=None,
                    font_size=14
                )
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write("Result")
        data = create_submission(session, content, language, stdin)
        st.text(data)
        st.text(f"the submission token is: {data['token']}")
        status_id = 0
        while not status_id:
            sleep(3)
            runtime = get_submission(session, data['token'])
            if runtime['stdin'] == runtime['stdout']:
                st.success("Submission Accepted")
            else:
                st.error("Something Wrong")
            st.json({
                'expected_output': runtime['stdin'],
                'output': runtime['stdout'],
                'status': runtime['status']['description'],
                'time': runtime['time'],
                'memory': runtime['memory'],
                
            })
            print(runtime)
            if runtime['status_id'] == 3:
                status_id=1