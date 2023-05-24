import openai 
import streamlit as st
#import config


def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("メッセージ履歴", value=str("\n".join(messages_str)), height=400)


st.header("GPTアシスタント")

##If used privately : openai.api_key = config.api_key

#If used with streamlitcloud
openai.api_key = st.secrets["chatGPT"]["OPENAI_KEY"]
BASE_PROMPT = [{"role": "system", "content": "あなたは関西弁で話す親切なおばちゃんです"}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT


text = st.empty()
show_messages(text)

col1_1, col1_2 = st.columns([6,1]);
with col1_1:
    st.caption("GPT3.5があなたの質問に答えます。履歴を消したい場合は消去を押して下さい")
with col1_2:
    if st.button("消去"):
        st.session_state["messages"] = BASE_PROMPT
        show_messages(text)

col2_1, col2_2, col2_3 = st.columns([5, 1, 1])
with col2_1:
    prompt = st.text_input("入力欄 👇", value="",placeholder="ここに質問を記入してください")

with col2_2:
    temp = st.radio("回答形式",("厳密", "程々", "自由"))
    temp_dict = {"厳密":0, "程々":0.5, "自由":1}
    Select_temp = temp_dict[temp]

with col2_3:
    st.caption("送信して質問")
    if st.button("送信"):
        with st.spinner("メッセージを生成中..."):
            st.session_state["messages"] += [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=st.session_state["messages"], temperature=Select_temp, max_tokens =256
            )
            message_response = response["choices"][0]["message"]["content"]
            st.session_state["messages"] += [
                {"role": "system", "content": message_response}
            ]
            show_messages(text)
