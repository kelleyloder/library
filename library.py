# Classes and methods for a simple library program
# Authors: Dave Matuszek and Kelley Loder and Nicki Hoffman
#--------------------------------------------------------------

class Calendar(object):
    """Keeps track of the current date (as an integer)."""

    def __init__(self):
        """Creates the initial calendar."""
        self.day = 0

    def get_date(self):
        """Returns (as a positive integer) the current date."""
        return self.day

    def advance(self):
        """Advances this calendar to the next date."""
        self.day += 1

#--------------------------------------------------------------

class Book(object):
    """Represents one copy of a book. There may be many copies
       of a book with the same title and author.
       Each book has:
         * An id (a unique integer)
         * A title
         * An author (one string, even if many authors)
         * A due date (or None if the book is not checked out.)."""

    def __init__(self, title, author):
        """Creates a book, not checked out to anyone."""
        self.title = title
        self.author = author
        self.due_date = None

    def get_title(self):
        """Returns the title of this book."""
        return self.title

    def get_author(self):
        """Returns the author(s) of this book, as a single string."""
        return self.author

    def get_due_date(self):
        """If this book is checked out, returns the date on
           which it is due, else returns None."""
        return self.due_date

    def check_out(self, due_date):
        """Sets the due date for this book."""
        self.due_date = due_date

    def check_in(self):
        """Clears the due date for this book (sets it to None)."""
        self.due_date = None

    def __str__(self):
        """Returns a string representation of this book,
        of the form: title, by author"""
        return "%s, by %s" % (self.title, self.author)

    def __eq__(self, other):
        """Tests if this book equals the given parameter. Not
        required by assignment, but fairly important."""
        return self.title == other.title and self.author == other.author

#--------------------------------------------------------------

class Patron(object):
    """Represents a patron of the library. A patron has:
         * A name
         * A set of books checked out"""

    def __init__(self, name):
        """Constructs a new patron, with no books checked out yet."""
        self.name = name
        self.checked_out = set()

    def get_name(self):
        """Returns this patron's name."""
        return self.name

    def get_books(self):
        """Returns the set of books checked out to this patron."""
        return self.checked_out

    def take(self, book):
        """Adds a book to the set of books checked out to this patron."""
        self.checked_out.add(book)

    def give_back(self, book):
        """Removes a book from the set of books checked out to this patron."""
        self.checked_out.discard(book)

    def __str__(self):
        """Returns the name of this patron."""
        return self.name

#--------------------------------------------------------------
    
class OverdueNotice(object):
    """Represents a message that will be sent to a patron."""

    def __init__(self, set_of_books):
        """Takes note of all the books checked out to some patron."""
        self.set_of_books = set_of_books

    def __str__(self):
        """From a set of books, returns a multi-line string giving
           the dates on which the books were or will be due.
           This should only be called when at least one of the books
           is overdue, but ALL the patron's books are listed, with
           their due dates, and the overdue ones specially marked."""
        notice = 'Patron has the following books checked out:\n'
        for book in self.set_of_books:
            if book.get_due_date() < calendar.get_date():
                notice += "%s which is overdue (was due on %d)\n" \
                          % (book, book.get_due_date())
            else:
                notice += "%s which is due on %d\n" % (book, book.get_due_date())
        return notice

#--------------------------------------------------------------

class Library(object):
    """Provides operations available to the librarian."""
    
    def __init__(self):
        """Constructs a library, which involves reading in a
           list of books that are in this library's collection."""
        
        # Create a global calendar, to be used by many classes
        global calendar
        calendar = Calendar()
        
        # Initialize some instance variables for _this_ library
        self.is_open = False            # Is library open?
        self.collection = []            # List of all Books
        self.patrons = {}            # Set of all Patrons
        self.patron_being_served = None # Current patron
        self.current_patrons_books = [] # books checked out by current patron
        self.found_books = set()

    def get_date(self):
        """Returns the current value of the global calendar -
        useful for unittests."""
        return calendar.get_date()
        
    def read_in_collection(self):
        # Read in the book collection
        file = open('collection.txt')
        for line in file:
            if len(line) > 1:
                tuple = eval(line.strip())
                self.collection.append(Book(tuple[0], tuple[1]))
        file.close()

    def set_collection(self, *list_of_books):
        for line in list_of_books:
            self.collection.append(Book(line[0], line[1]))        
    
    def open(self):
        """Opens this library for business at the start of a new day."""
        if self.is_open:
            return "The library is already open!"
        else:
            self.is_open = True
            calendar.advance()
            return "Today is day %d." % calendar.get_date()

    def list_overdue_books(self):
        """Checks records and prints overdue notices to all
           delinquent patrons who have an overdue book."""
        message = ''
        if self.is_open:
            for patron in self.patrons:
                for book in self.patrons[patron].get_books():
                    if book.get_due_date() < calendar.get_date():
                        message += self.patrons[patron].get_name() + '\n' + \
                                  OverdueNotice(self.patrons[patron].get_books()).__str__()
                        break
            if not message:
                message = "No books are overdue."
        else:
            message += "The library is not open."
        return message
                
    def issue_card(self, name_of_patron):
        """Allows the named person the use of this library. For
           convenience, immediately begins serving the new patron."""
        if self.is_open:
            if name_of_patron not in self.patrons:
                self.patrons[name_of_patron] = Patron(name_of_patron)
                message = "Library card issued to %s.\n" % name_of_patron
            else:
                message = "%s already has a library card.\n" % name_of_patron
            return message + self.serve(name_of_patron)
        else:
            return "The library is not open."

    def serve(self, name_of_patron):
        """Saves the given patron in an instance variable. Subsequent
           check_in and check_out operations will refer to this patron,
           so that the patron's name need not be entered many times."""
        message = ''
        if self.is_open:
            if name_of_patron in self.patrons:
                self.patron_being_served = self.patrons[name_of_patron]
                self.current_patrons_books = []
                message += "Now serving %s.\n" % name_of_patron
                if self.patron_being_served.get_books():
                    message += "%s has the following books checked out:\n" % name_of_patron
                    i = 1
                    for book in self.patron_being_served.get_books():
                        message += "%d. %s\n" % (i, book)
                        self.current_patrons_books.append(book)
                        i += 1
                else:
                    message += "%s has no books checked out." % name_of_patron
            else:
                message += "%s does not have a library card." % name_of_patron
        else:
            message += "The library is not open."
        return message
		
    def check_in(self, *book_numbers):
        """Accepts books being returned by the patron being served,
           and puts them back "on the shelf"."""
        message = ''
        if self.is_open:
            if self.patron_being_served:
                count = 0
                for book_number in book_numbers:
                    if book_number <= len(self.current_patrons_books):
                        book = self.current_patrons_books[book_number - 1]
                        self.patron_being_served.give_back(book)
                        book.check_in()
                        count += 1
                    else:
                        message += "The patron does not have book %d.\n" % book_number
                if count:
                    self.current_patrons_books = list(self.patron_being_served.get_books())
                    message += "%s has returned %d books." % \
                         (self.patron_being_served.get_name(), count)
            else:
                message += "No patron is currently being served."
        else:
            message += "The library is not open."
        return message

    def search(self, string):
        """Looks for books with the given string in either the
           title or the author's name, and creates a globally
           available numbered list in self.found_books."""
        if self.is_open:
            min_length = 4
            search_limit = 10
            self.found_books = []
            found_titles = set()
            if len(string) >= min_length:
                string = string.lower()
                for book in self.collection:
                    if (string in book.get_title().lower() or \
                        string in book.get_author().lower()) \
                       and not book.get_due_date() \
                       and not book.__str__() in found_titles:
                        self.found_books.append(book)
                        found_titles.add(book.__str__() + '\n')
                        if len(self.found_books) > search_limit:
                            break
                if found_titles:
                    return self.create_numbered_list(self.found_books)
                else:
                    return "No books found."
            else:
                return "Search string must contain at least four characters."
        else:
            return "The library is not open."

    def create_numbered_list(self, items):
        """Creates and returns a numbered list of the given items,
           as a multiline string. Returns "Nothing found." if the
           list of items is empty."""
        if self.is_open:
            i = 1
            numbered_list = ''
            for item in items:
                numbered_list += "%d. %s\n" % (i, item)
                i += 1
            if not numbered_list:
                return "Nothing found."
            return numbered_list.strip()
        else:
            return "The library is not open."

    def check_out(self, *book_numbers):
        """Checks books out to the patron currently being served.
           Books will be due seven days from "today".
           Patron must have a library card, and may have not more
           than three books checked out at a time."""
        message = ''
        if self.is_open:
            limit = 3
            checkout_period = 7
            if self.patron_being_served:
                count = 0
                for book_number in book_numbers:
                    if book_number <= len(self.found_books):
                        book = self.found_books[book_number - 1]
                        if len(self.patron_being_served.get_books()) < limit:
                            self.patron_being_served.take(book)
                            book.check_out(calendar.get_date() + checkout_period)
                            count += 1
                        else:
                            message += "%s already has the maximum # of books checked out.\n" % self.patron_being_served.get_name()
                            break
                    else:
                        message += "The library does not have book %d.\n" % book_number
                if count:
                    self.current_patrons_books = list(self.patron_being_served.get_books())
                    message += "%s has checked out %d books." % \
                         (self.patron_being_served.get_name(), count)
            else:
                message += "No patron is currently being served."
        else:
            message += "The library is not open."
        return message
            
    def renew(self, *book_ids):
        """Renews books for the patron currently being served.
        Books renewed will be due 7 days from "today"."""
        message = ''
        if self.is_open:
            if self.patron_being_served:
                count = 0
                checkout_period = 7
                for book_id in book_ids:
                    if book_id <= len(self.current_patrons_books):
                        book = self.current_patrons_books[book_id - 1]
                        book.check_out(calendar.get_date() + checkout_period)
                        count += 1
                    else:
                        message += "The patron does not have book %d." % book_id
                if count:
                    message += "%d books have been renewed for %s." % \
                         (count, self.patron_being_served.get_name())
            else:
                message += "No patron is currently being served."
        else:
            message += "The library is not open."
        return message
            
    def close(self):
        """Closes the library for the day."""
        if self.is_open:
            self.patron_being_served = None
            self.current_patrons_books = []
            self.is_open = False
            return "Good night."
        else:
            return "The library is not open."

    def quit(self):
        self.patron_being_served = None
        self.current_patrons_books = []
        self.is_open = False
        return "The library is now closed for renovations."

    def help(self):
         return """
help()
     Repeat this list of commands.
open()
     Opens the library for business; do this once each morning.
     
list_overdue_books()
     Prints out information about books due yesterday.
     
issue_card("name_of_patron")
     Allows the named person the use of the library.
     
serve("name_of_patron")
     Sets this patron to be the current patron being served.
     
search("string")
     Searches for any book or author containing this string
     and displays a numbered list of results.
     
check_out(books...)
     Checks out books (by number) to the current patron.
     
check_in(books...)
     Accepts returned books (by number) from the current patron.
     
close()
     Closes the library at the end of the day.

quit()
     Closes the library for good. Hope you never have to use this!"""

    # ----- Assorted helper methods (of Library) -----

    # Feel free to add any more helper methods you would like

#--------------------------------------------------------------

def main():
    library = Library()
    library.read_in_collection()
    print len(library.collection), 'books in collection.'
    print "Ready for input. Type 'help()' for a list of commands.\n"
    command = '\0'
    while command != 'quit()':
        try:
            command = raw_input('Library command: ').strip()
            if len(command) == 0:
                print "What? Speak up!\n"
            else:
                print eval('library.' + command)
        except AttributeError, e:
            print "Sorry, I didn't understand:", command
            print "Type 'help()' for a list of the things I do understand.\n"
        except Exception, e:
            print "Unexpected error:", e            
    
if __name__ == '__main__':
    main()
