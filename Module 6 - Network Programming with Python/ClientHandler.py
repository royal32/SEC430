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
import re

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
        """
        Main loop of the handler; Waits for commands from the client to interact with the server.

        Communication Diagram:
        inbound = decoded data received from a client.
        message = list containing each piece of the inbound message. (eg. ['ADD','Data1,Data2']

        """
        self.client.send(bytes("Welcome to the address book application!", CODE))

        while True:
            inbound = decode(self.client.recv(BUFSIZE), CODE)
            if not inbound:
                # Displays connection status as disconnected if no connection is present
                print("Client disconnected")
                self.client.close()
                break
            else:

                # The anticipated command format is COMMAND;DATA
                # Currently does not handle malformed commands and is probably
                # super exploitable..... Might be a fun experiment.

                message = inbound.split(";")  # Splits the received command by semicolon.
                command = message[0]
                payload = message[1]

                if command == "FIND":
                    result = self.addressbook.get_by_name(payload)
                    if not result:
                        # Display when name is not present in address book
                        reply = "DONE"
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
                    self.addressbook.add([payload])  # [string] crates a list of one string
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
                    self.addressbook.iter_reset()
                self.client.send(bytes(reply, CODE))
