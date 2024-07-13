from models import Author, Quote
import redis
from redis_lru import RedisLRU

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

if __name__ == "__main__":
    while True:
        command = input("Enter command (name: <author> | tag: <tag> | tags: <tag1,tag2> | exit): ")
        if command.startswith("name: "):
            author = command[len("name: "):].strip()
            print(find_by_author(author))
        elif command.startswith("tag: "):
            tag = command[len("tag: "):].strip()
            print(find_by_tag(tag))
        elif command.startswith("tags: "):
            tags = command[len("tags: "):].strip().split(',')
            for tag in tags:
                print(find_by_tag(tag))
        elif command == "exit":
            break
        else:
            print("Invalid command.")
