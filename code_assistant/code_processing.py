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



def load_code(code_dir: str)-> List[Document]:
    return split_docs(__load_code(code_dir))


def __load_code(code_dir: str)-> List[Document]:
    loader = GenericLoader.from_filesystem(
        code_dir,
        glob="**/*",
        suffixes=[".py"],
        exclude=[],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),

    )
    documents = loader.load()
    return documents

def split_docs(documents: List[Document]) -> List[Document]:

    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)
    return texts
