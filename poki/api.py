import os
from pathlib import Path
import re
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, Header, Request, Response

from poki.store import PasteStore

DATA_DIR = Path(os.environ.get("POKI_DATA_DIR", "./lipu"))
store = PasteStore(DATA_DIR)

app = FastAPI()


IPV4_REGEX = re.compile(r"^http://([0-9]{1,3}.){3}([0-9]{1,3})(:[0-9]{1,5})?/$")


def get_base_url(request: Request) -> str:
    # TODO: handle IPv6
    if IPV4_REGEX.match(str(request.base_url)):
        return str(request.base_url)

    return "https://" + request.headers["host"] + "/"


@app.get("/")
async def read_root(request: Request) -> Response:
    return Response(
        f"""<!DOCTYPE html>
<html>
    <head>
        <title>Poki</title>
        <style>
            * {{
                color-scheme: light dark;
            }}

            html {{
                display: flex;
                flex-direction: column;

                height: 100%;
            }}

            body {{
                flex-grow: 1;

                display: flex;
                justify-content: center;
                align-items: center;
            }}
        </style>
    </head>
    <body>
        <main>
            <h1>Hello, welcome to Poki.</h1>

            <p>Poki is a simple, extremely minimal pastebin-like service.
            You can make an upload to this page using <code><raw>echo "example" | curl --data-binary @- {get_base_url(request)}lipu</raw> -H "Authorization: Bearer &lt;your token here&gt;"</code>.</p>
        </main>
    </body>
</html>""",
        headers={"content-type": "text/html"},
    )


@app.post("/")
@app.post("/lipu")
async def upload_content(
    content: Annotated[bytes, Body()],
    request: Request,
    authorization: Annotated[str, Header()] = "",
):
    if not authorization or not len(authorization.split()) == 2:
        raise HTTPException(
            401, "You do not have authorization to upload files to this server."
        )

    if authorization.split()[1] != os.environ.get("POKI_API_KEY"):
        raise HTTPException(
            401, "You do not have authorization to upload files to this server."
        )

    hash = store.add(content)
    uri = f"{get_base_url(request)}lipu/{hash}"

    return {"uri": uri}


@app.get("/lipu/{hash}")
async def read_lipu(hash: str) -> Response:
    content = store.get(hash)

    if content is None:
        raise HTTPException(404, "That upload does not exist.")

    return Response(content)


@app.delete("/lipu/{hash}")
async def delete_lipu(hash: str, authorization: Annotated[str, Header()] = ""):
    if not authorization or not len(authorization.split()) == 2:
        raise HTTPException(401, "You do not have authorization to remove files.")

    if authorization.split()[1] != os.environ.get("POKI_API_KEY"):
        raise HTTPException(401, "You do not have authorization to remove files.")

    store.remove(hash)
