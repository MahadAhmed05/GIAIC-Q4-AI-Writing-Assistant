import streamlit as st
import requests

api_key = st.secrets["openrouter_api_key"]


def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

st.title("AI Writing Assistant")

text = st.text_area("Enter your text here:", height=200)

tone = st.selectbox("Select Tone/Style", ["Formal", "Casual", "Professional", "Friendly"])

task = st.selectbox("Choose Task", ["Improve Text", "Summarize", "Rephrase"])

if st.button("Run AI"):
    if text.strip() == "":
        st.warning("Please enter some text first!")
    else:
        prompt_map = {
            "Improve Text": f"Please improve the following text with a {tone.lower()} tone:\n\n{text}",
            "Summarize": f"Please summarize the following text in a {tone.lower()} tone:\n\n{text}",
            "Rephrase": f"Please rephrase the following text in a {tone.lower()} tone:\n\n{text}",
        }
        prompt = prompt_map[task]
        with st.spinner("Getting AI response..."):
            result = get_ai_response(prompt)
        st.subheader("AI Response:")
        st.write(result)
        
        # Optional: download button for the result text
        st.download_button("Download Response as Text", result, file_name="ai_response.txt")
