"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Client



"""

from socket import *
from codecs import decode
from breezypythongui import EasyFrame

HOST = "66.31.240.86"
PORT = 7000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
CODE = "ascii"


class AddressBookClient(EasyFrame):

    def __init__(self):
        """Initialize the frame and widgets."""
        EasyFrame.__init__(self, title="Address Book Client")
        # Add the labels, fields, and button
        self.statusLabel = self.addLabel(text="Do you want to connect to the Phonebook?",
                                         row=0, column=0,
                                         columnspan=3)
        self.findBtn = self.addButton(row=1, column=0,
                                      text="Find",
                                      command=self.find,
                                      state="disabled")
        self.addBtn = self.addButton(row=1, column=1,
                                     text="Add",
                                     command=self.add,
                                     state="disabled")
        self.connectBtn = self.addButton(row=1, column=2,
                                         text="Connect",
                                         command=self.connect)

    def find(self):
        """Looks up a name in the phone book."""
        name = self.prompterBox(promptString="Enter the name.")
        if name == "": return
        self.server.send(bytes("FIND " + name, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if not reply:
            self.messageBox(message="Server diconnected")
            self.disconnect()
        else:
            self.statusLabel["text"] = reply

    def add(self):
        """Adds a name and number to the phone book."""
        name = self.prompterBox(promptString="Enter the name.")
        if name == "": return
        number = self.prompterBox(promptString="Enter the number.")
        if number == "": return
        self.server.send(bytes("ADD " + name + " " + number, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if not reply:
            self.messageBox(message="Server diconnected")
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

    def disconnect(self):
        self.server.close()
        self.statusLabel["text"] = "Want to connect?"
        self.connectBtn["text"] = "Connect"
        self.connectBtn["command"] = self.connect
        self.findBtn["state"] = "disabled"
        self.addBtn["state"] = "disabled"


def main():
    """Instantiate and pop up the window."""
    AddressBookClient().mainloop()


if __name__ == "__main__":
    main()
