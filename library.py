import redis

class LibraryDB:
    def __init__(self, pubsub):
        """Constructor"""
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.pubsub = pubsub


    def add_book(self, isbn, title, author, number_of_copies, language, genre, publication_year):
        """Add a new book to db"""

        book_key = f"book:{isbn}"
        
        book_value = {
            "title": title,
            "author": author,
            "number of copies": number_of_copies,
            "language": language, 
            "genre": genre,
            "publication year": publication_year
        }
        
        self.redis_client.hset(book_key, mapping = book_value)

        # Giving all books a TTL of 5 minutes
        self.redis_client.expire(book_key, 300)

        # Publish book to channel (see class PubSub below)
        keywords = [author, language, genre, publication_year]
        for channel in keywords:
            self.pubsub.publish_to_channel(channel, f"New book published! Borrow {title}, by {author} while copies still are available ! ISBN: {isbn}.")

        print(f"The book {isbn} has successfully been added to the library.")
        return 1
    

    def remove_book(self, isbn):
        """Remove a book from the database"""
        book_key = f"book:{isbn}"

        if len(self.redis_client.hgetall(book_key)) > 0:

            # Preparing to publish to all the channels this book belonged to. 
            author = self.redis_client.hget(book_key, "author")
            language = self.redis_client.hget(book_key, "language")
            genre = self.redis_client.hget(book_key, "genre")
            publication_year = self.redis_client.hget(book_key, "publication year")
            title = self.redis_client.hget(book_key, "title")
            channels_to_remove = [author, language, genre, publication_year]
            
            # Removing the book 
            self.redis_client.delete(book_key)

            # Publishing to channels
            for channel in channels_to_remove:
                message = f"The book, {title} by {author} has been removed. ISBN: {isbn}."
                self.pubsub.publish_to_channel(channel, message)

            print(f"The book {isbn} has successfully been removed from the library.")
            return 1
        
        else:
            print(f"No book with ISBN {isbn} has been found. Transaction failed.")
            return 0


    def add_copies(self, isbn, number_of_copies_to_add):

        book_key = f"book:{isbn}"
        number_of_copies_left = self.redis_client.hget(book_key, "number of copies")

        self.redis_client.hset(book_key, "number of copies", int(number_of_copies_left)+int(number_of_copies_to_add))

        print(f"You have successfully added {number_of_copies_to_add} copies to the book: {isbn}")
        return 1


    def remove_copies(self, isbn, number_of_copies_to_remove):

        book_key = f"book:{isbn}"
        number_of_copies_left = self.redis_client.hget(book_key, "number of copies")

        if number_of_copies_left - number_of_copies_to_remove >= 0:
            self.redis_client.hset(book_key, "number of copies", int(number_of_copies_left)-int(number_of_copies_to_remove))
            print(f"You have successfully removed {number_of_copies_to_remove} copies to the book: {isbn}")
            return 1

        else:
            print(f"Transaction failed: You can maximally remove {number_of_copies_left} copies!")
            return 0
        
    
    def get_book(self, isbn):
        """Get book from db"""
        
        book_key = f"book:{isbn}"

        if len(self.redis_client.hgetall(book_key)) > 0:
            all_info = self.redis_client.hgetall(book_key)
            return all_info
        else:
            return 0
    

    def borrow_book(self, isbn):
        """borrow a book from the library"""

        book_key = f"book:{isbn}"
        number_of_copies_left = self.redis_client.hget(book_key, "number of copies")

        if number_of_copies_left and int(number_of_copies_left) > 0:
            self.redis_client.hset(book_key, "number of copies", int(number_of_copies_left)-1)

            # Reset the expiration of the book to the original 5 minutes. 
            self.redis_client.expire(book_key, 300)

            print(f"Congratulations ! You successfully borrowed {isbn}.")
            return 1

        else:
            print(f"Unfortunately there are not enough copies of {isbn} to complete the task.")
            return 0
        
        
    def return_book(self, isbn):
        """return a book to the library"""

        book_key = f"book:{isbn}"

        self.redis_client.hset(book_key, "number of copies", int(self.redis_client.hget(book_key, "number of copies"))+1)

        print(f"Thank you for returning the book {isbn}")
        return 1
    

    def subscribe_channel(self, channel):
        """Subscribe to news channels matching certain keywords"""
        self.pubsub.subscribe_to_channel(channel)
        print("Subscription successful !")
        return 1


    def unsubscribe_channel(self, channel):
        """Unsubscribe from a news channel"""
        self.pubsub.unsubscribe_from_channel(channel)
        print("Unsubscription successful !")
        return 1




class PubSub:

    def __init__(self):
        """Constructor"""
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()

    def publish_to_channel(self, channel, message):
        """Publish news to a specific channel"""
        self.redis_client.publish(channel, message)

    def subscribe_to_channel(self, channel):
        """Subscribe to news channels matching certain keywords"""
        self.pubsub.subscribe(channel)
        return self.pubsub
    
    def unsubscribe_from_channel(self, channel):
        """Unsubscribe from a news channel"""
        self.pubsub.unsubscribe(channel)

    def retrieve_news(self):
        """Retrieve news messages from subscribed channels"""
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                print(f"{message['data']}")
                
