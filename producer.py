import random
import pika
from faker import Faker
from mongoengine import connect, disconnect
from models import Contact

# Відключення попереднього з'єднання, якщо таке є
disconnect()

# Підключення до MongoDB
connect(db="hw", host="mongodb://localhost:27017")

fake = Faker()

def generate_fake_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        fullname = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        preferred_contact_method = random.choice(['email', 'sms'])
        contacts.append({
            'fullname': fullname,
            'email': email,
            'phone_number': phone,
            'preferred_method': preferred_contact_method,
            'sent_message': False
        })
    return contacts

def save_contacts_to_db(contacts):
    saved_contacts = []
    for contact_data in contacts:
        contact = Contact(**contact_data)
        contact.save()
        saved_contacts.append(contact)
    return saved_contacts

def send_contact_ids_to_queue(saved_contacts):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.queue_declare(queue='sms_queue')

    for contact in saved_contacts:
        message = str(contact.id)
        if contact.preferred_method == 'email':
            channel.basic_publish(exchange='', routing_key='email_queue', body=message)
            print(f"Sent message to email queue with Contact ID: {message}")
        else:
            channel.basic_publish(exchange='', routing_key='sms_queue', body=message)
            print(f"Sent message to SMS queue with Contact ID: {message}")

    connection.close()

if __name__ == '__main__':
    num_contacts = 5  # Кількість фейкових контактів, яку потрібно згенерувати
    fake_contacts = generate_fake_contacts(num_contacts)
    saved_contacts = save_contacts_to_db(fake_contacts)
    send_contact_ids_to_queue(saved_contacts)
