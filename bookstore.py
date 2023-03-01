# the module is imported
# The programme makes use of sql. 
import sqlite3

# The function that initialises the contact with the data base and the creation of the table. 
def database_contact(): 
    
    # Defensive programming added here
    try: 
         # db is set.
        db = sqlite3.connect('ebookstore_db')
        cursor = db.cursor() 

        # The table columns are set using .execute. 
        # As per the Task pdf the correct formatting is used. 
        # I've added IF NOT EXISTS so there aren't any errors with the printing of results. 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS bookstock (
            ID int(4) UNIQUE,
            Title varchar(30),
            Author varchar(16),
            Qty int) ''')

        # The commit is made to update the changes
        db.commit()
    except Exception as e:
        db.rollback()
    
    return db, cursor

# This function is quite straightward, it adds the VALUES, so the book details as a bookstock table. 
# The cursor variable is initiated at the start of the programme and is important for the function
# The starting stock is loaded and committed to the database
def load_starting_stock(cursor):

    cursor.execute('''INSERT INTO bookstock
    VALUES  (3001, "The Tale of Two Cities", "Charles Dickens", 30),
            (3002, "Harry Potter and the Philosophers Stone", "J K Rowling", 40),
            (3003, "The Lion, The Witch, and the Wardrobe", "C S Lewis", 25), 
            (3004, "The Lord of the Rings", "JR R Tolkein", 37),
            (3005, "Alice in Wonderland", "Lewis Carrol", 12)''')
    
    #The results are committed so if you re-run the program the details are still there. 
    db.commit()
    
    pass

# A quick get type function so that all books can be displayed. 
# The books the the variable and result of a .fetchall. 
# A quick function which is used in the programme
# This function is also latent for potential increase of functionality
def all_books(cursor):
    cursor.execute('SELECT * FROM bookstock')
    books = cursor.fetchall()
    return books

# Some effieciency saving on the output.
# A for loop with a that has a print output. 
def book_details_by_id(id_num, result):
    
    for book in result:
        output = f"\n\tBook ID:\t {book[0]}\n"
        output += f"\tTitle:\t\t {book[1]}\n"
        output += f"\tAuthor:\t\t {book[2]}\n"
        output += f"\tQty in stock:\t {book[3]}\n"
        print(output)

    pass

# This function works with a few user options inluding delete. 
def search_books_by(cursor):

    while True: 
        
        # Some more defensive programming to assure against errors or bad entries. 
        try: 

            search_choice = int(input('''How would you like to search for the book(s)
                                (1) By book ID
                                (2) By book title
                                (3) By author
                                
                                :'''))
            if search_choice < 1 or search_choice > 3: 
                print("Please enter a valid choice")
            else:
                break
        except ValueError:
            print("Please enter a number")

    return search_choice

# Search ID does as suggested, it searches the ID of a book
# The setting of the user_search with different variables is important for other functions. 
def search_ID(cursor, books):

    while True: 
            try: 
                user_search = int(input("Please enter the ID of the book or type '0' to exit: "))                             
            except ValueError and UnboundLocalError: 
                print("Please enter a number")

            if user_search == 0:
                user_search = "Null"
                break
            else: 
                cursor.execute('SELECT * FROM bookstock WHERE ID = ?', (user_search,))
                result = cursor.fetchall() 
            
            if result is None: 
                print(f"ID number '{user_search}' is not in stock.")  
                user_search = "Null"               
            if len(result) == 0: 
                print(f"ID number '{user_search}' is not in stock.")
                user_search = "Null"
            else:
                book_details_by_id(user_search, result)
                break

    return user_search

# A function that searches by title. 
# There's some efficiency on the print out but otherwise different from other search functions in content. 
def search_title(cursor, books): 

    while True: 
            user_search = input("Please enter title of the book: ")
            cursor.execute('SELECT * FROM bookstock WHERE Title = ?', (user_search,))

            # Again .fetchall is used here set for a print output. 
            result = cursor.fetchall()

            if len(result) == 0: 
                print(f"Books of the title '{user_search}' are not in stock")
                user_search = "Null"
                break
            else:
                book_details_by_id(user_search, result)
                break

    return user_search

# I added search by author and search by title for delete function.
# So this function is worth having a modular as are the other two search functions. 
def search_author(cursor, books): 

    while True: 
            user_search = input("Please enter the name of the author: ")
            cursor.execute('SELECT * FROM bookstock WHERE Author = ?', (user_search,))

            result = cursor.fetchall()
            
            if len(result) == 0: 
                print(f"Books by author '{user_search}' are not in stock")
                user_search = "Null"
                break
            else:
                book_details_by_id(user_search, result)
                break

    return user_search 

# A view book function of if statements. 
# This function is used as a component, the search functions above are activated. 
def view_book(cursor, search_choice, books):

    if search_choice == 1:
        search_ID(cursor, books)                             
            
    if search_choice == 2:
        search_title(cursor, books)        

    if search_choice == 3:
        search_author(cursor, books)
        
    pass

# Because the delete confirmation is required in three instances this helps with efficiency. 
# Used in the delete_book() function. 
def delete_confirmation(search_result):
    if search_result == "Null":
        return None
    elif search_result != "Null":
        confirmation = input("Are you sure you would like to delete the title(s)? Y/N? ").capitalize()
        if confirmation == "N":
            print("\nOk, the main menu: ")
            return None
        elif confirmation == "Y": 
            return search_result

# Its worth noting that throughout cursor has been added to functions for .execution. 
# As beolow, search_id() and delete_confirmation functions are used in this function. 
# Again functionality and efficiency was aimed for. 
def delete_book(cursor, search_choice, books):
    if search_choice == 1:
        user_search = search_ID(cursor, books)
        delete_choice = delete_confirmation(user_search)
        
        cursor.execute('DELETE FROM bookstock WHERE ID = ?', (delete_choice,))
        db.commit()

    if search_choice == 2:
        user_search = search_title(cursor, books)
        delete_choice = delete_confirmation(user_search)
        
        cursor.execute('DELETE FROM bookstock WHERE Title = ?', (delete_choice,))
        db.commit()

    if search_choice == 3:
        user_search = search_author(cursor, books)
        delete_choice = delete_confirmation(user_search)
        
        cursor.execute('DELETE FROM bookstock WHERE Author = ?', (delete_choice,))
        db.commit()       

    pass
   

# This function includes a print for confirmation and of course the choice of what to edit. 
# The user is presented with extra options and the inputs are collected. 
def update_book_menu(cursor, books):
    while True:
        try:
            id = int(input("Please enter the ID of the book you would like to update: "))
            if id not in [book[0] for book in books]:
                print("That book ID hasn't been recognised")
                continue
            else: 
                if id in [book[0] for book in books]:                    
                    for book in books:                        
                        if id == book[0]:
                            output = f"\n\tBook ID:\t {book[0]}\n"
                            output += f"\tTitle:\t\t {book[1]}\n"
                            output += f"\tAuthor:\t\t {book[2]}\n"
                            output += f"\tQty in Stock:\t {book[3]}\n"
                            print(output)
                          

            edit_choice = int(input('''Would you like to: 
                                        (1) Edit the ID
                                        (2) Edit the QTY
                                        (3) Edit the author
                                        (4) Edit the title
                                        : '''))
            if edit_choice < 1 or edit_choice > 4:
                print("Please enter a valid choice")
                continue
            else: 
                update_book(cursor, id, edit_choice)
                break
        
        except ValueError:
            print("That's not a number")           
        
    pass

# This function makes use of .execute to change ID, QTY, Author and Title as chosen by the user. 
# Note the table and database is referred to as is consistent througout the programme. 
def update_book(cursor, id, edit_choice):

    if edit_choice == 1:
        new_id= input("Please enter the new ID of the book: ")
        cursor.execute('UPDATE bookstock SET ID = ? WHERE ID = ?', (new_id, id))
        db.commit()
    elif edit_choice == 2:
        new_qty = input("Please enter the new quantity of the book: ")
        cursor.execute('UPDATE bookstock SET Qty = ? WHERE ID = ?', (new_qty, id))
        db.commit()
    elif edit_choice == 3:
        new_auth = input("Please enter the new author of the book: ")
        cursor.execute('UPDATE bookstock SET Author = ? WHERE ID = ?', (new_auth, id))
        db.commit()
    elif edit_choice == 4: 
        new_title = input("Please enter the new title of the book: ")
        cursor.execute('UPDATE bookstock SET Title = ? WHERE ID = ?', (new_title, id))
        db.commit()
    else: 
        print("That's an invalid choice")

    pass

# The function for entering a new book the ID can't be repeated but title can
# Its possible that there might be two books of the same title. 
def enter_new_book(cursor, db, books):

    print("\nOk, you'll need to have the details handy: ")

    while True: 

        try: 
            id = int(input("\nPlease enter the ID of the book: "))
            if id in [book[0] for book in books]:
                print("That ID is already being used")
            if len(str(id)) != 4:
                print("Please enter a four digit number")
            else:
                break          
        except ValueError: 
            print("You need enter a four digit number.")

    while True:

        title = input("\nPlease enter the title of the book: ")
        if title in [book[1] for book in books]:
            print("That book title already exists")
        if len(title) <= 0: 
            print("Your didn't enter anything")           
        else: 
            print(f"The title you entered was {title}")
            break

    while True:

        author = input("\nPlease enter the name of the author: ")

        if len(title) <= 0: 
            print("You didn't enter anything")            
        else: 
            print(f"The author you entered was {author}")
            break

    while True:

        try:
            qty = int(input("Please enter the amount of the stock of the book: "))
            break
        except ValueError: 
            print("You didn't enter a number")

    cursor.execute(f'''INSERT INTO bookstock VALUES({id}, "{title}", "{author}", {qty})''')
    # Note the commit() which means newer versions of the database remain updated. 
    db.commit()           
        
    pass                              

# This initiates the program upon starting and setting the two most important variables
db, cursor = database_contact()

print('''\nDear Mentor / User, option 1 is only to get started, if you choose it twice it will double up on the data\n
            I added a small amount of functionality...''')

# The user is presented with their choices upon running the programme. 
while True:
    try:
        user_choice = int(input('''\nPlease choose from the following options

                            (1) To load the starting stock
                            (2) To enter a new book into stock
                            (3) To update a book in stock
                            (4) To delete a book from stock
                            (5) To search all books
                            (6) To view a list of all books in stock
                            (0) Exit

                            : '''))
           
        # There are the user's starting options. 
        # The functions are made use of. 
        if user_choice == 1:
            load_starting_stock(cursor)
            print("\nThat's been executed")
        elif user_choice == 2:
            books = all_books(cursor)
            enter_new_book(cursor, db, books)
        elif user_choice == 3:
            books = all_books(cursor)
            update_book_menu(cursor, books)
        elif user_choice == 4:
            print("\nSearch for the book you would like to delete.\n")
            books = all_books(cursor)
            search_choice = search_books_by(cursor)
            delete_book(cursor, search_choice, books)
        elif user_choice == 5:
            books = all_books(cursor)
            search_choice = search_books_by(cursor)
            view_book(cursor, search_choice, books)
        elif user_choice == 6: 
            books = all_books(cursor)
            for book in books:
                print(book)
        elif user_choice == 0:
            try: 
                db.close()
            except Exception as e:
                raise e
            exit()
        elif user_choice > 5 or user_choice < 0:
            print("Please enter a valid choice")
    except ValueError:
        print("\nThat wasn't a number")


# I tried to be as modular as possible with this and enjoyed adding functionality for current and future use. 
# Of course, I also used sql
# Code ends. 
