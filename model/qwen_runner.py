from openai import OpenAI
client = OpenAI()

def generate_answer(prompt):
    # response = llm(
    #     prompt=prompt,
    #     max_tokens=512,
    #     temperature=0.5,
    #     stop=["<END>"]
    # )


    response = client.responses.create(
        model = "gpt-5-nano-2025-08-07",
        input = prompt,
        # stop = ["<END>"]
    )
    return response

