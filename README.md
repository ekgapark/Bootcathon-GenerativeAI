# Bootcathon - Generative AI - Demystifying Retrieval Augmented Generation (RAG) 

## Introduction

**Bootcathon - Generative AI - Demystifying Retrieval Augmented Generation (RAG)** is an introduction to understanding the conceptual foundations of RAG technique based on Azure AI services including Azure OpenAI, Azure Document Intelligence and Azure AI Search.

This workshop consists of five challenges and is designed to be self-administered, so anyone can complete the material independently. Whether you have limited to no experience with Generative AI or have experimented with OpenAI before but want a deeper understanding of how to implement RAG based chat application, this hack is for you.

## Learning Objectives

This workshop is for anyone who wants to gain hands-on experience experimenting with foundation RAG and prompt engineering best practices, and apply them to generate effective responses from Azure OpenAI models.

Participants will learn how to:

- Provision Azure AI services using [Azure Portal](https://portal.azure.com)
- Use Azure SDK to interact with different Azure services
- Create a foundational RAG technique including data ingestion and data retrieval
- Create user and system prompts to control generated output from large language model

## Reference Architecture
![image](/Instructions/Images/chat-with-your-data.png)

## Challenges

- Challenge 00: **[Prerequisites - Set up IDE and Azure resources](Instructions/Challenge-00.md)**
  - Prepare your coding environment and provision Azure services
- Challenge 01: **[Explore Document Parsing and Chunking](Instructions/Challenge-01.md)**
  - Parse PDF documents using Azure Document Intelligence and break output into smaller chunks
- Challenge 02: **[Embedding chunks, create Azure AI search index](Instructions/Challenge-02.md)**
  - Use embedding model and upload vectorized content to Azure AI search	
- Challenge 03: **[Retrieve search output and interact with Azure OpenAI](Instructions/Challenge-03.md)**
  - Explore searching methods to find relevant context and use GPT model to generate the answer
- Challenge 04: **[Implement chat with your data web page using Streamlit](Instructions/Challenge-04.md)**
  - Create a simple chat interface to interact with Azure OpenAI based on your documents
- Challenge 05: **[Prompt Engineering](Instructions/Challenge-05.md)**
  - Use prompt engineering with RAG and interact with GPT model
  
## Contributors

- Ekgapark Wonghirunsombat
- Vorakarn Chiamsiri
- Nathaphop Sundarabhogin
