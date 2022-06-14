import json
import logging
import os

import azure.functions as func
import yaml
from azure.storage.blob import BlobServiceClient, ContainerClient
from pydantic import BaseModel, ValidationError

from yaml2bklg.core import BacklogIssueAddReq, add_issues


class RequestBodyModel(BaseModel):
    blob_container_name: str
    issue_metafile_name: str


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # parse request body
    try:
        req_body: dict = req.get_json()
        logging.debug(req_body)
    except ValueError:
        return func.HttpResponse("can't parse body", status_code=400)

    if not isinstance(req_body, dict):
        return func.HttpResponse("can't parse body", status_code=400)

    if len(req_body.keys()) == 0:
        return func.HttpResponse("need any body parameters", status_code=400)

    # validate request body
    try:
        req = RequestBodyModel(**req_body)
    except ValidationError as e:
        return func.HttpResponse(
            e.json(),
            status_code=400,
            mimetype="application/json",
        )

    is_success_main_process, message = main_process(req)

    if is_success_main_process is True:
        res_body = {"message": message}
        return func.HttpResponse(
            json.dumps(res_body),
            status_code=200,
            mimetype="application/json",
        )
    else:
        return func.HttpResponse("process error", status_code=500)


def main_process(req: RequestBodyModel) -> (bool, str):
    issue_metafile_path = f"./data/{req.issue_metafile_name}"
    if not os.path.isfile(issue_metafile_path):
        get_remote_issue_metafile(req.blob_container_name, req.issue_metafile_name)
    with open(issue_metafile_path) as issue_metafile:
        parsed_yaml = yaml.safe_load(issue_metafile)
        if "project_id" not in parsed_yaml:
            print("project_idがありません")
        if "parent_issue_summary" not in parsed_yaml:
            print("親課題の件名がありません")
        if "parent_issue_description" not in parsed_yaml:
            print("親課題の詳細がありません")
        if "parent_issue_type_id" not in parsed_yaml:
            print("親課題の詳細がありません")
        project_id = parsed_yaml["project_id"]

        parent_req = BacklogIssueAddReq(
            projectId=project_id,
            summary=parsed_yaml["parent_issue_summary"],
            description=parsed_yaml["parent_issue_description"],
            issueTypeId=parsed_yaml["parent_issue_type_id"],
        )
        child_issues_req = [
            BacklogIssueAddReq(
                projectId=project_id,
                summary=child_issue["child_issue_summary"],
                description=child_issue["child_issue_description"],
                issueTypeId=child_issue["child_issue_type_id"],
            )
            for child_issue in parsed_yaml["child_issues"]
        ]
        add_issues(parent_req=parent_req, child_issues_req=child_issues_req)

    return True, "success"


def get_remote_issue_metafile(blob_container_name: str, issue_metafile_name: str):
    storage_account_connect_str = os.environ.get("STORAGE_ACCOUNT_CONNECT_STR", "")
    blob_service_client = BlobServiceClient.from_connection_string(storage_account_connect_str)
    container_client: ContainerClient = blob_service_client.get_container_client(blob_container_name)
    with open(f"data/{item.name}", "wb") as my_blob:
        my_blob.write(container_client.download_blob(issue_metafile_name).readall())
