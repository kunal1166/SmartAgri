
import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL")
model_id = os.getenv("GRANITE_MODEL_ID")

if not all([api_key, project_id, url, model_id]):
    raise ValueError("Missing IBM credentials. Check your .env file.")

credentials = Credentials(
    url=url,
    api_key=api_key
)

model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id,
    params={
        "max_new_tokens": 150,
        "temperature": 0.3
    }
)

response = model.chat(
    messages=[
        {
            "role": "user",
            "content": "You are SmartAgri, an agricultural assistant. Explain why soil testing is important for farmers."
        }
    ],
    params={
        "max_tokens": 150,
        "temperature": 0.3
    }
)

print("\n========== SMARTAGRI GRANITE TEST ==========")
print(response["choices"][0]["message"]["content"])
print("\nGranite connection test completed.")
