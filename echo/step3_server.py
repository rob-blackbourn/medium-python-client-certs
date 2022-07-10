import asyncio
from os.path import expanduser
import socket
import ssl


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    peercert = writer.get_extra_info('peercert')
    print(f"Received {message!r} from {addr!r} with cert {peercert!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    host = socket.gethostname()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(
        expanduser("~/.keys/server.crt"),
        expanduser("~/.keys/server.key")
    )
    context.load_verify_locations(
        expanduser("~/.keys/cacerts.pem")
    )
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True

    server = await asyncio.start_server(
        handle_echo,
        host,
        8888,
        ssl=context
    )

    addrs = ', '.join(
        str(sock.getsockname())
        for sock in server.sockets
    )
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
