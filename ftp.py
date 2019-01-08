from ipc import *

class FTP(ABC):
    def __init__(self):
        self.server_address = ('localhost', 10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class FTPSender(SendingProtocol, FTP):
    def __init__(self):
        FTP.__init__(self)
        SendingProtocol.__init__(self)
        print('Attempting to connect...')
        self.sock.connect(self.server_address)
        print('Connected!')

    def send(self, data):
        if data[0] == 0:
            print('Terminal mssg with timestamp: ', data[self.varlist.index('timestamp_s')], ' ', data[self.varlist.index('timestamp_ns')])
        else:
            print('Sending data with timestamp: ', data[self.varlist.index('timestamp_s')], ' ', data[self.varlist.index('timestamp_ns')])
        packed_data = self.encode(data)
        self.sock.sendall(packed_data)

    def close(self):
        print('Ending Transmission...')
        self.sock.close()

class FTPReceiver(ReceivingProtocol, FTP):
    def __init__(self):
        FTP.__init__(self)
        ReceivingProtocol.__init__(self)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
        print('Awaiting connection...')
        self.connection, client_address = self.sock.accept()
        print('Connected!')

    def recv(self):
        data = self.connection.recv(self.packer.size)
        unpacked_data = self.decode(data)
        if unpacked_data[0] == 0:
            print('Terminal mssg with timestamp: ', unpacked_data[self.varlist.index('timestamp_s')], ' ', unpacked_data[self.varlist.index('timestamp_ns')])
        else:
            print('Received data with timestamp: ', unpacked_data[self.varlist.index('timestamp_s')], ' ', unpacked_data[self.varlist.index('timestamp_ns')])
        return unpacked_data

    def close(self):
        print("Ending Transmission...")
        self.connection.close()
        self.sock.close()
