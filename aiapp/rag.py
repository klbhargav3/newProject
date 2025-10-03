from openai import OpenAI
from decouple import config
from pypdf import PdfReader
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import textwrap

def word_wrap(text,width=80):
    return textwrap.fill(text,width)

client=OpenAI(api_key=config("OPENAI_API_KEY"))
def get_text(file):
    reader=PdfReader(file)
    extract_text=[p.extract_text().strip() for p in reader.pages]
    extract_all_text=[text for text in extract_text if text]

    char_split=RecursiveCharacterTextSplitter(
        separators=["\n\n","\n","."," ",""],
        chunk_size=1000,
        chunk_overlap=200
    )

    char_text_split=char_split.split_text("\n\n".join(extract_all_text))
    return char_text_split

def get_rag(query,file):
    char_text=get_text(file)

    chroma_client=chromadb.Client()

    if "user_docs" in[col.name for col in chroma_client.list_collections()]:
        chroma_client.delete_collection(name="user_docs")

    embedding_function=OpenAIEmbeddingFunction(
        model_name="text-embedding-3-small",
        api_key=config("OPENAI_API_KEY")
    )


    chroma_collection=chroma_client.create_collection(
        name="user_docs",
        embedding_function=embedding_function
    )
    
    ids=[f"{file}_{i}" for i in range(len(char_text))]
    chroma_collection.add(ids=ids,documents=char_text)

    if query:
        result=chroma_collection.query(
            query_texts=[query],
            n_results=5,
            include=["documents"]
        )

        retrieved=result["documents"]
        retrieved_text=[text for doc in retrieved for text in doc]

        
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Answer using only the provided information."},
            {"role": "user", "content": f"Information: {retrieved_text}\nQuestion: {query}"}
        ]

        response=client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3
        )

        content=response.choices[0].message.content
        return word_wrap(content)