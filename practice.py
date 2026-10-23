# # # # book_title = "clean code"
# # # # copies = 3
# # # # price = 29.99
# # # # available = True 

# # # # print(book_title)

# # # # copies = 3
# # # # copies = copies - 1

# # # # print(copies)

# # # # books = [
# # # #     "clean code",
# # # #     "design patterns",
# # # #     "refactoring",
# # # # ]

# # # # # print(books[1]) 

# # # # books.append("the pragmatic programmer") 
# # # # books.remove("refactoring")
# # # # print(books)
# # # # print(len(books))

# # # # book = {
# # # #     "title": "clean code",
# # # #     "copies": 3,
# # # #     "price": 29.99,
# # # #     "available": True   

# # # # }

# # # # print(book["title"])

# # # # // lists and dictionaries are used to store multiple values in a single variable. Lists are ordered collections of items, while dictionaries are unordered collections of key-value pairs.

# # # books = [
# # #     {
# # #         "title": "clean code",
# # #         "copies": 3,
# # #         "price": 29.99,
# # #         "available": True
# # #     },
# # #     {
# # #         "title": "design patterns",
# # #         "copies": 2,
# # #         "price": 39.99,
# # #         "available": True
# # #     },
# # #     {
# # #         "title": "refactoring",
# # #         "copies": 1,
# # #         "price": 49.99,
# # #         "available": True
# # #     }
# # # ]


# # # print(books[1]["title"])  # Accessing the title of the second book in the list


# # #conditional statements

# # # copies = 3
# # # if copies > 0:
# # #     print("There are books available.")
# # # elif copies == 0:
# # #     print("No copies available.")   
# # # else:
# # #     print("Invalid number of copies.")

# # # not 

# # # available = False

# # # if not available:
# # #     print("The book is not available.")


# # #loops

# # books = ["the pragmatic programmer", "clean code", "design patterns"]

# # for book in books:
# #     print(book)

# while True:
#     print("1. Display books")
#     print("2. Exit")

#     choice = input("Choose an option: ")

#     if choice == "2":
#         print("Goodbye!")
#         break

#     print("You selected:", choice)

# # functions


# def example():
#     for number in range(5):
#         if number == 2:
#             break
#         print(number)

#     print("Loop ended.")

# example()

def calculate_late_fee(days):
    fee = days *0.50
    return fee

result = calculate_late_fee(5)
print(result) 

#