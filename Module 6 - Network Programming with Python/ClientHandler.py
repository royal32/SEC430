"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Client Handler

This program communicates directly with a client.
"""

from socket import *
from codecs import encode, decode
from threading import Thread
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import re

BUFSIZE = 1024
CODE = "utf-8"


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

        rng = Random.new().read
        RSAkey = RSA.generate(2048, rng)
        self.pubkey = RSA.importKey(RSAkey.publickey().exportKey("PEM"))
        # print(self.pubkey.exportKey("PEM"))
        self.privkey = RSA.importKey(RSAkey.exportKey("PEM"))
        self.decipher = PKCS1_OAEP.new(self.privkey)

        self.clientkey = None
        self.cipher = None

    def recv_and_decrypt(self):
        """
        Receive encrypted, encoded data from a client and return decrypted, decoded data.
        Also checks for a disconnected client.
        """
        inboundc = self.client.recv(BUFSIZE)
        if not inboundc:
            # Displays connection status if closed
            print("Client disconnected")
            self.client.close()
            return None
        inbound = decode(self.decipher.decrypt(inboundc), CODE)
        return inbound

    def send_and_encrypt(self, outbound):
        """Receive decrypted, decoded data from the main loop and return encrypted, encoded data to a client."""
        outboundc = self.cipher.encrypt(encode(outbound))
        self.client.send(outboundc)

    def run(self):
        """
        Main loop of the handler; Waits for commands from the client to interact with the server.

        Communication Diagram:
        inboundc = encrypted, encoded data received from a client.
        inbound = decrypted, decoded data received from a client.
        outboundc = encrypted, encoded data being sent to a client.
        outbound = decrypted, decoded data being sent to a client.
        message = list containing each piece of the inbound message. (eg. ['ADD','Data1,Data2']
            command = The piece of the inbound message before the delimiting semicolon.
            payload = The piece of the inbound message after the delimiting semicolon.

        """

        # Key exchange
        self.client.send(self.pubkey.exportKey("PEM"))
        inbound = decode(self.client.recv(BUFSIZE), CODE)
        if not inbound:
            print("Client disconnected")
            self.client.close()
            return
        self.clientkey = RSA.importKey(inbound)
        self.cipher = PKCS1_OAEP.new(self.clientkey)
        print("\nServer received clientkey:\n{}\n".format(decode(self.clientkey.exportKey("PEM"), CODE)))

        while True:
            inbound = self.recv_and_decrypt()
            if not inbound:
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
                            self.send_and_encrypt(outbound)
                            self.recv_and_decrypt()  # Receive acknowledgements ("OK") from the client


                elif command == "ADD":
                    # Allows adding to the address book
                    self.addressbook.set([payload])  # [string] crates a list of one string

                elif command == "UPDATE":
                    # Allows a client to edit an entry
                    self.addressbook.update(payload)

                elif command == "DELETE":
                    # Allows a client to edit an entry
                    self.addressbook.delete(payload)

                elif command == "LIST":
                    # Lists all entries from address book
                    for entry in self.addressbook:
                        outbound = str(entry)
                        self.send_and_encrypt(outbound)
                        self.recv_and_decrypt()  # Receive acknowledgements ("OK") from the client
                    self.addressbook.iter_reset()


                elif command == "SAVE":
                    # Tell the server to write the addressbook to the file
                    self.server.save_file()

                self.send_and_encrypt("DONE")
