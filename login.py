from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint
from dotenv import load_dotenv
import os

load_dotenv()

personal_access_token = os.environ["AZURE_DEVOPS_PAT"]
organization_url = f"https://dev.azure.com/{os.environ['AZURE_DEVOPS_ORG']}"
project_name = os.environ["AZURE_DEVOPS_PROJECT_NAME"]
variable_value = os.environ["AZURE_DEVOPS_VARIABLE_VALUE"]

credentials = BasicAuthentication("", personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

build_client = connection.clients.get_build_client()
build_definitions = build_client.get_definitions(project=project_name)

index = 0
build_definition_ids = []
while build_definitions is not None:
    for build_definition in build_definitions.value:
        build_definition_ids.append(build_definition.id)
        index += 1
    if (
        build_definitions.continuation_token is not None
        and build_definitions.continuation_token != ""
    ):
        build_definitions = build_definitions = build_client.get_definitions(
            project=project_name,
            continuation_token=build_definitions.continuation_token,
        )
    else:
        build_definitions = None
print(build_definition_ids)
build_definition_details = []
for build_definition_id in build_definition_ids:
    build_definition_detail = build_client.get_definition(
        project=project_name, definition_id=build_definition_id
    )
    build_definition_details.append(build_definition_detail)
for build_definition in build_definition_details:
    for k, v in build_definition.variables.items():
        if v.value == variable_value:
            print(k, "---", v.value)
