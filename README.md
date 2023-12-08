# Library-Redis
For this project, I was tasked with writing a toy application of a database of books that can be borrowed in a library. For this project, the Key-value store, Redis, was used. 

### Application specification
1. All books in the library database have an ISBN, a title, an author and a number of copies.
1. Books may also have other properties.
1. Create a publish-subscribe news system that:
- on the publisher side lets the user add a book to the library, indexes it by the keywords
in its description, publishes a channel for each indexed keyword, and emits a news message
containing the newly published book ID;
- on the subscriber side enables the user to subscribe to news channels matching certain keywords, retrieve a book from a news by the ID, and show the full book entry from the database;
separately the user can borrow or return a book: the system needs to check if the book is
available;
- makes books expire after a while (if no one borrows the book): these are no longer available
to borrow;
- if someone borrows a book (by, e.g., setting a certain field in the database), makes the book
refresh its expiry date.
