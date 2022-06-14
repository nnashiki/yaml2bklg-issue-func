import json
import logging

import azure.functions as func
from pydantic import BaseModel, ValidationError


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
        RequestBodyModel(**req_body)
    except ValidationError as e:
        return func.HttpResponse(
            e.json(),
            status_code=400,
            mimetype="application/json",
        )

    is_success_main_process, message = main_process(req_body)

    if is_success_main_process is True:
        res_body = {"message": message}
        return func.HttpResponse(
            json.dumps(res_body),
            status_code=200,
            mimetype="application/json",
        )
    else:
        return func.HttpResponse("process error", status_code=500)


def main_process(_) -> (bool, str):
    return True, "success"


class RequestBodyModel(BaseModel):
    param_str: str
    param_int: int
