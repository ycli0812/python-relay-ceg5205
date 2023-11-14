import multiprocessing
import websockets

from sender import send
from utils import proc_print
from receiver import websocket_receive

server_port = 12345
sender_port = 8888


async def mock_send():
    async with websockets.connect(f"ws://127.0.0.1:{server_port}") as websocket:
        with open('model/mock-sensor-control.csv', 'r') as fin:
            fin.readline()
            for line in fin:
                await websocket.send('[%s]' % (line.strip()))


if __name__ == '__main__':
    # random change
    proc_print('This is main process')
    queue = multiprocessing.Queue()
    lock = multiprocessing.Semaphore(2)

    # process handlers
    lock.acquire()  # lock for load model and setup of unity connector
    lock.acquire()  # lock for setup of host receiver
    p_test_receiver = multiprocessing.Process(target=websocket_receive, args=(lock, queue, server_port))
    p_test_sender = multiprocessing.Process(target=send, args=(lock, queue, sender_port, ))

    # start processed
    p_test_receiver.start()
    p_test_sender.start()

    lock.acquire()
    lock.release()

    # await processes
    p_test_receiver.join()
    p_test_sender.join()

