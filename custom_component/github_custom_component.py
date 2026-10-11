# from lfx.field_typing import Data
from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput
from lfx.schema.data import Data
from composio import Composio
from composio_langchain import LangchainProvider

class CustomComponent(Component):
    display_name = "Custom Component"
    description = "Use as a template to create your own component."
    documentation: str = "https://docs.langflow.org/components-custom-components"
    icon = "code"
    name = "CustomComponent"
    ALLOWWED_TOOLS = [
        "GITHUB_GET_THE_AUTHENTICATED_USER", "GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER",
        "GITHUB_GET_A_REPOSITORY", "GITHUB_GET_REPOSITORY_CONTENT", "GITHUB_GET_A_TREE",
        "GITHUB_LIST_BRANCHES", "GITHUB_LIST_COMMITS", "GITHUB_GET_A_COMMIT",
        "GITHUB_LIST_REPOSITORY_ISSUES", "GITHUB_GET_AN_ISSUE", "GITHUB_LIST_ISSUE_COMMENTS",
        "GITHUB_LIST_PULL_REQUESTS", "GITHUB_GET_A_PULL_REQUEST", "GITHUB_LIST_PULL_REQUESTS_FILES",
        "GITHUB_SEARCH_CODE", "GITHUB_SEARCH_REPOSITORIES", "GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS",
        "GITHUB_CREATE_AN_ISSUE", "GITHUB_UPDATE_AN_ISSUE", "GITHUB_CREATE_AN_ISSUE_COMMENT",
        "GITHUB_CREATE_BRANCH", "GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS", "GITHUB_COMMIT_MULTIPLE_FILES",
        "GITHUB_CREATE_A_PULL_REQUEST", "GITHUB_UPDATE_A_PULL_REQUEST",
        "GITHUB_CREATE_A_REVIEW_FOR_A_PULL_REQUEST",
    ]

    inputs = [
        MessageTextInput(
            name="tools_choosen",
            display_name="Input Value",
            info="This is a custom component Input",
            tool_mode=True,
        ),
        SecretStrInput(      
            name="API_KEY",
            display_name="YOUR API_KEY",
            info="This is to place your compossio api key"
        )
    ]

    outputs = [
        Output(display_name="Output", name="output", method="github_output"),
    ]

    def github_output(self) -> Data:
        composio = Composio(api_key=self.API_KEY,provider=LangchainProvider())
        if self.tools_choosen in self.ALLOWWED_TOOLS:

            data = Data(value="Allowed")
            result = composio.tools.execute(user_id="default",arguments={},dangerously_skip_version_check=True,slug=self.tools_choosen)
            

            if result["successful"]:
                return Data(value=result["data"])
            else:
                return Data(value={"error": result["error"]})
                
        else:
            return "Not Allowed"
