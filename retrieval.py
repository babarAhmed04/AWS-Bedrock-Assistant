from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from embeddings import bedrock_embeddings
from config import FAISS_INDEX_PATH
from langchain.vectorstores import FAISS

def get_response(llm, history, current_question):
    # Load the vector store for document retrieval
    vector_store = FAISS.load_local(FAISS_INDEX_PATH, bedrock_embeddings, 
                                    allow_dangerous_deserialization=True)

    # Defining the prompt template 
    prompt_template_text = """
    Human: As an Amazon Bedrock Subject Matter Expert, your role is to provide all the details, ensuring expert-level responses based on your specialized knowledge. Please ensure that your responses take account of the previous responses in chat, are comprehensive and directly address the customer's query. If the information is not available or beyond your expertise, clearly state that you do not have an answer and suggest possible alternative sources or actions.

    <Context>
    {context}
    </Context>

    Question: {question}

    Assistant:
    """

   
    full_context = " ".join(history)  # Combine entire history into one string

    # Initialize the PromptTemplate
    prompt_template = PromptTemplate(
        template=prompt_template_text,
        input_variables=["context", "question"]
    )

    # inputs for the retrieval model
    inputs = {
        "context": full_context,
        "query": current_question
    }

    # Create the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )

    # Invoke the chain with prepared inputs
    result = qa_chain(inputs)
    
    return result.get('result', "No answer found.")