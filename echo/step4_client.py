import asyncio
from os.path import expanduser
import socket
import ssl

import httpx


async def http_echo_client(message: str):
    host = socket.gethostname()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(expanduser("~/.keys/cacerts.pem"))
    context.load_cert_chain(
        certfile=expanduser("~/.keys/client.crt"),
        keyfile=expanduser("~/.keys/client.key"),
    )

    async with httpx.AsyncClient(verify=context) as client:
        response = await client.post(
            f"https://{host}:8888/echo",
            content=message.encode()
        )
        print(response.content.decode())

asyncio.run(http_echo_client('Hello World!'))
