from rag_pipeline import RAGPipeline



documents = [

    "Aircraft fly because wings generate lift.",

    "Lift is created because wings change the airflow direction and create pressure differences.",

    "Jet engines provide thrust which pushes aircraft forward."

]


rag = RAGPipeline(
    documents
)



while True:


    question = input(
        "\nAsk: "
    )


    if question.lower()=="exit":
        break


    answer = rag.ask(
        question
    )


    print(
        "\nAI:",
        answer
    )