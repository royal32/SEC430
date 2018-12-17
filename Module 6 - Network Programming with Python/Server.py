"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Server

This program creates a virtual server for client interaction.
It uses a gui interface to turn on and off the server.  
"""

from breezypythongui import EasyFrame
import tkinter.filedialog
import os
import threading
import re
from socket import *
from Addressbook import ThreadSafeAddressbook
from ClientHandler import ClientHandler

"""Configuration"""
HOST = "localhost"
PORT = 7000
ADDRESS = (HOST, PORT)


class AddressBookServer(EasyFrame):

    def __init__(self):
        """Sets up the window,widgets, and data."""
        EasyFrame.__init__(self, title="Address Book Server")
        # Sets attributes for and creates and labels a button to open files
        self.file_open_btn = self.addButton(text="Open", row=0, column=0, command=self.open_file)
        self.file_label = self.addLabel(text="Please open an address book.", row=0, column=1)
        # Default setting of server status
        self.server_running = False
        # List of the available status states for the server
        self.status_label_dict = {"running": "Server is running.", "not_running": "Server is not running.",
                                  "error": "An error occurred."}
        # Sets attributes for and creates and labels start button
        self.status_button = self.addButton(text="Start", row=1, column=0, command=self.toggle_server)
        self.status_label = self.addLabel(text=self.status_label_dict["not_running"], row=1, column=1, foreground="red")

        self.server = socket(AF_INET, SOCK_STREAM)

    def open_file(self):
        """
        Loads a .csv from an OS load file dialog,
        creates a list from it, adds it to the addressbook, and closes it.
        """
        filetype_list = [("Comma Separated Values (CSV)", "*.csv")]
        filename = tkinter.filedialog.askopenfilename(parent=self, filetypes=filetype_list)
        try:
            file = open(filename, "r")
            data = list(file)
            file.close()
            data.pop(0)  # Remove the "First Name,Last Name,Phone,Address,City,State,Zip" line from the file
            self.addressbook = ThreadSafeAddressbook()
            self.addressbook.add(data)
            self.addressbook.set_filename(filename)
            self.file_label["text"] = os.path.basename(filename) + " loaded."

        except IOError:
            # File error message
            self.messageBox(title="Error", message="I/O Error occurred while opening the file.")

        except IndexError:
            self.messageBox(title="Error", message="An error has occurred. Check the format of the file.")

        print(str(self.addressbook))

    def save_file(self):
        """Opens the addressbook file on the disk and saves the contents of the addressbook object to it."""
        filename = self.addressbook.get_filename()
        file = open(filename, "w")
        data = "First Name,Last Name,Phone,Address,City,State,Zip\n" + str(self.addressbook)
        file.write(data)
        file.close()
        print("Addressbook Saved")

    # Turns the server on and off.
    def toggle_server(self):
        """Determines whether an addressbook is loaded and starts the server, or shuts it down if its running."""
        if self.server_running:
            self.stop_server()
            self.status_label["text"] = self.status_label_dict["not_running"]
            self.status_label["foreground"] = "red"
        elif self.addressbook.get_filename() != "":
            """Start the server, but do it in a new thread so that the GUI stays responsive."""
            threading.Thread(target=self.start_server).start()
            self.status_label["text"] = self.status_label_dict["running"]
            self.status_label["foreground"] = "green"
        else:
            # Notifies user to load address book prior to server start
            self.messageBox(title="Error", message="Please load an address book before starting the server.")

    # Defines what server does if / when started
    def start_server(self):
        """Start the server"""
        try:
            self.server.bind(ADDRESS)
            self.server.listen(5)
            print("listening")
            self.server_running = True
        except OSError:
            self.messageBox(title="Error", message="There was an error starting the server.")

        while self.server_running:
            try:
                print("Waiting for connection ...")
                (client, address) = self.server.accept()
                print("... connected from: ", address)
            except:
                self.messageBox(title="Error", message="There was an error connecting to a client.")
                break

            try:
                clienthandler = ClientHandler(self, client, self.addressbook)
                clienthandler.start()
            except:
                self.messageBox(title="Error", message="There was an error starting a client handler.")
                break

    def stop_server(self):
        """Stop the server. Haven't gotten this working yet."""
        # self.server.shutdown(SHUT_RDWR)  # Currently throws an error
        # self,server.close()  # Currently throws an error
        print("server stopped")
        return


def main():
    """Instantiate and pop up the window."""
    AddressBookServer().mainloop()


if __name__ == "__main__":
    main()
