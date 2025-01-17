from openai import AzureOpenAI
import os


client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
)

completion = client.chat.completions.create(
    model="GPT4oChat",  # GPT4oChat
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."},
    ],
)
print(completion)
print(completion.choices[0].message)
