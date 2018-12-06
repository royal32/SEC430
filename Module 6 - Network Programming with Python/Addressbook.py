import re


class Addressbook(object):
    """The Addressbook class facilitates storage of individual Person objects."""
    def __init__(self):
        self.entries = []
        self.filename = ""
        self.iter_current = 0

    def __iter__(self):
        """Declares that this class is iterable."""
        return self

    def __next__(self):
        """Facilitates iteration through the addressbook."""
        if self.iter_current >= len(self.entries): # Stop condition
            raise StopIteration
        else:
            result = self.entries[self.iter_current]
            self.iter_current += 1
            return result

    def iter_reset(self):
        """Keeps track of the current index while iterating through the addressbook."""
        self.iter_current = 0

    def set_filename(self, filename):
        """Set the filename of the addressbook for later retrieval if necessary."""
        self.filename = filename

    def get_filename(self):
        """Returns the filename of the addressbook .csv that is loaded."""
        return self.filename

    def add(self, data):
        """Adds one to many People to the addressbook."""
        for entry in data:
            entry = entry.rstrip("\n") # Strip out any newlines if they exist
            attributes = entry.rsplit(",") # Split the entry into a list of attributes
            new_entry = Person()
            new_entry.add(attributes)
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

    def add(self, attributes):
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
