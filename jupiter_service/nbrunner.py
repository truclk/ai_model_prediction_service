# Execute a notebook over Jupyter Lab API
#
# Based on https://stackoverflow.com/a/54551221/942520

import argparse
import datetime
import json
import os
import sys
import uuid
from pprint import pprint

import requests
from websocket import WebSocketTimeoutException
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


# Main function
# This is the entrypoint for both local and cloud execution
# The event and context arguments are only used when running in the cloud
def main(notebook_path=None, training_file_path=None, predict_column=None):

    verbose = False
    # Notebook path on Jupyter server with a leading slash
    notebook_path = notebook_path
    training_file_path = training_file_path
    predict_column = predict_column
    # Either http or https
    protocol = "http"
    # Jupyter server address and port
    jupyter_server = os.environ.get("JUPYTER_SERVER")
    headers = {"Authorization": f"Token {os.environ['JUPYTER_TOKEN']}"}
    # Create a kernel
    url = f"{protocol}://{jupyter_server}/api/kernels"
    print(f"Creating a new kernel at {url}", file=sys.stderr)
    with requests.post(url, headers=headers) as response:
        pprint({"kernel": response.headers}, sys.stderr) if verbose else None
        kernel = json.loads(response.text)

    # Load the notebook and get the code of each cell
    url = f"{protocol}://{jupyter_server}/api/contents{notebook_path}"
    with requests.get(url, headers=headers) as response:
        file = json.loads(response.text)
    pprint({"notebook_content": file}, sys.stderr) if verbose else None
    # filter out non-code cells like markdown
    code = [
        c["source"]
        for c in file["content"]["cells"]
        if len(c["source"]) > 0 and c["cell_type"] == "code"
    ]
    # Execution request/reply is done on websockets channels
    ws = create_connection(
        f"{'ws' if protocol == 'http' else 'wss'}://{jupyter_server}/api/kernels/{kernel['id']}/channels",
        header=headers,
    )

    print("Sending execution requests for each cell", file=sys.stderr)
    for code_line in code:
        if code_line.startswith("training_file = ") and training_file_path is not None:
            code_line = f"training_file = '{training_file_path}'"
        elif code_line.startswith("predict_column = ") and predict_column is not None:
            code_line = f"predict_column = '{predict_column}'"
        ws.send(json.dumps(send_execute_request(code_line)))

    code_blocks_to_execute = len(code)
    accuracy_score = 0
    roc_auc_score = 0

    while code_blocks_to_execute > 0:
        try:
            rsp = json.loads(ws.recv())
            msg_type = rsp["msg_type"]
            if msg_type == "error":
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

        if (
            msg_type == "execute_reply"
            and rsp["metadata"].get("status") == "ok"
            and rsp["metadata"].get("dependencies_met", False)
        ):
            code_blocks_to_execute -= 1

    print("Processing finished. Closing websocket connection", file=sys.stderr)
    ws.close()

    # Delete the kernel
    print("Deleting kernel", file=sys.stderr)
    url = f"{protocol}://{jupyter_server}/api/kernels/{kernel['id']}"
    response = requests.delete(url, headers=headers)
    return {"accuracy_score": accuracy_score, "roc_auc_score": roc_auc_score}


if __name__ == "__main__":
    print(main(None))
