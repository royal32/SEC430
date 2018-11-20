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

    def add(self, first, last, phone, street, city, state, zip):

        self.entries.append(Person(first, last, phone, street, city, state, zip))

    def add(self, data):

        for i, entry in enumerate(data):
            entry = entry.rstrip("\n")
            attributes = entry.split(",")
            self.entries.append(Person())
            self.entries[i].add(attributes)
            # print(str(self.entries[i]))

    def get_by_index(self, index):
        return self.entries[index].get()

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


def main():
    """
        Testing function for PhoneBook.
        The main function is not meant to be called directly from the other programs
    """
    book = Addressbook()  # instantiate the phonebook class into a phonebook object
    for name in range(10):
        # This loop is for testing purpose
        # in actual phone book app, this main is not called
        #
        book.add("Name" + str(name), "524-4682")
    print(book)
    for name in range(10):
        print(book.get("Name" + str(name)))


if __name__ == "__main__":
    main()
