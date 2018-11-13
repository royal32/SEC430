"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Client



"""

from breezypythongui import EasyFrame
import tkinter.filedialog


class AddressBookClient(EasyFrame):

    def __init__(self):
        """Sets up the window,widgets, and data."""
        EasyFrame.__init__(self, title="Address Book Client")


def main():
    """Instantiate and pop up the window."""
    AddressBookClient().mainloop()


if __name__ == "__main__":
    main()
