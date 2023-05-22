import openai 
import streamlit as st
#import config


def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("メッセージ履歴", value=str("\n".join(messages_str)), height=400)


st.header("GPT私設秘書")

##If used privately : openai.api_key = config.api_key

#If used with streamlitcloud
openai.api_key = st.secrets["chatGPT"]["OPENAI_KEY"]
BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT


text = st.empty()
show_messages(text)

col3_1, col3_2 = st.columns([5,1]);
with col3_1:
    st.caption("GPT3.5があなたの質問に答えます。履歴を消したい場合は消去を押して下さい")
with col3_2:
    if st.button("消去"):
        st.session_state["messages"] = BASE_PROMPT
        show_messages(text)



col1, col2 = st.columns([5, 1])
with col1:
    prompt = st.text_input("入力欄 👇", value="",placeholder="ここに質問を記入してください")

with col2:
    st.caption("送信して質問")
    if st.button("送信"):
        with st.spinner("メッセージを生成中..."):
            st.session_state["messages"] += [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=st.session_state["messages"],temperature=0.3
            )
            message_response = response["choices"][0]["message"]["content"]
            st.session_state["messages"] += [
                {"role": "system", "content": message_response}
            ]
            show_messages(text)
