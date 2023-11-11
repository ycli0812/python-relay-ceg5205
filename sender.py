from utils import proc_print


def send(q, bind_port=7777, remote_port=8888):
    if q is None:
        proc_print('This function must be run in a sub-process and require a Queue.')
        return

    # create server and wait for connection
    # TODO: connect to Unity socket
    # relay = RelayServer.RelayServer(host='127.0.0.1', port=bind_port)
    # relay.connect(host='127.0.0.1', port=remote_port)

    # ready to receive
    while True:
        while not q.empty():
            data = q.get()
            # TODO: store data
            # TODO: feed data into the model
            # TODO: send data to Unity client
            proc_print('Sender:', sum(data))

