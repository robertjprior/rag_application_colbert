from ragatouille import RAGPretrainedModel


def ragatouille_db_instance(vector_db_url: str) -> RAGPretrainedModel:
    """Instantiate Weaviate client for the local instance based on the url"""
    try:
        rag = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
        return rag
    except Exception as e:
        raise e





if __name__ == "__main__":
    # run as a script to test Weaviate + Hamilton locally
    import vector_db

    from hamilton import driver

    inputs = dict(
        vector_db_url="http://localhost:8083",
    )

    dr = driver.Builder().with_modules(vector_db).build()

    results = dr.execute(final_vars=["ragatouille_db_instance"], inputs=inputs)
