import asyncio
import websockets
from utils import proc_print
import time


def websocket_receive(lock, q, port=12345):
    if q is None:
        return

    async def echo(websocket, path):
        async for message in websocket:
            try:
                data = eval(message)
                q.put(data)
            except Exception as e:
                proc_print('Parse failed.')

    start_server = websockets.serve(echo, "0.0.0.0", port)  # Change the host and port if needed
    lock.release()

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
