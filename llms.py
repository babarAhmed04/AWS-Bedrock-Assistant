from langchain.llms.bedrock import Bedrock
import boto3

bedrock = boto3.client(service_name="bedrock-runtime")

def get_llm(model_id):
    # Default parameters for llama
    model_kwargs = {'max_gen_len': 512}

    # parameters for the Titan model
    if "titan" in model_id.lower():  
        model_kwargs = {'maxTokenCount': 8192}

    return Bedrock(model_id=model_id, client=bedrock, model_kwargs=model_kwargs)