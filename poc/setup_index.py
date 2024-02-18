from ragatouille import RAGPretrainedModel
import re
import sqlite_utils

_tags_re = re.compile(r'<[^>]+>')

def strip_html_tags(text):
    return _tags_re.sub('', text)

def go():
    db = sqlite_utils.Database("simonwillisonblog.db")
    rag = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
    entries = list(db["blog_entry"].rows)
    entry_texts = [
        entry["title"] + '\n' + strip_html_tags(entry["body"])
        for entry in entries
    ]
    print("len of entry_texts is", len(entry_texts))
    entry_ids = [str(entry["id"]) for entry in entries]
    entry_metadatas = [
        {"slug": entry["slug"], "created": entry["created"]} for entry in entries
    ]
    rag.index(
        collection=entry_texts,
        document_ids=entry_ids,
        document_metadatas=entry_metadatas,
        index_name="blog", 
        max_document_length=180, 
        split_documents=True
    )


if __name__ == "__main__":
    go()
