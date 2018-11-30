import re

class Addressbook(object):

    def __init__(self):
        self.entries = []
        self.filename = ""
        self.iter_current = 0

    def __iter__(self):
        """Makes object iterable"""
        return self

    def __next__(self):
        if self.iter_current >= len(self.entries):
            raise StopIteration
        else:
            print(self.iter_current)
            result = self.entries[self.iter_current]
            self.iter_current += 1
            return result

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def add(self, data):

        for i, entry in enumerate(data):
            entry = entry.rstrip("\n")
            attributes = entry.split(",")
            self.entries.append(Person())
            self.entries[i].add(attributes)

    def get_by_index(self, index):
        return self.entries[index].get()

    def get_by_name(self, namere):
        result = []
        for entry in self.entries:
            if re.search(namere, str(entry), re.IGNORECASE):
                 result.append(str(entry))
        return result


    def __str__(self):
        """Returns the string representation of the phone book."""
        result = ""
        for person in self.entries:
            result += str(person) + "\n"
        return result


class Person:

    def __init__(self):
        self.first = ""
        self.last = ""
        self.phone = ""
        self.street = ""
        self.city = ""
        self.state = ""
        self.zip = ""

    def add(self, attributes):
        self.first = attributes[0]
        self.last = attributes[1]
        self.phone = attributes[2]
        self.street = attributes[3]
        self.city = attributes[4]
        self.state = attributes[5]
        self.zip = attributes[6]

    def get(self):
        return self.first, self.last, self.phone, self.street, self.city, self.state, self.zip

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.first, self.last, self.phone, self.street,
                                               self.city, self.state, self.zip)

