from typing import List

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

import code_assistant
import sys
import argparse
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from code_assistant.code_processing import load_code


def question(ask: str, model: str, api_key: str, code_path: str, temperature=0.5) -> str:
    texts = load_code(code_path)

    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8},
    )

    chat = ChatOpenAI(model=model, temperature=temperature, api_key=api_key)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            (
                "user",
                "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
            ),
        ]
    )

    retriever_chain = create_history_aware_retriever(chat, retriever, prompt)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user's questions based on the below context:\n\n{context}",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )
    document_chain = create_stuff_documents_chain(chat, prompt)

    qa = create_retrieval_chain(retriever_chain, document_chain)

    result = qa.invoke({"input": ask})

    return result['answer']
