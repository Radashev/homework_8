from faker import Faker
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect(db="hw", host="mongodb://localhost:27017")

# Створення екземпляра Faker
fake = Faker()

def create_fake_contact():
    fullname = fake.name()
    email = fake.email()
    sent_message = fake.boolean()
    return Contact(fullname=fullname, email=email, sent_message=sent_message)

if __name__ == '__main__':
    for _ in range(20):  # Генеруємо 20 контактів
        contact = create_fake_contact()
        contact.save()
        print(f"Created Contact: {contact.fullname}, {contact.email}, {contact.sent_message}")
