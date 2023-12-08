from library import LibraryDB, PubSub

class main_options:

    def customer(library_db, pubsub):
        while True:
            print("\nYou are in customer mode. What would you like to do ?")
            print("1. Get book information")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Subscribe to a channel")
            print("5. Unsubscribe to a channel")
            print("6. Retrieve news from subscribed channels")
            print("7. Return to the main menu")    
            
            choice_cust = input("Enter your choice: ")

            if choice_cust == "1":
                isbn = input("Please provide your isbn: ")
                retrieved_info = library_db.get_book(isbn)
            
                if retrieved_info:
                    print(f"   Information on your book (ISBN: {isbn}): \n     {retrieved_info['title']} by {retrieved_info['author']}, \n     Total number of copies left at the library: {retrieved_info['number of copies']}, \n     Futher information: Language = {retrieved_info['language']}, Genre = {retrieved_info['genre']}, Year of publication = {retrieved_info['publication year']}")
                else: 
                    print("Unfortunately, it seems this book does not exist in the National Library of Narnia.")

            
            elif choice_cust == "2":
                isbn = input("Please provide your isbn: ")
                library_db.borrow_book(isbn)
            
            elif choice_cust == "3":
                isbn = input("Please provide your isbn: ")
                library_db.return_book(isbn)

            elif choice_cust == "4":
                while True:
                    channel = input("You are about to subscribe to a channel. Please provide the channel you would like to subscribe to (can be an Author name, Language, Genre or Year of Publication). If you would like to cancel your subscription request, please write \"cancel\": ")
                    if channel.lower() == "cancel":
                        break
                    library_db.subscribe_channel(channel)
                    break

            elif choice_cust == "5":
                while True:
                    channel = input("You are about to unsubscribe from a channel. Please provide the channel you would like to unsubscribe from. If you would like to cancel your subscription request, please write \"cancel\": ")
                    if channel.lower() == "cancel":
                        break
                    library_db.unsubscribe_channel(channel)
                    break

            elif choice_cust == "6":
                pubsub.retrieve_news()

            elif choice_cust == "7":
                print("returning to main menu")
                break
            
            else: 
                print("Invalid choice. Please enter 1, 2, 3 or 4.")


    def librarian(library_db):
        while True:
            print("\nYou are in librarian mode. What would you like to do ?")
            print("1. Get book information")
            print("2. Add a book")
            print("3. Remove a book")
            print("4. Return to the main menu")    

            choice_lib = input("Enter your choice: ")

            if choice_lib == "1":
                isbn = input("Please provide your isbn: ")
                retrieved_info = library_db.get_book(isbn)
                if retrieved_info:
                    print(f"   Information on your book (ISBN: {isbn}): \n     {retrieved_info['title']} by {retrieved_info['author']}, \n     Total number of copies left at the library: {retrieved_info['number of copies']}, \n     Futher information: Language = {retrieved_info['language']}, Genre = {retrieved_info['genre']}, Year of publication = {retrieved_info['publication year']}")
                else:
                    print("Unfortunately, it seems this book does not exist in the National Library of Narnia.")
            
            elif choice_lib == "2":
                isbn = input("Please provide the isbn: ")
                
                if bool(library_db.get_book(isbn)):
                    print("This book already exists. Would you like to add or remove some copies ? ")
                    print("1. Add copies")
                    print("2. Remove copies")
                    print("3. Return to main menu")
                    choice_add_book = input("Enter your choice: ")

                    if choice_add_book == "1":
                        number_of_copies_to_add = input("How many copies would you like to add ? ")
                        library_db.add_copies(isbn, number_of_copies_to_add)

                    elif choice_add_book == "2":
                        number_of_copies_to_remove = input("How many copies would you like to remove ? ")
                        library_db.remove_copies(isbn, number_of_copies_to_remove)  
                    
                    elif choice_lib == "3":
                        print("returning to main menu")
                        break      

                    else:
                        print("Invalid choice. Please enter 1, 2, or 3.")
                    
                else:
                    title = input("Please provide the title: ")
                    author = input("Please provide the author: ")
                    number_of_copies = input("Please provide the number of copies: ")
                    language = input("Please provide the language of the book: ")
                    genre = input("Please provide the genre of the book: ")
                    publication_year = input("Please provide the year of publication of the book: ")
                    library_db.add_book(isbn, title, author, number_of_copies, language, genre, publication_year)                
            
            elif choice_lib == "3":
                isbn = input("Please provide your isbn: ")
                library_db.remove_book(isbn)

            elif choice_lib == "4":
                print("returning to main menu")
                break
            
            else: 
                print("Invalid choice. Please enter 1, 2, or 3.")


class main:

    pubsub = PubSub()
    lib = LibraryDB(pubsub)

    print("Welcome to the National Library of Narnia")

    while True:
        print("\nChoose an option:")
        print("1. Customer")
        print("2. Librarian")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            main_options.customer(lib, pubsub)
        elif choice == "2":
            main_options.librarian(lib)
        elif choice == "3":
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")