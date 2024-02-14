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

_tags_re = re.compile(r'<[^>]+>')

def strip_html_tags(text: str) -> str:
    return _tags_re.sub('', text)

def store_documents(
    ragatouille_db_instance: RAGPretrainedModel,  # Assuming this dependency is provided
    vector_db_url: str,
    db_file: UploadFile,
) -> None:
    """Store arxiv objects in Weaviate in batches.
    The vector and references between Document and Chunk are specified manually
    """
    try:
        
        #db = sqlite_utils.Database(db_file)  # Use db_file.filename directly
        # Process the db content (same logic as before)
       # entries = list(db["blog_entry"].rows)
        entries = pd.read_csv(db_file.file)
        entry_texts = [
            entry["title"] + '\n' + strip_html_tags(entry["body"])
            for entry_id, entry in entries.iterrows()
        ]
        entry_ids = [str(entry["id"]) for entry_id, entry in entries.iterrows()]
        entry_metadatas = [
            {"slug": entry["slug"], "created": entry["created"]} for entry_id, entry in entries.iterrows()
        ]

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
    
    _test_upload_file = Path('database.csv')
    from io import BytesIO
    bio = BytesIO()
    

    file_path = _test_upload_file
    with open(file_path, "rb") as f:
        bio.write(f.read())
        bio.seek(0)
        f = bio
        uploaded_file = UploadFile(f)# to make a mock fastapi upload file
    
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
        vector_db_url="backend/.ragatouille/colbert/indexes/blog/",
        db_file = uploaded_file,
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