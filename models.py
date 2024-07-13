from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE, BooleanField

# Підключення до MongoDB
connect(db="hw", host="mongodb://localhost:27017")

# Модель автора

class Author(Document):
    fullname = StringField(required=True, unique=True)  # Повне ім'я автора
    born_date = StringField(max_length=50)  # Дата народження
    born_location = StringField(max_length=150)  # Місце народження
    description = StringField()  # Опис автора
    meta = {"collection": "authors"}  # Налаштування колекції в MongoDB

# Модель цитати

class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)  # Ссилка на автора цитати
    tags = ListField(StringField(max_length=15))  # Список тегів
    quote = StringField()  # Текст цитати
    meta = {"collection": "quotes"}  # Налаштування колекції в MongoDB

# Модель контакту
class Contact(Document):
    fullname = StringField(required=True)  # Повне ім'я контакту
    email = StringField(required=True)  # Email контакту
    phone_number = StringField(required=True)
    sent_message = BooleanField(default=False)  # Прапорець, що показує, чи було відправлено повідомлення
    preferred_method = StringField(choices=["email", "sms"], default="email")
    meta = {'collection': 'contacts'}  # Налаштування колекції в MongoDB


    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)