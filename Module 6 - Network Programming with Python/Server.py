"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Server



"""

from breezypythongui import EasyFrame
import tkinter.filedialog


class AddressBookServer(EasyFrame):

    def __init__(self):
        """Sets up the window,widgets, and data."""
        EasyFrame.__init__(self, title="Address Book Server")

        self.file_open_btn = self.addButton(text="Open", row=0, column=0, command=self.file_open)
        self.file_label = self.addLabel(text="Please open an address book.", row=0, column=1)

        self.status_label = self.addLabel(text="Server not running.", row=1, column=0, foreground="red")

    def file_open(self):
        filetype_list = [("Comma Separated Values (CSV)", "*.csv")]
        self.filename = tkinter.filedialog.askopenfilename(parent=self, filetypes=filetype_list)

        if self.filename != "":
            try:
                file = open(self.filename, "rw")
                self.address_book = file.read()
                file.close()

            except IOError:
                self.messageBox(title="Error", message="I/O Error occurred while opening the file.")


def main():
    """Instantiate and pop up the window."""
    AddressBookServer().mainloop()


if __name__ == "__main__":
    main()
