import asyncio
from os.path import expanduser
import socket
import ssl


async def tcp_echo_client(message):
    host = socket.gethostname()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_verify_locations(
        expanduser("~/.keys/cacerts.pem")
    )
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True

    reader, writer = await asyncio.open_connection(
        host,
        8888,
        ssl=context
    )

    peercert = writer.get_extra_info('peercert')
    print(f'Peer cert: {peercert!r}')

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client('Hello World!'))
