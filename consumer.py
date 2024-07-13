import pika
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect(db="hw", host="mongodb://localhost:27017")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

def process_message(ch, method, properties, body):
    contact_id = body.decode()
    try:
        contact = Contact.objects.get(id=contact_id)
        # Тут можна додати імітацію відправки email
        print(f"Simulating email sending for Contact ID: {contact_id}")

        # Позначаємо, що повідомлення було надіслане
        contact.sent_message = True
        contact.save()
        print(f"Marked Contact ID {contact_id} as message sent")
    except Contact.DoesNotExist:
        print(f"Contact with ID {contact_id} not found in the database")


channel.basic_consume(queue='email_queue', on_message_callback=process_message, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# import pika
# import json
# from mongoengine import connect
# from models import Contact
#
# # Підключення до MongoDB
# connect(db="hw", host="mongodb://localhost:27017")
#
# # Підключення до RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
#
# # Створення черги, якщо вона не існує
# channel.queue_declare(queue='email_queue', durable=True)
#
# def send_email(contact_id):
#     # Логіка надсилання email, це може бути ваша реальна функція надсилання email
#     # Здесь ваш код для надсилання email
#     print(f"Sending email to contact with id: {contact_id}")
#
#     # Позначаємо контакт як 'sent_message=True' в MongoDB
#     contact = Contact.objects.get(id=contact_id)
#     contact.sent_message = True
#     contact.save()
#
# def callback(ch, method, properties, body):
#     message = json.loads(body)
#     contact_id = message['contact_id']
#     send_email(contact_id)
#     print(f" [x] Received {contact_id}")
#
# channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
