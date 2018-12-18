"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Client
This program creates a gui based virtual client to interact with the virtual server.


"""

from socket import *
from codecs import encode, decode
from breezypythongui import EasyFrame

"""Configuration"""
HOST = "localhost"
PORT = 7000
ADDRESS = (HOST, PORT)
BUFSIZE = 1024
CODE = "utf-8"


class AddressBookClient(EasyFrame):

    def __init__(self):
        """Initialize the frame and widgets for the GUI"""
        EasyFrame.__init__(self, title="Address Book Client")
        # Add the labels, fields, and buttons

        self.addr_listbox = self.addListbox(row=0, column=0, columnspan=3)

        entry_event_panel = self.addPanel(row=1, column=0,
                                          columnspan=3)

        # Creates find button
        self.find_btn = entry_event_panel.addButton(row=0, column=0,
                                                    text="Find",
                                                    command=self.find,
                                                    state="disabled")
        # Creates add button
        self.add_btn = entry_event_panel.addButton(row=1, column=0,
                                                   text="Add",
                                                   command=self.add,
                                                   state="disabled")
        # Creates update button
        self.update_btn = entry_event_panel.addButton(row=0, column=1,
                                                      text="Update",
                                                      command=self.update,
                                                      state="disabled")

        # Creates delete button
        self.delete_btn = entry_event_panel.addButton(row=1, column=1,
                                                      text="Delete",
                                                      command=self.delete,
                                                      state="disabled")

        server_event_panel = self.addPanel(row=2, column=0,
                                           columnspan=3)

        # Creates button to tell the server to write the addressbook to the file
        self.save_btn = server_event_panel.addButton(row=0, column=0,
                                                     text="Save",
                                                     command=self.save,
                                                     state="disabled")

        # Creates refresh button to refresh the local addressbook
        self.refresh_btn = server_event_panel.addButton(row=0, column=1,
                                                        text="Refresh",
                                                        command=self.download,
                                                        state="disabled")

        # Creates connection button to connect to server
        self.connect_btn = server_event_panel.addButton(row=1, column=0,
                                                        columnspan=3,
                                                        text="Connect",
                                                        command=self.connect)

        # Creates display of client status
        self.status_label = server_event_panel.addLabel(text="Not connected to a server.",
                                                        row=3, column=0,
                                                        columnspan=3)

    def find(self):
        """Looks up a name in the phone book."""
        # Prompts user for input of desired search
        namere = self.prompterBox(promptString="Enter your query.")
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

        self.messageBox(message="".join(result), width=75)

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
        # Adds commas for delineation
        outbound = ("ADD;{},{},{},{},{},{},{}"
                   .format(first, last, phone, street, city, state, zip))
        self.server.send(bytes(outbound, CODE))
        inbound = decode(self.server.recv(BUFSIZE), CODE)
        if not inbound:
            # Creates notification of server disconnection
            self.messageBox(message="Server disconnected")
            self.disconnect()
        else:
            self.status_label["text"] = "Entry added."

    def update(self):
        """Adds name, number, and address to the phone book."""
        selected_entry = self.addr_listbox.getSelectedItem()
        if not selected_entry:
            self.messageBox(title="Error", message="Please select an entry.")
            return
        attributes = selected_entry.split(",")  # Split the entry into a list of attributes
        attributes = [a.strip() for a in attributes]  # Trim whitespace from each attribute
        first = self.prompterBox(inputText=attributes[0], promptString="Enter the first name.")
        if first == "": return
        last = self.prompterBox(inputText=attributes[1], promptString="Enter the last name.")
        if last == "": return
        phone = self.prompterBox(inputText=attributes[2], promptString="Enter the phone number.")
        if phone == "": return
        street = self.prompterBox(inputText=attributes[3], promptString="Enter the street address.")
        if street == "": return
        city = self.prompterBox(inputText=attributes[4], promptString="Enter the city.")
        if city == "": return
        state = self.prompterBox(inputText=attributes[5], promptString="Enter the state.")
        if state == "": return
        zip = self.prompterBox(inputText=attributes[6], promptString="Enter the zip code.")
        if zip == "": return
        # Adds commas for delineation
        outbound = ("UPDATE;{}:{},{},{},{},{},{},{}"
                   .format(selected_entry, first, last, phone, street, city, state, zip))
        self.server.send(bytes(outbound, CODE))
        inbound = decode(self.server.recv(BUFSIZE), CODE)
        if not inbound:
            # Creates notification of server disconnection
            self.messageBox(message="Server disconnected")
            self.disconnect()
        else:
            self.status_label["text"] = "Entry edited."

    def delete(self):
        """Tells the server to delete the selected entry"""
        self.status_label["text"] = "Deleting..."

        selected_entry = self.addr_listbox.getSelectedItem()
        if not selected_entry:
            self.messageBox(title="Error", message="Please select an entry.")
            return
        outbound = ("DELETE;{}".format(selected_entry))

        self.server.send(bytes(outbound, CODE))
        self.status_label["text"] = "Entry Deleted"

    def connect(self):
        """Connect to the server"""
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(ADDRESS)
        self.status_label["text"] = decode(self.server.recv(BUFSIZE), CODE)
        self.connect_btn["text"] = "Disconnect"
        self.connect_btn["command"] = self.disconnect
        self.find_btn["state"] = "normal"
        self.add_btn["state"] = "normal"
        self.update_btn["state"] = "normal"
        self.delete_btn["state"] = "normal"
        self.save_btn["state"] = "normal"
        self.refresh_btn["state"] = "normal"
        self.download()

    def disconnect(self):
        """Disconnect from the server"""
        self.server.close()
        self.status_label["text"] = "Want to connect?"
        self.connect_btn["text"] = "Connect"
        self.connect_btn["command"] = self.connect
        self.find_btn["state"] = "disabled"
        self.add_btn["state"] = "disabled"
        self.update_btn["state"] = "disabled"
        self.delete_btn["state"] = "disabled"
        self.save_btn["state"] = "disabled"
        self.refresh_btn["state"] = "disabled"

    def download(self):
        """Download the newest addressbook from the server"""
        self.status_label["text"] = "Downloading..."
        self.addr_listbox.clear()
        self.server.send(bytes("LIST;", CODE))
        while True:
            inbound = decode(self.server.recv(BUFSIZE), CODE)
            if inbound != "DONE":
                self.addr_listbox.insert(self.addr_listbox.size(), inbound)
                self.server.send(bytes("OK", CODE))
            else:
                break
        self.status_label["text"] = "Addressbook Synchronized."

    def save(self):
        """Tells the server to save its addressbook to the file"""
        self.status_label["text"] = "Saving..."
        self.server.send(bytes("SAVE;", CODE))
        self.status_label["text"] = "Saved"


def main():
    """Instantiate and pop up the window."""
    AddressBookClient().mainloop()


if __name__ == "__main__":
    main()
