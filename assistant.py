import pickle
from collections import UserDict
from datetime import datetime, timedelta

class Field: 
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
class Name(Field):
    # def __init__(self, value):
    #     self.value = value
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("The phone didn't pass validation")
        
class Birthday(Field):
    def __init__(self, birthday):
        try:
            super().__init__(datetime.strptime(birthday, "%d.%m.%Y").date())
        
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        self.phones = [p for p in self.phones if str(p) != phone_number]

    # TODO: Потрібно додати функції з попередньої роботи
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones: # ітерація по номерах в списку
            if p.value == old_phone: # перевіряємо чи заданий номер "дорівнює" номеру, який ми хочемо замінити
                p.value = new_phone # якщо збігається - замінюємо на новий
    
    def find_phone(self, phone):
        for p in self.phones: # ітерація по номерах в списку
            if p.value == phone: # перевірка чи заданий номер є у списку
                return p # повертаємо його
        return "Contact is missing" # повертаємо повідомлення, якщо номер не знайдено

    #Не вийшло правильно перетворити, тому написав нові методи            
    # def edit_phone(self, args):
    #     name, new_phone = args

    #     if name == self.name.value:
    #         self.phones = [new_phone]
    #         return "Contact changed!"
    #     else:
    #         return "Contact is missing"

    # def find_phone(self, args):
    #     name = args[0]
    #     if name == self.name.value:
    #         return self.phones
    #     else:
    #         return "Contact is missing"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):                                                  
        return f'Contact name: {self.name}, Phones: {"; ".join(str(p) for p in self.phones)}, Birthday: {self.birthday})'
    
    def __repr__(self):
        return f'Contact name: {self.name}, Phones: {"; ".join(str(p) for p in self.phones)}, Birthday: {self.birthday}'

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find_next_weekday(self, d, weekday: int):                                                 
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + timedelta(days=days_ahead)

    def get_upcoming_birthdays(self):                                                                
        days = 7
        today_date = datetime.today().date()
        upcoming_birthdays = []
        for el in self.data.values():
            if el.birthday:
                birthday_this_year = el.birthday.value.replace(year=today_date.year)
                if birthday_this_year < today_date:
                    birthday_this_year = birthday_this_year.replace(year=today_date.year + 1)           
                elif 0 <= (birthday_this_year - today_date).days <= days:
                    if birthday_this_year.weekday() >= 5:
                        birthday_this_year = self.find_next_weekday(birthday_this_year, 0)
                    congratulation_date = birthday_this_year.strftime("%d.%m.%Y")            
                    upcoming_birthdays.append({'Name': el.name, "Congratulation Date": congratulation_date})
        return upcoming_birthdays
    
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def add_contact(args, book):
    name, phone = args
    if name in book:
        book[name].add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return "Contact added."

def change_contact(args, book):
    name, new_phone = args
    if name in book:
        book[name].add_phone(new_phone)
        return "Contact changed!"
    else:
        return "Contact is missing"

def show_phone(args, book):
    name = args[0]
    if name in book:
        return ", ".join(str(phone) for phone in book[name].phones)
    else:
        return "Contact is missing"

def show_all_contacts(book):
    if book:
        return "\n".join(str(record) for record in book.values())
    else:
        return "Address book is empty."

def add_birthday(args, book):                          
    name, birthday = args
    if name in book:
        book[name].add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact is missing."

def show_birthday(args, book):                    
    name = args[0]
    if name in book and book[name].birthday:
        return str(book[name].birthday)
    else:
        return "Birthday not found or contact is missing."

def show_upcoming_birthdays(book):                              
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(f"{birthday['Name']} - {birthday['Congratulation Date']}" for birthday in upcoming_birthdays)
    else:
        return "No upcoming birthdays."

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

@error_handler
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command == "close" or command == "exit":
            print ("Good bye! :)")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))  

        elif command == "change":
            print(change_contact(args, book))
                  
        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))  
        
        elif command == "add_birthday":
            print(add_birthday(args, book))
        
        elif command == "show_birthday":
            print(show_birthday(args, book))
        
        elif command == "birthdays":
            print(show_upcoming_birthdays(book))
        
        else:
            print("Invalid command.")
        
        save_data(book)  # Викликати перед виходом з програми

if __name__ == "__main__":
    main()