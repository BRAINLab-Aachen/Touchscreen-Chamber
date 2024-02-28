import socket


class Hallway_UDP:
    def __init__(self):
        self._serverAddressPort = ("127.0.0.1", 20001)

        # Create a UDP socket at client side
        self.udp_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #

    def send(self, message="Hello UDP Server"):

        # Send to server using created UDP socket
        self.udp_client.sendto(str.encode(message), self._serverAddressPort)
    #

    def read(self):
        bufferSize = 1024
        message_received = self.udp_client.recvfrom(bufferSize)
        msg = "Message from Server {}".format(message_received[0])
        print(msg)
    #
#
