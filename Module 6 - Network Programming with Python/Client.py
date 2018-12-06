"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Client
This program creates a gui based virtual client to interact with the virtual server.


"""

from socket import *
from codecs import decode
from breezypythongui import EasyFrame

"""Configuration"""
HOST = "localhost"
PORT = 7000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
CODE = "ascii"


class AddressBookClient(EasyFrame):

    def __init__(self):
        """Initialize the frame and widgets for the GUI"""
        EasyFrame.__init__(self, title="Address Book Client")
        # Add the labels, fields, and buttons

        self.addrListBox = self.addListbox(row=0, column=0, columnspan=3)
        # Creates find button
        self.findBtn = self.addButton(row=1, column=0,
                                      text="Find",
                                      command=self.find,
                                      state="disabled")
        # Creates add button
        self.addBtn = self.addButton(row=1, column=1,
                                     text="Add",
                                     command=self.add,
                                     state="disabled")
        # Creates connection button to connect to server
        self.connectBtn = self.addButton(row=1, column=2,
                                         text="Connect",
                                         command=self.connect)
        # Creates display of server connection status
        self.statusLabel = self.addLabel(text="Not connected to a server.",
                                         row=2, column=0,
                                         columnspan=3)

    def find(self):
        """Looks up a name in the phone book."""
        # Prompts user for input of desired search
        namere = self.prompterBox(promptString="Enter the name.")
        if namere == "": return
        self.server.send(bytes("FIND;" + namere, CODE))
        result = []
        i = 0
        while True:
            # Ensures the server is connected, continues search until complete or server disconnect
            inbound = decode(self.server.recv(BUFSIZE), CODE)
            if not inbound:
                self.messageBox(message="Server disconnected")
                self.disconnect()
            elif inbound != "DONE":
                result.append(inbound)
                self.server.send(bytes("OK", CODE))
                i += 1
            elif inbound == "DONE":
                if not result:
                    result.append("No results found.")
                break

        self.messageBox(message=", ".join(result), width=75)

    def add(self):
        """Adds name, number, and address to the phone book."""
        first = self.prompterBox(promptString="Enter the first name.")
        if first == "": return
        last = self.prompterBox(promptString="Enter the last name.")
        if last == "": return
        phone = self.prompterBox(promptString="Enter the phone number.")
        if phone == "": return
        street = self.prompterBox(promptString="Enter the street address.")
        if street == "": return
        city = self.prompterBox(promptString="Enter the city.")
        if city == "": return
        state = self.prompterBox(promptString="Enter the state.")
        if state == "": return
        zip = self.prompterBox(promptString="Enter the zip code.")
        if zip == "": return
        # Adds commas for delimination
        package = ("ADD;{},{},{},{},{},{},{}"
                   .format(first, last, phone, street, city, state, zip))
        self.server.send(bytes(package, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if not reply:
            # Creates notification of server disconnection
            self.messageBox(message="Server disconnected")
            self.disconnect()
        else:
            self.statusLabel["text"] = reply

    # Connect to server and confirm connection

    def connect(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(ADDRESS)
        self.statusLabel["text"] = decode(self.server.recv(BUFSIZE), CODE)
        self.connectBtn["text"] = "Disconnect"
        self.connectBtn["command"] = self.disconnect
        self.findBtn["state"] = "normal"
        self.addBtn["state"] = "normal"
        self.download()

    # Disconnects from server
    def disconnect(self):
        self.server.close()
        self.statusLabel["text"] = "Want to connect?"
        self.connectBtn["text"] = "Connect"
        self.connectBtn["command"] = self.connect
        self.findBtn["state"] = "disabled"
        self.addBtn["state"] = "disabled"

    # notifies user of download status
    def download(self):
        self.statusLabel["text"] = "Downloading..."
        self.addrListBox.clear()
        inbound = ""
        self.server.send(bytes("LIST;", CODE))
        i = 0
        while True:
            inbound = decode(self.server.recv(BUFSIZE), CODE)
            if inbound != "DONE":
                self.addrListBox.insert(i, inbound)
                self.server.send(bytes("OK", CODE))
                i += 1
            else:
                break
        self.statusLabel["text"] = "Finished downloading"


def main():
    """Instantiate and pop up the window."""
    AddressBookClient().mainloop()


if __name__ == "__main__":
    main()
