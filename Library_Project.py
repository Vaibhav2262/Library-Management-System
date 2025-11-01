from datetime import datetime, timedelta

# ------------ B O O K - C L A S S ---------------
class Book:
    def __init__(self, book_title, book_author, publish_year, available_copies):
        self.title = book_title
        self.author = book_author
        self.year = publish_year
        self.total_copies = available_copies  # Total copies in the library
        self.available_copies = available_copies  # Copies currently available for issue
        self.issued = []  # List to track which student has issued the book

# ------------ L I B R A R Y - C L A S S ---------------
class Library:
    def __init__(self):
        self.books = []  # List to store all books

    # ----------- A D D - B O O K S---------------
    def add_book(self, title, author, year, copies):
        new_book = Book(title, author, year, copies)  # Create a new Book object
        self.books.append(new_book)  # Add it to the library list
        print(f"Book '{title}' added successfully!")
        self.save_books()  # Save the updated library to file

    # ----------- D  E L E T E - B O O K S---------------
    def delete_book(self, index):
        try:
            book = self.books.pop(index)  # Remove the book from the list
            print(f"Book '{book.title}' deleted successfully!")
            self.save_books()
        except IndexError:
            print("Invalid index! Cannot delete.")  # Error if index is out of range
        except Exception as e:
            print(f"Error while deleting book: {e}")

    # ----------- U P D A T E - B O O K S---------------
    def update_book(self, index):
        try:
            book = self.books[index]  # Get the book using index
            print(f"\nSelected Book: {book.title} by {book.author} ({book.year})")
            print("Press Enter to skip a field.")  # Optional: skip by pressing Enter

            # Update title if input is not empty
            new_title = input("Enter new title: ")
            if new_title:
                book.title = new_title

            # Update author if input is not empty
            new_author = input("Enter new author: ")
            if new_author:
                book.author = new_author

            # Update year if input is numeric
            new_year = input("Enter new year: ")
            if new_year.isdigit():
                book.year = int(new_year)

            # Update available copies if numeric, and adjust total copies
            new_copies = input("Enter new available copies: ")
            if new_copies.isdigit():
                diff = int(new_copies) - book.available_copies
                book.available_copies = int(new_copies)
                book.total_copies += diff  # Adjust total copies if required

            print("Book updated successfully!")
            self.save_books()
        except IndexError:
            print("Invalid index! Please select a correct book number.")
        except Exception as e:
            print(f"Error updating book: {e}")

    # ----------- V I E W - B O O K S---------------
    def view_books(self):
        try:
            if not self.books:  # No books in library
                print("No books available in the library.")
                return
            # Display all books with index, title, author, year, total, and available
            for i, book in enumerate(self.books):
                print(f"{i+1}. {book.title} by {book.author} ({book.year}) - "  
                      f"Total: {book.total_copies}, Available: {book.available_copies}")
        except Exception as e:
            print(f"Error displaying books: {e}")

    # ----------- I S S U E - B O O K S---------------
    def issue_book(self, index, student_name):
        try:
            book = self.books[index]
            if book.available_copies > 0:
                issue_date = datetime.now().strftime("%Y-%m-%d")  # Today's date
                return_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")  # Return after 7 days
                book.issued.append({
                    "student": student_name,
                    "issue_date": issue_date,
                    "return_date": return_date
                })
                book.available_copies -= 1  # Reduce available copies
                print(f"Book '{book.title}' issued to {student_name}. Return by {return_date}")
                self.save_books()
                self.save_issued()
            else:
                print(f"No available copies of '{book.title}'.")
        except IndexError:
            print("Invalid index! Cannot issue.")  # If index is out of range
        except Exception as e:
            print(f"Error while issuing book: {e}")

    # ----------- R E T U R N - B O O K S---------------
    def return_book(self, index, student_name):
        try:
            book = self.books[index]
            for record in book.issued:
                if record["student"].lower() == student_name.lower():  # Match student
                    return_date = datetime.strptime(record["return_date"], "%Y-%m-%d")
                    today = datetime.now()
                    days_late = (today - return_date).days
                    if days_late > 0:
                        charge = days_late * 100  # Rs 100 per day late fee
                        print(f"Late return! {days_late} day(s) late. Charge: Rs {charge}")
                    book.issued.remove(record)  # Remove record from issued list
                    book.available_copies += 1  # Increase available copies
                    print(f"Book '{book.title}' returned by {student_name}.")
                    self.save_books()
                    self.save_issued()
                    return
            print(f"No record found for {student_name} with book '{book.title}'.")
        except IndexError:
            print("Invalid index! Cannot return.")  # Index out of range
        except Exception as e:
            print(f"Error while returning book: {e}")

    # ----------- V I E W - I S S U E D - B O O K S---------------
    def view_issued_books(self):
        try:
            found = False
            for book in self.books:
                for record in book.issued:
                    print(f"{book.title} issued to {record['student']} | "
                          f"Issue Date: {record['issue_date']} | Return Date: {record['return_date']}")
                    found = True
            if not found:
                print("No issued books found.")
        except Exception as e:
            print(f"Error displaying issued books: {e}")

    # ----------- S A V E  - B O O K S---------------
    def save_books(self, filename="books.txt"):
        try:
            with open(filename, "w") as f:
                for book in self.books:
                    f.write(f"{book.title}|{book.author}|{book.year}|{book.total_copies}|{book.available_copies}\n")
        except Exception as e:
            print(f"Error while saving books: {e}")

    # ----------- L O A D - B O O K S---------------
    def load_books(self, filename="books.txt"):
        try:
            with open(filename, "r") as f:
                for line in f:
                    title, author, year, total, available = line.strip().split("|")
                    self.add_book(title, author, int(year), int(total))
                    self.books[-1].available_copies = int(available)
        except FileNotFoundError:
            print("No previous book data found. Starting fresh.")
        except Exception as e:
            print(f"Error while loading books: {e}")

    # ----------- S A V E - I S S U E D - B O O K S---------------
    def save_issued(self, filename="issued.txt"):
        try:
            with open(filename, "w") as f:
                for book in self.books:
                    for record in book.issued:
                        f.write(f"{book.title}|{record['student']}|{record['issue_date']}|{record['return_date']}\n")
        except Exception as e:
            print(f"Error while saving issued data: {e}")

    # -----------L O A D - I S S U E D - B O O K S---------------
    def load_issued(self, filename="issued.txt"):
        try:
            with open(filename, "r") as f:
                for line in f:
                    title, student, issue_date, return_date = line.strip().split("|")
                    for book in self.books:
                        if book.title.lower() == title.lower():
                            book.issued.append({
                                "student": student,
                                "issue_date": issue_date,
                                "return_date": return_date
                            })
        except FileNotFoundError:
            print("No previous issued data found. Starting fresh.")
        except Exception as e:
            print(f"Error while loading issued data: {e}")



# ------------ M A I N - P R O G R A M ---------------
if __name__ == "__main__":
    lib = Library()

    # Load existing books and issued records
    lib.load_books()
    lib.load_issued()

    # Preload 5 books only if they are not already in library
    preloaded_books = [
        ("Python Basics", "Author A", 2020, 3),
        ("Django Guide", "Author B", 2021, 3),
        ("SQL Mastery", "Author C", 2019, 3),
        ("Data Science", "Author D", 2022, 3),
        ("AI Fundamentals", "Author E", 2023, 3)
    ]
    existing_titles = [book.title for book in lib.books]
    for title, author, year, copies in preloaded_books:
        if title not in existing_titles:
            lib.add_book(title, author, year, copies)

    # ------------------- U S E R - Selection -------------------
    while True:
        print("\n--- S E L E C T - U S E R ---")
        print("1. Owner")
        print("2. Student")
        print("3. Exit")
        user_choice = input("Enter Your Choice : ")

        # -------------------O W N E R - M E N U -------------------
        if user_choice == "1":
            while True:
                print("\n--- O W N E R - M E N U ---")
                print("1. Add Book")
                print("2. Delete Book")
                print("3. Update Book")
                print("4. View Books")
                print("5. View Issued Books")
                print("6. Exit")
                owner_choice = input("Enter your choice : ")

                    # --- Choice - 1 --> Add Book ----------
                if owner_choice == "1": 
                    title = input("Enter Book Title : ")
                    author = input("Enter Author Name: ")
                    year_input = input("Enter Book Publish year : ")
                    copies_input = input("Enter copies Awilable : ")

                    if not year_input.isdigit() or not copies_input.isdigit():
                        print("Invalid year or copies! Must be Numbers.")  # Integer check
                    else:
                        lib.add_book(title, author, int(year_input), int(copies_input))

                    # --- Choice - 2 --> Delete Book  ----------
                elif owner_choice == "2":
                    lib.view_books()
                    index_input = input("Enter book index to Delete Book : ")
                    #--------->>>>> Handle empty or invalid input
                    if not index_input.strip():
                        print("You can't skip the book index. Please enter a valid Number.")
                    elif not index_input.isdigit():
                        print("Invalid input! Please enter a number.")
                    else:
                        index = int(index_input) - 1
                        lib.delete_book(index)

                        # --- Choice - 3 --> Update Books ----------
                elif owner_choice == "3": 
                    lib.view_books()
                    index_input = input("Enter Book Index Number Update : ")

                    if not index_input.strip():
                        print("You can't skip the book index. Please enter a valid number.")
                    elif not index_input.isdigit():
                        print("Invalid input! Please enter a number.")
                    else:
                        index = int(index_input) - 1
                        lib.update_book(index)

                        # --- Choice - 4 --> View Books ----------
                elif owner_choice == "4":  
                    lib.view_books()

                    # --- Choice - 5 --> View Issued Books ----------
                elif owner_choice == "5": 
                    lib.view_issued_books()

                    # --- Choice - 6 --> Exit ----------
                elif owner_choice == "6":  
                    break

                else:
                    print("Invalid choice! Try again.")


        # ------------------- S T U D E N T - M E N U -------------------

        elif user_choice == "2":
            while True:
                print("\n--- S T U D E N T - M  E N U ---")
                print("1. View Books")
                print("2. Issue Book")
                print("3. Return Book")
                print("4. Exit")

                student_choice = input("Enter your choice: ")

                # --- Choice - 1 --> View Book ---------
                if student_choice == "1":
                    lib.view_books()

                    # --- Choice - 2 --> Issue Book ----------
                elif student_choice == "2":
                    lib.view_books()
                    index_input = input("Enter book index to issue: ")
                    student_name = input("Enter Your Name : ")

                    # Error handling for empty input
                    if not index_input.strip() or not index_input.isdigit():
                        print("You can't skip the book index. Enter a valid number.")
                    else:
                        index = int(index_input) - 1
                        lib.issue_book(index, student_name)

                        # --- Choice - 3 --> Return Book ----------
                elif student_choice == "3":
                    lib.view_books()
                    index_input = input("Enter book index to return : ")
                    student_name = input("Enter Your Name : ")

                    if not index_input.strip() or not index_input.isdigit():
                        print("You can't skip the book index. Enter a valid number.") # space Error Handle
                    else:
                        index = int(index_input) - 1
                        lib.return_book(index, student_name)

                        # --- Choice - 4 --> Exit ----------
                elif student_choice == "4":  # Exit student menu
                    break

                else:
                    print("Invalid choice! Try again.")


        # ------------------- Exit Program -------------------

        elif user_choice == "3":
            lib.save_books()  # Save all book records
            lib.save_issued()  # Save all issued records
            print("Exiting... Data Saved Successfully.")
            break
        else:
            print("Invalid Choice! Try Again.")
