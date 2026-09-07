from litellm import acompletion


class AIService:

    def __init__(self, model_config: dict):
        self.model_config = model_config

    async def ask(self, text: str) -> str:
        response = await acompletion(
            model=self.model_config["model_id"],
            api_key=self.model_config["api_key"],
            base_url=self.model_config["base_url"],
            messages=[
                {"role": "user", "content": text}
            ],
        )
        return response.choices[0].message.content