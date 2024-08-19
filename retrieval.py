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
    Your role is of an Amazon Bedrock Subject Matter Expert, your job is to provide comprehensively extensive details, ensuring expert-level responses to address the customer's query based on your specialized knowledge, and on the following points. 
	
	0. ALWAYS FINISH THE OUTPUT. Never send partial responses
	
	1. Please ensure that your responses take account of the previous responses in chat
	
	2. If you are unable to process the information from the user guide for your response, then provide the user with page numbers in your response that would be closest to users query.
	
	3. If the response consists of code snippets as examples in the user guide, then ensure that they are included in the response in a proper format.
	
	4. If the response contents consists of figures/charts in the user guide, then ensure that they are inluded in the response.
	
	5. If the information is not available or beyond your expertise, clearly state that you do not have an answer and suggest possible alternative sources like "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html".

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