"""
File: phonebookclienthandler.py
Project 10.5
Client handler for phonebook.
"""

from socket import *
from codecs import decode

BUFSIZE = 1024
CODE = "ascii"  # You can specify other encoding, such as UTF-8 for non-English characters


class ClientHandler():
    """Handles a phonebook requests from a client."""

    def __init__(self, client, addressbook):
        """Saves references to the client socket and phonebook."""
        self.client = client
        self.addressbook = addressbook

    def run(self):
        self.client.send(bytes("Welcome to the phone book application!", CODE))
        while True:
            message = decode(self.client.recv(BUFSIZE), CODE)
            if not message:
                print("Client disconnected")
                self.client.close()
                break
            else:
                request = message.split()
                command = request[0]
                if command == "FIND":
                    number = self.addressbook.get(request[1])
                    if not number:
                        reply = "Number not found."
                    else:
                        reply = "The number is " + number + '.'
                else:
                    self.addressbook.add(request[1], request[2])
                    reply = "Name and number added to phone book."
                self.client.send(bytes(reply, CODE))


