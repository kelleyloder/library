# Unit tests for a simple library program
# Authors: Dave Matuszek and Kelley Loder and Nicki Hoffman
#--------------------------------------------------------------
import unittest
from library import *

lib = Library()
lib.open()

class CalendarTest(unittest.TestCase):

    def test_calendar(self):
        cal = Calendar()
        self.assertEqual(0, cal.get_date())
        cal.advance()
        self.assertEqual(1, cal.get_date())

class BookTest(unittest.TestCase):

    def setUp(self):
        global book1, book2, book3, book4
        book1 = Book("Contact", "Carl Sagan")
        book2 = Book("The Count of Monte Cristo", "Alexandre Dumas")
        book3 = Book("The Lord of the Rings", "JRR Tolkien")
        book4 = Book("The Jungle", "Upton Sinclair")
        self.assertTrue(type(book1) is Book)
        self.assertTrue(type(book2) is Book)
        self.assertFalse(type(book3) is Calendar)
        self.assertFalse(type(book4) is Patron)

    def test_get_title(self):
        self.assertEqual("Contact", book1.get_title())
        self.assertEqual("The Lord of the Rings", book3.get_title())

    def test_get_author(self):
        self.assertEqual("Carl Sagan", book1.get_author())
        self.assertEqual("Alexandre Dumas", book2.get_author())

    def test_get_due_date(self):
        self.assertEqual(None, book1.get_due_date())

    def test_book_check_out_and_check_in(self):
        lib.serve("Amy Gutmann")
        book1.check_out(17)
        self.assertEqual(17, book1.get_due_date())
        book1.check_in()
        self.assertEqual(None, book1.get_due_date())
        book2.check_out(20)
        self.assertEqual(20, book2.get_due_date())

class PatronTest(unittest.TestCase):
    def setUp(self):
        global patron1, patron2, patron3
        patron1 = Patron("Amy Gutmann")
        patron2 = Patron("Dr. Dave")
        patron3 = Patron("Miley Cyrus")
        
    def test_get_name(self):
        self.assertEquals("Amy Gutmann", patron1.get_name())
        self.assertEquals("Dr. Dave", patron2.get_name())
        self.assertEquals("Miley Cyrus", patron3.get_name())

    def test_get_books_and_take_and_give_back(self):
        self.assertEquals(set([]), patron1.get_books())
        patron1.take(book1)
        self.assertEquals(set([book1]), patron1.get_books())
        patron1.give_back(book1)
        self.assertEquals(set([]), patron1.get_books())
        patron1.take(book2)
        patron1.take(book3)
        self.assertEquals(set([book2, book3]), patron1.get_books())
        self.assertEquals(set([]), patron2.get_books())
        patron2.take(book2)
        self.assertEquals(set([book2]), patron2.get_books())

class LibraryTest(unittest.TestCase):

    def setUp(self):
        lib = Library()
        lib.open()
        global book1, book2, book3, book4
        book1 = ("Contact", "Carl Sagan")
        book2 = ("C0ntact", "Carl Sagan")
        book3 = ("C01ntact", "Carl Sagan")
        book4 = ("C02ntact", "Carl Sagan")
        lib.set_collection(book1, book2, book3, book4)

    def test_get_date(self):
        self.assertEqual(1, lib.get_date())
        lib.close()
        lib.open()
        self.assertEqual(2, lib.get_date())

    def test_open_and_close(self):
        self.assertEqual("The library is already open!", lib.open())
        self.assertEqual("Good night.", lib.close())
        self.assertEqual("The library is not open.", lib.close())
        self.assertEqual("Today is day 2.", lib.open())

    def test_issue_card(self):
        lib.close()
        self.assertEqual("The library is not open.", lib.issue_card("Dave"))
        lib.open()
        self.assertEqual("Library card issued to Dave.\nNow serving Dave.\n" +\
                         "Dave has no books checked out.",
                         lib.issue_card("Dave"))
        self.assertEqual("Dave already has a library card.\n" +\
                         "Now serving Dave.\nDave has no books checked out.",
                         lib.issue_card("Dave"))

    def test_serve(self):
        lib.close()
        self.assertEqual("The library is not open.", lib.serve("Someone"))
        lib.open()
        lib.issue_card("Sam")
        self.assertEqual("Now serving Sam.\nSam has no books checked out.", \
                         lib.serve("Sam"))
        self.assertEqual("Sam", lib.patron_being_served.get_name())
        self.assertEqual("Randall does not have a library card.",
                         lib.serve("Randall"))
        
    def test_search(self):
        lib.collection = []
        lib.set_collection(book1, book2, book3, book4)
        lib.close()
        self.assertEqual("The library is not open.", lib.search("aaa"))
        lib.open()
        self.assertEqual("Search string must contain at least four characters.",
                         lib.search("aaa"))
        self.assertEqual("No books found.", lib.search("xkcd"))
        self.assertEqual("1. Contact, by Carl Sagan", lib.search("contact"))
        self.assertEqual("1. Contact, by Carl Sagan\n" +\
                         "2. C0ntact, by Carl Sagan\n" +\
                         "3. C01ntact, by Carl Sagan\n" +\
                         "4. C02ntact, by Carl Sagan",
                         lib.search("sagan"))

    def test_check_in_and_check_out(self):
        lib.collection = []
        lib.set_collection(book1, book2, book3, book4)
        lib.close()
        self.assertEqual("The library is not open.", lib.check_in(1))
        self.assertEqual("The library is not open.", lib.check_out(1))
        lib.open()
        self.assertEqual("No patron is currently being served.", lib.check_in(1))
        self.assertEqual("No patron is currently being served.", lib.check_out(1))
        lib.issue_card("Vimes")
        self.assertEqual("The patron does not have book 1.\n", lib.check_in(1))
        lib.search("sagan")
        self.assertEqual("The library does not have book 5.\n", lib.check_out(5))
        self.assertEqual("Vimes already has the maximum # of books checked out.\n" +\
                         "Vimes has checked out 3 books.",
                         lib.check_out(1, 2, 3, 4))
        self.assertEqual("Vimes has returned 3 books.",
                         lib.check_in(1, 2, 3))
        
    def test_list_overdue_books(self):
        lib.collection = []
        lib.set_collection(book1, book2, book3, book4)
        lib.close()
        self.assertEqual("The library is not open.", lib.list_overdue_books())
        lib.open()
        self.assertEqual("No books are overdue.", lib.list_overdue_books())
        lib.issue_card("Errol")
        lib.search("sagan")
        lib.check_out(1)
        self.assertEqual("No books are overdue.", lib.list_overdue_books())
        for i in range(8):
            lib.close()
            lib.open()
        self.assertEqual("Errol\nPatron has the following books checked " +\
                         "out:\nContact, by Carl Sagan which is overdue " +\
                         "(was due on 9)\n", lib.list_overdue_books())
        
    def test_create_numbered_list(self):
        ul = []
        self.assertEqual("Nothing found.", lib.create_numbered_list(ul))
        ul = ["a thing", "another thing"]
        self.assertEqual("1. a thing\n2. another thing",
                         lib.create_numbered_list(ul))

    def test_renew(self):
        lib.set_collection(book1, book2, book3, book4)
        lib.close()
        self.assertEquals('The library is not open.', lib.renew(1))
        lib.open()
        self.assertEquals('No patron is currently being served.', lib.renew(1))
        lib.issue_card('Dr. Dave')
        self.assertEquals('The patron does not have book 1.', lib.renew(1))
        lib.search('contact')
        lib.check_out(1)
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.serve('Dr. Dave')
        self.assertEquals('1 books have been renewed for Dr. Dave.', lib.renew(1))
        self.assertEquals(lib.get_date() + 7, lib.current_patrons_books[0].get_due_date())
        
    def test_quit(self):
        lib.close()
        self.assertEquals('The library is now closed for renovations.', lib.quit())



unittest.main()
