from typing import List

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_core.documents import Document
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_code(code_dir: str) -> List[Document]:
    language = Language.PYTHON
    return split_docs(__load_code(code_dir, language), language)


def __load_code(code_dir: str, language: Language) -> List[Document]:
    loader = GenericLoader.from_filesystem(
        code_dir,
        glob="**/*",
        suffixes=[".py"],
        exclude=[],
        parser=LanguageParser(language=language, parser_threshold=500),

    )
    documents = loader.load()
    return documents


def split_docs(documents: List[Document], language: Language) -> List[Document]:
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=language, chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)
    return texts
