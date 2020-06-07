''' This program creates a class to store and alter book information'''
import sqlite3


class Book(object):
    def __init__(self, book_id, title, author, qty):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.qty = qty

    def __repr__(self):
        return '\nBook ID : ' + str(self.book_id) +\
               '\nTitle : ' + self.title +\
               '\nAuthor : ' + self.author +\
               '\nQuantity : ' + str(self.qty)


def enter_book(Book):
    '''  The enter_book function is used by the user to add
    a new book to the ebookstore from a book object
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    try:
        cursor.execute('''
            INSERT INTO books
                VALUES(?, ?, ?, ?)
            ''', (Book.book_id, Book.title, Book.author, Book.qty))
    except:
        db.rollback()
    finally:
        db.commit()
        db.close()


def update_book(Book):
    ''' The update_book function is used by the user to update a book record
    in the ebookstore using the book id with an updated Book object.
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    try:
        cursor.execute('''
            UPDATE books
                SET Title = ?, Author = ?, Qty = ?
                WHERE id = ?
            ''', (Book.title, Book.author, Book.qty, Book.book_id))
    except:
        db.rollback()
    finally:
        db.commit()
        db.close()


def delete_book(book_id):
    ''' The update_book function is used by the user to delete a book record
    from the ebookstore using the book ID number
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    try:
        cursor.execute('''
            DELETE FROM books
                WHERE id = ?
            ''', (book_id,))
    except:
        db.rollback()
    finally:
        db.commit()
        db.close()


def search_book_t(title):
    ''' The search_book_t function is used by the user to search for a book by it's title
    it's title & then  prints the query & returns a book object.
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    cursor.execute('''
           SELECT *
           FROM books
           WHERE Title = ?
           ''', (title,))
    bk_data = cursor.fetchall()
    db.close()
    outp = []
    for bk in bk_data:
        outp.append(Book(bk[0], bk[1], bk[2], bk[3]))
    return outp


def search_book_a(author):
    ''' The search_book_a function is used by the user to search for a book
    by it's author and then  prints the query and returns a book object.
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    cursor.execute('''
           SELECT *
           FROM books
           WHERE Author = ?
           ''', (author,))
    bk_data = cursor.fetchall()
    db.close()
    outp = []
    for bk in bk_data:
        outp.append(Book(bk[0], bk[1], bk[2], bk[3]))
    return outp


def return_book(book_id):
    ''' The return book function returns the book object when the book id is given
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    cursor.execute('''
           SELECT *
           FROM books
           WHERE id = ?
           ''', (book_id,))
    bk_data = cursor.fetchall()
    db.close()
    return Book(bk_data[0][0], bk_data[0][1], bk_data[0][2], bk_data[0][3])


def assign_id():
    ''' Finds the maximum number used as an ID in books
    in order to assign new book id numbers
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    cursor.execute('''
           SELECT MAX(id)
           FROM books
            ''')
    return (cursor.fetchall()[0][0]) + 1


def print_ebookstore():
    ''' Prints the entire book database
    '''
    db = sqlite3.connect('ebookstore')
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM books''')
    bk_data = cursor.fetchall()
    db.close()
    outp = []
    for bk in bk_data:
        outp.append(Book(bk[0], bk[1], bk[2], bk[3]))
    print(outp)

# Connection objects
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

# Database initialisation
opening_stock = [Book(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                 Book(3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
                 Book(3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
                 Book(3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                 Book(3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

try:  # Create table if does not exist
    cursor.execute('''
        CREATE TABLE books(
            id int PRIMARY KEY, Title varchar(40), Author varchar (40), Qty int
        )
    ''')
except:
    pass
finally:
    db.close()

# Create table with initial data
for book in opening_stock:
    enter_book(book)

Run = True  # Allows program to run while condition holds

while Run:
    invalid_option = True
    try:  # Gather user option skips procedure back to beginning if invalid input
        user_requirement = int(input('\nPlease select an option: 1 - Enter Book\n' +\
            '                         2 - Update Book\n' +\
            '                         3 - Delete Book\n' +\
            '                         4 - Search Books\n' +\
            '                         5 - Print Booklist\n' +\
            '                         0 - Exit                   -->  '))

        if user_requirement > 5 and user_requirement < 0:
            invalid_option = False
    except:
        invalid_option = False
    if invalid_option:
        if user_requirement == 1:  # Add new book
            try:
                title = input('Title of book  ')
                author = input('Author of book   ')
                qty = int(input('Quantity of book  '))
                add_book = Book(assign_id(), title, author, qty)
                enter_book(add_book)
                print(f'{add_book}\nhas been added.\n')
            except:
                print('Invalid input for entering a new book\n')
        elif user_requirement == 2:  # Update an existing book option
            try:
                book_id = input('Input the ID of the book to be updated  ')
                upd_Book = return_book(book_id)
                print(upd_Book)
                upd_title = input(f'Update title from {upd_Book.title} (P to pass)  ')
                if upd_title == 'P':
                    upd_title = upd_Book.title
                upd_author = input(f'Update author from {upd_Book.author} (P to pass)  ')
                if upd_author == 'P':
                    upd_author = upd_Book.author
                upd_quant = input(f'Update quantity from {upd_Book.qty} (P to pass)  ')
                if upd_quant == 'P':
                    upd_quant = upd_Book.qty
                else:
                    upd_quant = int(upd_quant)
                updated_Book = Book(upd_Book.book_id, upd_title, upd_author, upd_quant)
                update_book(updated_Book)
                print(f'{updated_Book}\nhas been updated.\n')
            except:
                print('Invalid input for update of book\n')

        elif user_requirement == 3:  # Delete book option
            try:
                del_book_id = input('Input the ID of the book to be deleted  ')
                delete_book(del_book_id)
                print(f'Book with ID {del_book_id} has been deleted.\n')
            except:
                print('Invalid input for deletion of book\n')
        elif user_requirement == 4:  # Search option
            try:
                search_books = input('Would you like to search by title? (Yes/No)  ')
                if search_books.title() == 'Yes':
                    search_title = input('Input the title of the book to be found  ')
                    sbook = search_book_t(search_title)
                    print(sbook)
                else:
                    search_author = input('Input the author of the book to be found  ')
                    sbook = search_book_a(search_author)
                    print(sbook)
            except:
                print('Book does not exist in database\n')

        elif user_requirement == 5:  # Print database option
            print_ebookstore()
        elif user_requirement == 0:  # Exit program option
            Run = False
        else:
            print('Invalid input, please enter again.\n')
