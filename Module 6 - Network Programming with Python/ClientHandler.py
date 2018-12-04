"""
Created by Seth Phillips with assistance of Eric Betz
File: phonebookclienthandler.py
Project 10.5
This file acts as a client handler within the addressbook program.
It allows the client to interact with the address book data. 
The client may search for a name in the listing.
Search for a name in the listing.
Add a name to the list.

"""

from socket import *
from codecs import decode

BUFSIZE = 1024
CODE = "ascii"  # Default set to use ascii characters
                # You can specify other encoding, such as UTF-8 for non-English characters


class ClientHandler():
    """Handles a phonebook requests from a client."""

    def __init__(self, client, addressbook):
        """Saves references to the client socket and phonebook."""
        self.client = client
        self.addressbook = addressbook
        # Welcomes user to program when connected to server
    def run(self):
        self.client.send(bytes("Welcome to the phone book application!", CODE))
        while True:
            message = decode(self.client.recv(BUFSIZE), CODE)
            if not message:
                # Displays connection status as disconnected if no connection is present
                print("Client disconnected")
                self.client.close()
                break
            else:
                request = message.split(";")
                command = request[0]
                # Sets up search funtionality and process
                if command == "FIND":
                    result = self.addressbook.get_by_name(request[1])
                    if not result:
                        # Display when name is not present in address book
                        reply = "Name not found."
                    else:
                        for entry in result:
                            outbound = entry
                            self.client.send(bytes(outbound, CODE))
                            inbound = decode(self.client.recv(BUFSIZE), CODE)
                            if not inbound:
                                # Displays connection status if closed
                                print("Client disconnected")
                                self.client.close()
                                break
                        reply = "DONE"
                     # Allows adding to the address book
                elif command == "ADD":
                    self.addressbook.add(request[1])
                    # Confirms the information has been added
                    reply = "Name and number added to address book."
                elif command == "LIST":
                    # Lists data from address book
                    for entry in self.addressbook:
                        outbound = str(entry)
                        self.client.send(bytes(outbound, CODE))
                        inbound = decode(self.client.recv(BUFSIZE), CODE)
                        if not inbound:
                            # Displays connection status if closed
                            print("Client disconnected")
                            self.client.close()
                            break
                    reply = "DONE"
                self.client.send(bytes(reply, CODE))


