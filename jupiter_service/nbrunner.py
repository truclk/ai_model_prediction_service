import datetime
import json
import os
import sys
import uuid
from pprint import pprint

import requests
from websocket import create_connection

if "JUPYTER_TOKEN" not in os.environ:
    raise Exception("JUPYTER_TOKEN environment variable must be set")


def send_execute_request(code):
    msg_type = "execute_request"
    content = {"code": code, "silent": False}
    hdr = {
        "msg_id": uuid.uuid1().hex,
        "username": "test",
        "session": uuid.uuid1().hex,
        "data": datetime.datetime.now().isoformat(),
        "msg_type": msg_type,
        "version": "5.0",
    }
    msg = {"header": hdr, "parent_header": hdr, "metadata": {}, "content": content}
    return msg


def upload_notebook(notebook_path, notebook_content):
    pass


def get_csrf_token(jupyter_server, headers):
    url = f"http://{jupyter_server}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for cookie in response.cookies:
            if cookie.name == "_xsrf":
                return cookie.value
    raise Exception("Could not get CSRF token")


def main_training(notebook_path=None, training_file_path=None, predict_column=None, features=None, parameters_str=None):
    verbose = False
    notebook_path = notebook_path
    training_file_path = training_file_path
    predict_column = predict_column
    protocol = "http"
    jupyter_server = os.environ.get("JUPYTER_SERVER")
    headers = {"Authorization": f"Token {os.environ['JUPYTER_TOKEN']}"}
    errors = []

    csrf_token = get_csrf_token(jupyter_server, headers)
    headers["X-CSRFToken"] = csrf_token

    url = f"{protocol}://{jupyter_server}/api/kernels"
    print(f"Creating a new kernel at {url}", file=sys.stderr)
    with requests.post(url, headers=headers) as response:
        pprint({"kernel": response.headers}, sys.stderr) if verbose else None
        kernel = json.loads(response.text)

    url = f"{protocol}://{jupyter_server}/api/contents{notebook_path}"
    with requests.get(url, headers=headers) as response:
        file = json.loads(response.text)
        if response.status_code != 200:
            errors.append(response.text)
            return {}, errors

    pprint({"notebook_content": file}, sys.stderr) if verbose else None
    code = [c["source"] for c in file["content"]["cells"] if len(c["source"]) > 0 and c["cell_type"] == "code"]

    ws = create_connection(
        f"{'ws' if protocol == 'http' else 'wss'}://{jupyter_server}/api/kernels/{kernel['id']}/channels",
        header=headers,
    )

    print("Sending execution requests for each cell", file=sys.stderr)
    for code_line in code:
        if code_line.startswith("dsr_training_file = ") and training_file_path is not None:
            code_line = f"dsr_training_file = '{training_file_path}'"
        elif code_line.startswith("dsr_predict_column = ") and predict_column is not None:
            code_line = f"dsr_predict_column = '{predict_column}'"
        elif code_line.startswith("dsr_features = ") and features is not None:
            # I want to have feature print in list format with quotes in string
            feature_str = ", ".join([f"'{f}'" for f in features])
            code_line = f"dsr_features = [{feature_str}]"
        elif code_line.startswith("dsr_parameters_str = ") and features is not None:
            # I want to have feature print in list format with quotes in string
            code_line = f"dsr_parameters_str = '{parameters_str}'"
        ws.send(json.dumps(send_execute_request(code_line)))

    code_blocks_to_execute = len(code)
    accuracy_score = 0
    roc_auc_score = 0
    f1_score = 0
    best_parameters = ""

    while code_blocks_to_execute > 0:
        try:
            rsp = json.loads(ws.recv())
            msg_type = rsp["msg_type"]
            if msg_type == "error":
                errors.append(rsp["content"]["evalue"])
                pprint({"exception": rsp["content"]}, sys.stderr)
                raise Exception(rsp["content"]["traceback"][0])
        except Exception as _e:
            print(_e, sys.stderr)
            break

        if msg_type == "execute_result" and verbose:
            pprint(rsp["content"])
        if rsp["content"].get("name", "") == "stdout":
            if rsp["content"]["text"].startswith("accuracy_score:"):
                accuracy_score = float(rsp["content"]["text"].strip().split(":")[1])
            if rsp["content"]["text"].startswith("roc_auc_score:"):
                roc_auc_score = float(rsp["content"]["text"].strip().split(":")[1])
            if rsp["content"]["text"].startswith("f1_score:"):
                f1_score = float(rsp["content"]["text"].strip().split(":")[1])
            if rsp["content"]["text"].startswith("best_parameters:"):
                best_parameters = rsp["content"]["text"].replace("best_parameters:", "")
            print(rsp["content"]["text"])

        if (
            msg_type == "execute_reply"
            and rsp["metadata"].get("status") == "ok"
            and rsp["metadata"].get("dependencies_met", False)
        ):
            code_blocks_to_execute -= 1

    print("Processing finished. Closing websocket connection", file=sys.stderr)
    ws.close()

    print("Deleting kernel", file=sys.stderr)
    url = f"{protocol}://{jupyter_server}/api/kernels/{kernel['id']}"
    response = requests.delete(url, headers=headers)
    return {
        "accuracy_score": accuracy_score,
        "roc_auc_score": roc_auc_score,
        "f1_score": f1_score,
        "best_parameters": best_parameters,
    }, errors


if __name__ == "__main__":
    print(main_training(None))
