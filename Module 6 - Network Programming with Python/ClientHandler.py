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
                request = message.split(";")
                command = request[0]
                if command == "FIND":
                    namere = self.addressbook.get_by_name(request[1])
                    if not namere:
                        reply = "Name not found."
                    else:
                        self.addressbook.get_by_name(namere)
                        reply = "The name is " +  + '.'
                elif command == "ADD":
                    self.addressbook.add(request[1])
                    reply = "Name and number added to phone book."
                elif command == "LIST":
                    for entry in self.addressbook:
                        outbound = str(entry)
                        self.client.send(bytes(outbound, CODE))
                        inbound = decode(self.client.recv(BUFSIZE), CODE)
                        if not inbound:
                            print("Client disconnected")
                            self.client.close()
                            break
                    reply = "DONE"
                self.client.send(bytes(reply, CODE))


