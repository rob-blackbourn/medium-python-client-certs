import asyncio
from os.path import expanduser
import socket
import ssl

from hypercorn.asyncio import serve
from hypercorn.config import Config
from bareasgi import Application, HttpRequest, HttpResponse, text_reader, text_writer


async def echo(request: HttpRequest) -> HttpResponse:
    body = await text_reader(request.body)
    return HttpResponse(
        200,
        [(b'content_type', b'text/plain')],
        text_writer(body)
    )


async def main():
    host = socket.gethostname()

    app = Application()
    app.http_router.add({'POST'}, '/echo', echo)

    config = Config()
    config.bind = [f"{host}:8888"]
    config.certfile = expanduser("~/.keys/server.crt")
    config.keyfile = expanduser("~/.keys/server.key")
    config.ca_certs = expanduser("~/.keys/cacerts.pem")
    config.verify_mode = ssl.CERT_REQUIRED
    await serve(app, config)

asyncio.run(main())
