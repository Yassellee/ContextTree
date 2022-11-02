import openai

class openai_toolkit:
    def __init__(self, api_key="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"):
        openai.api_key = api_key

    def get_completion(self, prompt, engine="ada"):
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt
        )
        return response

# checkout the demo below as an example
# demo_openai = openai_toolkit()
# print(demo_openai.get_completion("This is a test"))
