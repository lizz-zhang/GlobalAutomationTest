import openai
from openai import OpenAI
from pydantic import BaseModel
from autoUtils.file_creation import create_file


client = OpenAI()


class Page(BaseModel):
    page_name: str
    menu_name: str
    module_name: str
    page_object_file_directory_name: str
    page_object_file_name: str
    page_object_file_content: str
    test_case_file_directory_name: str
    test_case_file_name: str
    test_case_file_content: str


class TestGenerationResponse(BaseModel):
    pages: list[Page]


# read prompt_system.md file as system content
with open("prompts/openai_prompt_system.md", "r") as file:
    system_content = file.read()

# read pages.csv file as user content
with open("prompts/pages.csv", "r") as file:
    user_content = file.read()

try:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        response_format=TestGenerationResponse,
    )
    response = completion.choices[0].message
    if response.parsed:
        pages = response.parsed.pages
        # print(pages)

        # create files based on the provided pages
        for page in pages:
            create_file(
                page.page_object_file_directory_name,
                page.page_object_file_name,
                page.page_object_file_content,
            )
            create_file(
                page.test_case_file_directory_name,
                page.test_case_file_name,
                page.test_case_file_content,
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
