import openai
from openai import AzureOpenAI
from pydantic import BaseModel
from autoUtils.file_creation import create_file
import os


client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
)


class Drawer(BaseModel):
    module_name: str
    menu_name: str
    page_name: str
    drawer_name: str
    drawer_object_file_directory_name: str
    drawer_object_file_name: str
    drawer_object_file_content: str
    drawer_test_case_file_directory_name: str
    drawer_test_case_file_name: str
    drawer_test_case_file_content: str


class TestGenerationResponse(BaseModel):
    drawers: list[Drawer]


# read prompt_system.md file as system content
with open("prompts/drawers_openai_prompt_system.md", "r") as file:
    system_content = file.read()

# read drawers.csv file as user content
with open("prompts/drawers.csv", "r") as file:
    user_content = file.read()

try:
    completion = client.beta.chat.completions.parse(
        model="GPT4oChat",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        response_format=TestGenerationResponse,
    )
    response = completion.choices[0].message
    if response.parsed:
        drawers = response.parsed.drawers
        # print(drawers)

        # create files based on the provided drawers
        for drawer in drawers:
            create_file(
                drawer.drawer_object_file_directory_name,
                drawer.drawer_object_file_name,
                drawer.drawer_object_file_content,
            )
            create_file(
                drawer.drawer_test_case_file_directory_name,
                drawer.drawer_test_case_file_name,
                drawer.drawer_test_case_file_content,
            )
    elif response.refusal:
        # handle refusal
        print(response.refusal)
except Exception as e:
    # Handle edge cases
    if type(e) == openai.LengthFinishReasonError:
        # Retry with a higher max tokens
        print("Too many tokens: ", e)
        pass
    else:
        # Handle other exceptions
        print(e)
        pass
