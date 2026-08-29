from web_ingestion import WebIngestion


pipeline = WebIngestion()


query = "What is artificial intelligence?"


vector_store = pipeline.ingest(
    query
)


print("Testing completed!")