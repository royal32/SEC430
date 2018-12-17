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
from threading import Thread
import re

BUFSIZE = 1024
CODE = "ascii"  # Default set to use ascii characters


# You can specify other encoding, such as UTF-8 for non-English characters


class ClientHandler(Thread):
    """Handles a phonebook requests from a client."""

    def __init__(self, server, client, addressbook):
        """Saves references to the client socket and phonebook."""
        Thread.__init__(self)
        self.server = server
        self.client = client
        self.addressbook = addressbook
        # Welcomes user to program when connected to server

    def run(self):
        """
        Main loop of the handler; Waits for commands from the client to interact with the server.

        Communication Diagram:
        inbound = decoded data received from a client.
        message = list containing each piece of the inbound message. (eg. ['ADD','Data1,Data2']
            command = The piece of the inbound message before the delimiting semicolon.
            payload = The piece of the inbound message after the delimiting semicolon.

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
                command = message[0].strip()
                payload = message[1].strip()

                if command == "FIND":
                    # Lists entries matched by regex
                    result = self.addressbook.get_by_name(payload)
                    if not result:
                        break
                    else:
                        for entry in result:
                            outbound = entry
                            self.client.send(bytes(outbound, CODE))
                            inbound = decode(self.client.recv(BUFSIZE),
                                             CODE)  # The client responds with OK for each entry received.
                            if not inbound:
                                # Displays connection status if closed
                                print("Client disconnected")
                                self.client.close()
                                break

                elif command == "ADD":
                    # Allows adding to the address book
                    self.addressbook.set([payload])  # [string] crates a list of one string

                elif command == "UPDATE":
                    # Allows a client to edit an entry
                    self.addressbook.update(payload)

                elif command == "LIST":
                    # Lists all entries from address book
                    for entry in self.addressbook:
                        outbound = str(entry)
                        self.client.send(bytes(outbound, CODE))
                        inbound = decode(self.client.recv(BUFSIZE), CODE)
                        if not inbound:
                            # Displays connection status if closed
                            print("Client disconnected")
                            self.client.close()
                            break
                    self.addressbook.iter_reset()

                elif command == "SAVE":
                    # Tell the server to write the addressbook to the file
                    self.server.save_file()

                self.client.send(bytes("DONE", CODE))
