"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Client



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
        """Initialize the frame and widgets."""
        EasyFrame.__init__(self, title="Address Book Client")
        # Add the labels, fields, and button

        self.addrListBox = self.addListbox(row=0, column=0, columnspan=3)

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
        self.statusLabel = self.addLabel(text="Not connected to a server.",
                                         row=2, column=0,
                                         columnspan=3)

    def find(self):
        """Looks up a name in the phone book."""
        name = self.prompterBox(promptString="Enter the name.")
        if name == "": return
        self.server.send(bytes("FIND;" + name, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if not reply:
            self.messageBox(message="Server diconnected")
            self.disconnect()
        else:
            self.statusLabel["text"] = reply

    def add(self):
        """Adds a name and number to the phone book."""
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
        package = ("ADD;{},{},{},{},{},{},{}"
                   .format(first, last, phone, street, city, state, zip))
        self.server.send(bytes(package, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if not reply:
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

    def disconnect(self):
        self.server.close()
        self.statusLabel["text"] = "Want to connect?"
        self.connectBtn["text"] = "Connect"
        self.connectBtn["command"] = self.connect
        self.findBtn["state"] = "disabled"
        self.addBtn["state"] = "disabled"

    def download(self):
        self.statusLabel["text"] = "Downloading..."
        inbound = ""
        self.server.send(bytes("LIST;", CODE))
        i = 0
        while True:
            inbound = decode(self.server.recv(BUFSIZE), CODE)
            if inbound != "DONE":
                self.addrListBox.insert(i, inbound)
                outbound = self.server.send(bytes("OK", CODE))
                i += 1
            else:
                break


def main():
    """Instantiate and pop up the window."""
    AddressBookClient().mainloop()


if __name__ == "__main__":
    main()
