import json
from mongoengine import connect
from models import Author, Quote

# Підключення до MongoDB Atlas
connect(db="hw", host="mongodb://localhost:27017")


def load_authors(authors_file):
    with open(authors_file, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author in authors_data:
            existing_author = Author.objects(fullname=author['fullname']).first()
            if existing_author:
                existing_author.update(
                    born_date=author['born_date'],
                    born_location=author['born_location'],
                    description=author['description']
                )
            else:
                new_author = Author(
                    fullname=author['fullname'],
                    born_date=author['born_date'],
                    born_location=author['born_location'],
                    description=author['description']
                )
                new_author.save()


def load_quotes(quotes_file):
    with open(quotes_file, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote in quotes_data:
            author = Author.objects.get(fullname=quote['author'])
            new_quote = Quote(
                author=author,
                tags=quote['tags'],
                quote=quote['quote']
            )
            new_quote.save()


if __name__ == "__main__":
    load_authors('../authors.json')
    load_quotes('../quotes.json')
