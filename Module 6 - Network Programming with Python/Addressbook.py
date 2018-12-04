import re


class Addressbook(object):
    # Initializes the entries, filename, and the current level of iterartion
    def __init__(self):
        self.entries = []
        self.filename = ""
        self.iter_current = 0

    def __iter__(self):
        # Enables iteration of the object
        return self

    def __next__(self):
        # Ends iteration once it reaches the end point
        if self.iter_current >= len(self.entries):
            raise StopIteration
        # Iterates through the entries
        else:
            print(self.iter_current)
            result = self.entries[self.iter_current]
            self.iter_current += 1
            return result
        # Defines file name

    def set_filename(self, filename):
        self.filename = filename
        # Gets and returns file name

    def get_filename(self):
        return self.filename

    def add(self, data):
        # combines the data and adds delimination
        if type(data) is list:
            for entry in data:
                entry = entry.rstrip("\n")
                attributes = entry.rsplit(",")
                new_entry = Person()
                new_entry.add(attributes)
                self.entries.append(new_entry)
        else:
            attributes = data.rsplit(",")
            new_entry = Person()
            new_entry.add(attributes)
            self.entries.append(new_entry)

    def get_by_index(self, index):
        return self.entries[index].get()
        # Allows a search of the names and returns the result

    def get_by_name(self, namere):
        result = []
        for entry in self.entries:
            if re.search(namere, str(entry), re.IGNORECASE):
                result.append(str(entry))
        return result

    def __str__(self):
        # Returns the address data as a string.
        result = ""
        for person in self.entries:
            result += str(person) + "\n"
        return result


class Person:
    # Defines person object as consisting of seven data types per person
    def __init__(self):
        self.first = ""
        self.last = ""
        self.phone = ""
        self.street = ""
        self.city = ""
        self.state = ""
        self.zip = ""

        # Assigns attributes to each person object

    def add(self, attributes):
        self.first = attributes[0]
        self.last = attributes[1]
        self.phone = attributes[2]
        self.street = attributes[3]
        self.city = attributes[4]
        self.state = attributes[5]
        self.zip = attributes[6]
        # Returns the parts of the person object

    def get(self):
        return self.first, self.last, self.phone, self.street, self.city, self.state, self.zip
        # String formatting

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.first, self.last, self.phone, self.street,
                                               self.city, self.state, self.zip)
