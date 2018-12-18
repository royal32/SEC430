"""
Primary Author: Seth Phillips
Team Members: Seth Phillips, Eric Betz
Program: Address Book Object

This program represents an addressbook object.
"""

from sharedcell import SharedCell
import re


class ThreadSafeAddressbook(object):
    """This class represents a thread-safe addressbook."""

    def __init__(self):
        """Wrap a new addressbook in a shared cell for
        thread-safety."""
        self.addressbook = Addressbook()
        self.cell = SharedCell(self.addressbook)
        self.iter_current = 0

    def __iter__(self):
        """Declares that this class is iterable."""
        return self

    def __next__(self):
        """Facilitates iteration through the addressbook."""
        if self.iter_current >= len(self.addressbook.entries):  # Stop condition
            raise StopIteration
        else:
            result = self.addressbook.entries[self.iter_current]
            self.iter_current += 1
            return result

    def iter_reset(self):
        """Keeps track of the current index while iterating through the addressbook."""
        self.iter_current = 0

    def __str__(self):
        """Returns the string representation of the addressbook."""
        try:
            return self.cell.read(lambda addressbook: str(self.addressbook))
        except:
            self.cell.endRead()
            raise

    def set_filename(self, filename):
        """Set the filename of the addressbook for later retrieval if necessary."""
        try:
            return self.cell.write(lambda addressbook: self.addressbook.set_filename(filename))
        except:
            print("Error writing to addressbook. (set_filename function)")
            self.cell.endRead()
            raise

    def get_filename(self):
        """Returns the filename of the addressbook .csv that is loaded."""
        try:
            return self.cell.read(lambda addressbook: self.addressbook.get_filename())
        except:
            print("Error reading from addressbook. (get_filename function)")
            self.cell.endRead()
            raise

    def add(self, message):
        """Adds entry to addressbook."""
        try:
            return self.cell.write(lambda addressbook: self.addressbook.add(message))
        except:
            print("Error writing to addressbook. (add function)")
            self.cell.endWrite()
            raise

    def get_by_index(self, index):
        """Returns the Person at the index specified from a parameter."""
        try:
            return self.cell.read(lambda addressbook: self.addressbook.get_by_index(index))
        except:
            print("Error reading from addressbook. (get_by_index function)")
            self.cell.endRead()
            raise

    def get_by_name(self, namere):
        """Searches the addressbook with regexp with a pattern from a parameter."""
        try:
            return self.cell.read(lambda addressbook: self.addressbook.get_by_name(namere))
        except:
            print("Error reading from addressbook. (get_by_name function)")
            self.cell.endRead()
            raise

    def update(self, payload):
        """Update an entry in the addressbook."""
        try:
            return self.cell.write(lambda addressbook: self.addressbook.update(payload))
        except:
            print("Error writing to addressbook. (updte function)")
            self.cell.endWrite()
            raise

    def delete(self, payload):
        """Delete an entry in the addressbook."""
        try:
            return self.cell.write(lambda addressbook: self.addressbook.delete(payload))
        except:
            print("Error writing to addressbook. (delete function)")
            self.cell.endWrite()
            raise


class Addressbook(object):
    """The Addressbook class facilitates storage of individual Person objects."""

    def __init__(self):
        self.entries = []
        self.filename = ""

    def set_filename(self, filename):
        """Set the filename of the addressbook for later retrieval if necessary."""
        self.filename = filename

    def get_filename(self):
        """Returns the filename of the addressbook .csv that is loaded."""
        return self.filename

    def add(self, data):
        """Adds one to many People to the addressbook. This function expects a list of strings."""
        for entry in data:
            entry = entry.strip()  # Strip out any newlines if they exist
            attributes = entry.split(",")  # Split the entry into a list of attributes
            attributes = [a.strip() for a in attributes]  # Trim whitespace from each attribute
            new_entry = Person()
            new_entry.set(attributes)
            self.entries.append(new_entry)

    def get_by_index(self, index):
        """Returns the Person at the index specified from a parameter."""
        return self.entries[index].get()

    def get_by_name(self, namere):
        """Searches the addressbook with regexp with a pattern from a parameter."""
        result = []
        for entry in self.entries:
            if re.search(namere, str(entry), re.IGNORECASE):
                result.append(str(entry) + "\n")
        return result

    def update(self, payload):
        old = payload.split(":")[0]
        new = payload.split(":")[1]
        attributes = new.split(",")  # Split the entry into a list of attributes
        attributes = [a.strip() for a in attributes]  # Trim whitespace from each attribute
        for entry in self.entries:
            if re.search(old, str(entry)):
                entry.set(attributes)

    def delete(self, payload):
        for entry in self.entries:
            if re.search(payload, str(entry)):
                self.entries.remove(entry)

    def __str__(self):
        """Returns the addressbook with one person per line."""
        result = ""
        for person in self.entries:
            result += str(person) + "\n"
        return result


class Person:
    """Defines a Person object, consisting of 7 attributes."""

    def __init__(self):
        self.first = ""
        self.last = ""
        self.phone = ""
        self.street = ""
        self.city = ""
        self.state = ""
        self.zip = ""

    def set(self, attributes):
        """Sets the attributes from a list parameter"""
        self.first = attributes[0]
        self.last = attributes[1]
        self.phone = attributes[2]
        self.street = attributes[3]
        self.city = attributes[4]
        self.state = attributes[5]
        self.zip = attributes[6]

    def get(self):
        """Returns the person's attributes"""
        return self.first, self.last, self.phone, self.street, self.city, self.state, self.zip

    def __str__(self):
        """Returns the person's attributes as a comma-separated string"""
        return "%s, %s, %s, %s, %s, %s, %s" % (self.first, self.last, self.phone, self.street,
                                               self.city, self.state, self.zip)
