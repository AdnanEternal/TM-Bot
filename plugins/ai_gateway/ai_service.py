from litellm import completion


llm_models={
    "GLM 4.7 F":{
        "model":"zai/glm-4.7-flash",
        "api key":"c28481904550430ea5334557643f5232.tXFhF47dCONlW8Cd",
        "base url":"https://api.z.ai/api/paas/v4/"
    }
}


class AIService:
    def __init__(self):
        self.active_model = "GLM 4.7 F"
        self.llm_data=llm_models[self.active_model]


    async def ask(self, text: str) -> str:
        response= completion(
            model=self.llm_data["model"],
            api_key=self.llm_data["api key"],
            base_url=self.llm_data["base url"],
            messages=[
                {
                    "role": "user",
                    "content": text
                    }
                    ]
                    )
        return response.choices[0].message.content