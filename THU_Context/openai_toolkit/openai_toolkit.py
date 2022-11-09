import openai

class openai_toolkit:
    def __init__(self, 
    api_key="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", 
    engine="ada",
    temperature=0.5):
        openai.api_key = api_key
        self.engine = engine
        self.temperature = temperature

    def get_completion(self, prompt):
        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            temperature=self.temperature
        )
        return response.get("choices")[0].get("text")

# checkout the demo below as an example
# demo_openai = openai_toolkit()
# print(demo_openai.get_completion("This is a test"))
