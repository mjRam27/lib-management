"""A simple library management system using basic Python concepts."""


class Book:
    def __init__(self, book_id, title, author):
        self.id = book_id
        self.title = title
        self.author = author
        self.available = True

    def borrow(self):
        if self.available:
            self.available = False
            return True
        return False

    def return_book(self):
        self.available = True


def display_books(books):
    """Display all books in the library."""
    if len(books) == 0:
        print("\nNo books are available.")
        return

    print("\nLibrary books:")
    for book in books:
        status = "Available" if book.available else "Borrowed"
        print(
            f"ID: {book.id} | Title: {book.title} | "
            f"Author: {book.author} | Status: {status}"
        )


def add_book(books, next_id):
    """Add a new book and return the next available ID."""
    title = input("Enter the book title: ").strip()
    author = input("Enter the author name: ").strip()

    if title == "" or author == "":
        print("Title and author cannot be empty.")
        return next_id

    books.append(Book(next_id, title, author))
    print("Book added successfully.")
    return next_id + 1


def find_book(books, book_id):
    """Find a book by its ID."""
    for book in books:
        if book.id == book_id:
            return book
    return None


def borrow_book(books):
    """Borrow an available book."""
    try:
        book_id = int(input("Enter the book ID to borrow: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    book = find_book(books, book_id)
    if book is None:
        print("Book not found.")
    elif not book.borrow():
        print("That book is already borrowed.")
    else:
        print("Book borrowed successfully.")


def return_book(books):
    """Return a borrowed book."""
    try:
        book_id = int(input("Enter the book ID to return: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    book = find_book(books, book_id)
    if book is None:
        print("Book not found.")
    elif book.available:
        print("That book is already available.")
    else:
        book.return_book()
        print("Book returned successfully.")


def search_books(books):
    """Search for books by title or author."""
    search_text = input("Enter a title or author to search: ").strip().lower()
    matching_books = []

    for book in books:
        if (
            search_text in book.title.lower()
            or search_text in book.author.lower()
        ):
            matching_books.append(book)

    if len(matching_books) == 0:
        print("No matching books found.")
    else:
        display_books(matching_books)


def show_menu():
    """Display the main menu."""
    print("\n--- Library Management System ---")
    print("1. Display all books")
    print("2. Add a book")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. Search for a book")
    print("6. Exit")


def main():
    """Run the library management system."""
    books = [
        Book(1, "The Hobbit", "J.R.R. Tolkien"),
        Book(2, "1984", "George Orwell"),
    ]
    next_id = 3

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_books(books)
        elif choice == "2":
            next_id = add_book(books, next_id)
        elif choice == "3":
            borrow_book(books)
        elif choice == "4":
            return_book(books)
        elif choice == "5":
            search_books(books)
        elif choice == "6":
            print("Thank you for using the library system.")
            break
        else:
            print("Invalid choice. Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()
