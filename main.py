import json
import redis
from redis_lru import RedisLRU
from mongoengine import connect
from models import Author, Quote

# Підключення до MongoDB Atlas
connect(db="hw", host="mongodb://localhost:27017")

# Підключення до Redis
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_tag(tag: str) -> list[str]:
    quotes = Quote.objects(tags__iregex=tag)
    return [q.quote for q in quotes]

@cache
def find_by_author(author: str) -> list[str]:
    authors = Author.objects(fullname__iregex=author)
    result = []
    for a in authors:
        quotes = Quote.objects(author=a)
        result.extend([q.quote for q in quotes])
    return result

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
    load_authors('authors.json')
    load_quotes('quotes.json')
    while True:
        command = input("Enter command (name: <author> | tag: <tag> | tags: <tag1,tag2> | exit): ")
        if command.startswith("name: "):
            author = command[len("name: "):].strip()
            results = find_by_author(author)
            print('\n'.join(results).encode('utf-8').decode('utf-8', 'ignore'))
        elif command.startswith("tag: "):
            tag = command[len("tag: "):].strip()
            results = find_by_tag(tag)
            print('\n'.join(results).encode('utf-8').decode('utf-8', 'ignore'))
        elif command.startswith("tags: "):
            tags = command[len("tags: "):].strip().split(',')
            results = []
            for tag in tags:
                results.extend(find_by_tag(tag.strip()))
            print('\n'.join(results).encode('utf-8').decode('utf-8', 'ignore'))
        elif command == "exit":
            break
        else:
            print("Invalid command.")
