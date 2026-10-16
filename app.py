import streamlit as st

from main import build_index, retrieve_and_answer

st.set_page_config(page_title="AI TA Chatbot", page_icon="🎓")

st.title("AI TA Chatbot")
st.caption("Ask questions about your Machine Learning lecture slides.")


@st.cache_resource(show_spinner="Reading lecture PDFs and building the index...")
def load_index():
    return build_index()


try:
    index, chunks, sources = load_index()
except Exception as e:
    st.error(str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, used = retrieve_and_answer(prompt, index, chunks, sources)
                response = answer + "\n\n*Sources: " + ", ".join(used) + "*"
            except Exception as e:
                response = f"Sorry, something went wrong: {e}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
