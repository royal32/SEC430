"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Server



"""

from breezypythongui import EasyFrame
import tkinter.filedialog
import os
import threading
import re
from socket import *
from Addressbook import Addressbook
from ClientHandler import ClientHandler

"""Configuration"""
HOST = "localhost"
PORT = 7000
ADDRESS = (HOST, PORT)

addressbook = Addressbook()
server = socket(AF_INET, SOCK_STREAM)


class AddressBookServer(EasyFrame):

    def __init__(self):
        """Sets up the window,widgets, and data."""
        EasyFrame.__init__(self, title="Address Book Server")

        self.file_open_btn = self.addButton(text="Open", row=0, column=0, command=self.open_file)
        self.file_label = self.addLabel(text="Please open an address book.", row=0, column=1)

        self.server_running = False
        self.status_label_dict = {"running": "Server is running.", "not_running": "Server is not running.",
                                  "error": "An error occurred."}
        self.status_button = self.addButton(text="Start", row=1, column=0, command=self.toggle_server)
        self.status_label = self.addLabel(text=self.status_label_dict["not_running"], row=1, column=1, foreground="red")

    def open_file(self):
        filetype_list = [("Comma Separated Values (CSV)", "*.csv")]
        filename = tkinter.filedialog.askopenfilename(parent=self, filetypes=filetype_list)

        if filename != "":
            try:
                file = open(filename, "r")
                data = list(file)
                data.pop(
                    0)  # This program expects the first line to be "First Name,Last Name,Phone,Address,City,State,Zip", this removes that
                addressbook.add(data)
                addressbook.set_filename(filename)
                file.close()
                print(str(addressbook))
                self.file_label["text"] = os.path.basename(filename) + " loaded."

            except IOError:
                self.messageBox(title="Error", message="I/O Error occurred while opening the file.")

    def toggle_server(self):
        if self.server_running:
            self.stop_server()
            self.status_label["text"] = self.status_label_dict["not_running"]
            self.status_label["foreground"] = "red"
        elif addressbook.get_filename() != "":
            """Start the server, but do it in a new thread so that the GUI stays responsive."""
            threading.Thread(target=self.start_server).start()
            self.status_label["text"] = self.status_label_dict["running"]
            self.status_label["foreground"] = "green"
        else:
            self.messageBox(title="Error", message="Please load an address book before starting the server.")

    def start_server(self):
        server.bind(ADDRESS)
        server.listen(5)
        print("listening")
        self.server_running = True
        while True:
            print("Waiting for connection ...")
            (client, address) = server.accept()
            print("... connected from: ", address)
            clienthandler = ClientHandler(client, addressbook)
            threading.Thread(target=clienthandler.run()).start()

    def stop_server(self):
        server.shutdown(SHUT_RDWR) # Currently throws an error
        server.close() # Currently throws an error
        print("server stopped")
        return


def main():
    """Instantiate and pop up the window."""
    AddressBookServer().mainloop()


if __name__ == "__main__":
    main()
