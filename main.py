import streamlit as st
from document_processing import load_and_split_documents
from embeddings import init_vector_store, vector_store_exists
from llms import get_llm
from retrieval import get_response
from config import DATA_DIR
import time as timer
import metrics_manager

def main():
    st.set_page_config("Amazon Bedrock Help Bot")
    st.header("Amazon Bedrock Help Bot")

    if 'history' not in st.session_state:
        st.session_state['history'] = []
    metrics_manager.initialize_metrics(st.session_state)

    
    if not vector_store_exists():
        with st.spinner("Initializing vector store..."):
            docs = load_and_split_documents(DATA_DIR)
            init_vector_store(docs)
            st.success("Vector store initialized!")

    with st.form(key='user_query_form'):
        user_question = st.text_input("How can i help?", key="user_input")
        model_choice = st.selectbox("Choose a model:", ["llama2", "llama3"], key="model_select")
        submit_button = st.form_submit_button("Get Answer")

    if submit_button and user_question:
        start_time = timer.time()
        with st.spinner("Fetching response..."):
           if model_choice == "llama3":
              llm = get_llm("meta.llama3-70b-instruct-v1:0")
              context = " ".join(st.session_state['history'])  
              response = get_response(llm, context, user_question)
           else:
              llm = get_llm("meta.llama2-70b-chat-v1")
              context = " ".join(st.session_state['history'])  
              response = get_response(llm, context, user_question)
           response_time = timer.time() - start_time
           metrics_manager.add_response_time(st.session_state, response_time)
           st.session_state['history'].append("User: " + user_question)
           st.session_state['history'].append("Bot: " + response)
        #    feedback = st.radio("Was this response helpful?", ("Yes", "No"), key=f"feedback_{len(st.session_state.history)//2}")
        #    metrics_manager.add_feedback(st.session_state, feedback)

    st.sidebar.title("Performance Metrics")
    response_times = metrics_manager.get_response_times(st.session_state)
    if response_times:
        st.sidebar.write("Response Times (s):")
        for idx, time_val in enumerate(response_times, 1):
            st.sidebar.write(f"{idx}. {time_val:.2f}s")

    # accuracy = metrics_manager.calculate_accuracy(st.session_state)
    # if accuracy:
    #     st.sidebar.title("Accuracy Metrics")
    #     st.sidebar.write(f"Accuracy: {accuracy:.2f}% based on user feedback.")
      
    st.markdown("### Conversation History:")
    for entry in reversed(st.session_state['history']):
        st.markdown(f"**{entry.split(': ')[0]}**: {entry.split(': ')[1]}", unsafe_allow_html=True)


    if st.button("Clear History"):
        st.session_state['history'] = []  
        metrics_manager.clear_metrics(st.session_state)
        st.success("Conversation history and metrics cleared!")

if __name__ == "__main__":
    main()
