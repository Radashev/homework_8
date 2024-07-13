import pika
from mongoengine import connect, disconnect
from models import Contact

# Відключення попереднього з'єднання, якщо таке є
disconnect()

# Підключення до MongoDB
connect(db="hw", host="localhost:27017")

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def process_message(ch, method, properties, body):
    contact_id = body.decode()
    try:
        contact = Contact.objects.get(id=contact_id)
        print(f"Processing email for Contact ID: {contact_id}")
        # Тут можна додати імітацію відправки email
        print(f"Simulating email sending for Contact ID: {contact_id}")

        # Позначаємо, що повідомлення було надіслане
        contact.sent_message = True
        contact.save()
        print(f"Marked Contact ID {contact_id} as message sent")
    except Contact.DoesNotExist:
        print(f"Contact with ID {contact_id} not found in the database")

channel.basic_consume(queue='email_queue', on_message_callback=process_message, auto_ack=True)

print('Waiting for email messages. To exit press CTRL+C')
channel.start_consuming()
