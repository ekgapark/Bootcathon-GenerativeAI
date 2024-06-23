# Import required libraries  
import streamlit as st
import os
from openai import AzureOpenAI, DefaultHttpxClient
from dotenv import load_dotenv, find_dotenv
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from azure.search.documents.models import Vector  

# Configure environment variables  
load_dotenv(find_dotenv('credential.env'), override=True)

# Azure AI Search
service_endpoint = os.environ['AZURE_AI_SEARCH_ENDPOINT']
key = os.environ['AZURE_AI_SEARCH_KEY']
index_name = os.environ['AZURE_AI_SEARCH_INDEX_NAME']
credential = AzureKeyCredential(key)

#Azure OpenAI
client = AzureOpenAI(
  api_key = os.environ['AZURE_OPENAI_API_KEY'],  # this is also the default, it can be omitted
  azure_endpoint = os.environ['AZURE_OPENAI_API_ENDPOINT'],
  api_version = os.environ['AZURE_OPENAI_API_VERSION'],
  http_client=DefaultHttpxClient(verify=False)
)
embedding_model = os.environ['EMBEDDING_MODEL_NAME']
gpt35turbo_model = os.environ['GPT35TURBO_MODEL_NAME']
gpt4turbo_model = os.environ['GPT4TURBO_MODEL_NAME']
gpt4o_model = os.environ['GPT4O_MODEL_NAME']

def generate_embeddings(text):
    print("embedding_query: "+text)
    response = client.embeddings.create(input=text, model=embedding_model)
    return response.data[0].embedding


def get_chat_completion(messages, model):
    print(f'Generating answer using {model} LLM model')
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def format_retrieved_documents(data_list):
    retrieved_documents = ""
    for item in data_list:
        # Extract the 'content' and 'sourcepage' values
        content = item.get('content', '')
        sourcepage = item.get('sourcepage', '')
        retrieved_documents += "sourcepage: "+sourcepage+ ", content: "+content+"\n"
    return retrieved_documents

st.title("Bootcathon GenAI Assistant")

# Initialize system prompt
# System prompt includes table information, rules, and prompts the LLM to produce a welcome message to the user.
st.subheader('System Prompt')

system_prompt = """- You are an AI assistance to help answer questions based on retrieved document.
"""

system_prompt = st.text_area('Update system prompt below', system_prompt)

st.subheader('Chat Panel')
# Initialize the chat messages history
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        messages = [
            {"role": "system", "content": system_prompt + " and introduce yourself for first greeting."},
            {"role": "user", "content": ""}
        ]

        # GPT Model Option: gpt35turbo_model, gpt4turbo_model and gpt4o_model
        response = get_chat_completion(messages, gpt4o_model)
        st.markdown(response)
else:
    with st.chat_message("assistant"):
        st.markdown("Hello! I'm your AI assistant. How can I help you today?")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    search_client = SearchClient(service_endpoint, index_name, credential=credential)

    vector = Vector(value=generate_embeddings(prompt), k=3, fields="contentVector")

    # Search using vector content and Semantic meaning search in Azure AI Search
    results = search_client.search(
        search_text=prompt,
        vectors=[vector],
        select=["content", "sourcepage"],
        query_type="semantic", query_language="en-us", semantic_configuration_name='my-semantic-config', query_caption="extractive", query_answer="extractive",
        top=3
    )  

    result_list = []
    for result in results:  
        result_list.append(result)

    system_prompt = system_prompt + "## Retrieved documents: "+format_retrieved_documents(result_list)

    system_message = [{"role": "system", "content": system_prompt},]
    
    input_prompt_message = system_message + st.session_state.messages
    print(input_prompt_message)
    
    # GPT Model Option: gpt35turbo_model, gpt4turbo_model and gpt4o_model
    response = get_chat_completion(input_prompt_message, gpt4o_model)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

    def reset_chat():
        st.session_state.messages = []

    if st.button('Clear Chat', on_click=reset_chat):
        st.success('Chat cleared!')
