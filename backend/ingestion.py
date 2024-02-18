import base64
import io
from pathlib import Path

from typing import Generator
from pathlib import Path
import pathlib
import pandas as pd

import fastapi
import re


from fastapi import FastAPI, UploadFile
import sqlite_utils
from ragatouille import RAGPretrainedModel
from config_backend.config_backend import logger

_tags_re = re.compile(r'<[^>]+>')

def strip_html_tags(text: str) -> str:
    return _tags_re.sub('', text)

def store_documents(
    ragatouille_db_instance: RAGPretrainedModel,  # Assuming this dependency is provided
    vector_db_url: str,
    db_file: pd.core.frame.DataFrame,#: UploadFile,
    content_body_columns: list[str],
    id_column: str,
    metadata_columns: list[str],
) -> None:
    """Store arxiv objects in Weaviate in batches.
    The vector and references between Document and Chunk are specified manually
    """
    try:
        
        logger.info("inside store_documents")

        #entries = pd.read_csv(db_file.file)
        entries = db_file
        entry_texts = [
            "\n".join(strip_html_tags(entry[col]) for col in content_body_columns)
            for entry_id, entry in entries.iterrows()
        ]
        entry_ids = entries[id_column].astype(str).tolist()
        entry_metadatas = entries[metadata_columns].to_dict('records')

        pathlib_vector_db_url = pathlib.PurePath(vector_db_url)
        index_name = str(pathlib_vector_db_url.name)

        ragatouille_db_instance.index(
            collection=entry_texts,
            document_ids=entry_ids,
            document_metadatas=entry_metadatas,
            index_name=index_name,
            max_document_length=180,
            split_documents=True
        )

        return {"message": "DB processed successfully!"}

    except Exception as e:
        return {"error": "Error processing db: " + str(e)}


if __name__ == "__main__":
    # run as a script to test Hamilton's execution
    import ingestion
    import vector_db

    from hamilton import driver
    #_test_upload_file = Path('simonwillisonblog.db')
    # db = sqlite_utils.Database("simonwillisonblog.db")
    # output = list(db["blog_entry"].rows)
    # import pandas as pd 
    # df = pd.DataFrame(output)
    # df.to_csv("database.csv")
    
    _test_upload_file = Path('test_backend/database.csv')
    from io import BytesIO
    bio = BytesIO()
    

    file_path = _test_upload_file
    with open(file_path, "rb") as f:
        bio.write(f.read())
        bio.seek(0)
        f = bio
        uploaded_file = UploadFile(f)# to make a mock fastapi upload file
    uploaded_file = pd.read_csv(_test_upload_file)
    import tempfile

    # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    #     temp_file.write(_files.read())

    #     # Create a mock UploadedFile object
    #     uploaded_file = UploadFile(filename=temp_file.name, file=temp_file)

    # Correctly create a mock UploadFile object using a temporary file
    # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    #     _test_upload_file = Path('simonwillisonblog.db')
    #     temp_file.write(_test_upload_file.read_bytes())  # Use read_bytes to read binary data
    #     uploaded_file = UploadFile(filename=temp_file.name, file=temp_file)


    inputs = dict(
        vector_db_url=".ragatouille/colbert/indexes/blog/",
        db_file = uploaded_file,
        content_body_columns= ['title', 'body'],
        id_column= "id",
        metadata_columns= ['slug', 'created'],
    )

    dr = (
        driver.Builder()
        .enable_dynamic_execution(allow_experimental_mode=True)
        .with_modules(ingestion, vector_db)
        .build()
    )

    results = dr.execute(
        final_vars=["store_documents"],
        inputs=inputs,
    )
    print(results)