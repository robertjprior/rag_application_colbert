import requests
from streamlit.runtime.uploaded_file_manager import UploadedFile
import fastapi
import io
import logging
import json

# the SERVER_URL matches the name of the service in the docker compose network bridge
SERVER_URL = "http://fastapi_server:8082"


def get_fastapi_status(server_url: str = SERVER_URL):
    """Access FastAPI /docs endpoint to check if server is running"""
    try:
        response = requests.get(f"{server_url}/docs")
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False


def post_store_arxiv(arxiv_ids: list[str], server_url: str = SERVER_URL):
    """Send POST request to FastAPI /store_arxiv endpoint"""
    payload = dict(arxiv_ids=arxiv_ids)
    response = requests.post(f"{SERVER_URL}/store_arxiv", data=payload)
    return response

def ensure_list(value):
    """Ensures the given value is a list. If not, converts it to a list."""
    if not isinstance(value, list):
        value = [value]  # Enclose in a list if not already a list
    return value

def post_store_data_files(db_file: UploadedFile, document_content_fields: list, id_field: str, metadata_fields: list, server_url: str = SERVER_URL):
    """Send POST request to FastAPI /store_pdfs endpoint"""
    #files = [("pdf_files", f) for f in pdf_files] #for multiple files since we can do it async with \
    #store_docs from the server.py file in backend folder
    
    #fake_upload_file = fastapi.UploadFile(
    #    filename=db_file.filename,
    #    content_type="text/csv",  # Assuming CSV files
    #    size=len(db_file.getvalue()),
    #    file=io.BytesIO(db_file.getvalue())
    #)

    document_field_assignments = dict(
        content_body_columns = document_content_fields,
        id_column = id_field,
        metadata_columns = metadata_fields
    )
    #data = {'data': json.dumps(document_field_assignments)}
    data = document_field_assignments
    fake_upload_file = io.BytesIO(db_file.getvalue())
    logging.info("file converted to BytesIO")
    response = requests.post(f"{SERVER_URL}/store_docs", data = data, files={"db_file": fake_upload_file})
    return response


def get_rag_summary(
    rag_query: str,
    #hybrid_search_alpha: float,
    retrieve_top_k: int,
    server_url: str = SERVER_URL,
):
    """Send GET request to FastAPI /rag_summary endpoint"""
    payload = dict(
        rag_query=rag_query, retrieve_top_k=retrieve_top_k
    )
    response = requests.get(f"{SERVER_URL}/rag_summary", params = payload) 
    #data=payload) instead of params=payload) #can be used if fastapi.Forms is default in api setup
    return response


def get_all_documents_file_name():
    """Send GET request to FastAPI /documents endpoint"""
    response = requests.get(f"{SERVER_URL}/documents")
    return response
