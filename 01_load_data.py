import weaviate
from weaviate.classes.config import Configure, Property, DataType
import os
from dotenv import load_dotenv

# Зареждане на променливите от .env файла
load_dotenv()

# Свързване с Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    headers={
        "X-Goog-Studio-Api-Key": os.getenv("GOOGLE_API_KEY")  # ВАЖНО: Сменихме името на хедъра за AI Studio
    }
)


def setup_database():
    print("Проверка и изтриване на стари колекции (ако има такива)...")
    client.collections.delete("Movie")
    client.collections.delete("Director")

    print("Създаване на колекция 'Director'...")
    client.collections.create(
        name="Director",
        vectorizer_config=Configure.Vectorizer.text2vec_google_aistudio(),
        # ДОБАВЯМЕ project_id="", за да не се сърди Python
        generative_config=Configure.Generative.google(project_id=""),
        properties=[
            Property(name="name", data_type=DataType.TEXT),
            Property(name="biography", data_type=DataType.TEXT),
            Property(name="awards", data_type=DataType.INT)
        ]
    )

    print("Създаване на колекция 'Movie'...")
    client.collections.create(
        name="Movie",
        vectorizer_config=Configure.Vectorizer.text2vec_google_aistudio(),
        # ДОБАВЯМЕ project_id="" И ТУК
        generative_config=Configure.Generative.google(project_id=""),
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="description", data_type=DataType.TEXT),
            Property(name="release_year", data_type=DataType.INT),
            Property(name="genre", data_type=DataType.TEXT),
            Property(name="director_name", data_type=DataType.TEXT),
            Property(name="rating", data_type=DataType.NUMBER)
        ]
    )

def load_sample_data():
    directors = client.collections.get("Director")
    movies = client.collections.get("Movie")

    # Примерни данни за режисьори
    directors_data = [
        {"name": "Кристофър Нолан",
         "biography": "Британско-американски режисьор, известен със своите сложни и визуално впечатляващи блокбъстъри.",
         "awards": 15},
        {"name": "Дени Вилньов",
         "biography": "Канадски режисьор, утвърдил се като майстор на съвременната научна фантастика.", "awards": 8}
    ]

    print("Зареждане на режисьори...")
    with directors.batch.dynamic() as batch:
        for d in directors_data:
            batch.add_object(properties=d)

    # Примерни данни за филми
    movies_data = [
        {"title": "Генезис (Inception)",
         "description": "Крадци проникват в сънищата на хората, за да откраднат техните тайни. Една последна мисия изисква от тях да посадят идея, вместо да я откраднат.",
         "release_year": 2010, "genre": "Sci-Fi", "director_name": "Кристофър Нолан", "rating": 8.8},
        {"title": "Интерстелар",
         "description": "Екип от изследователи пътува през червеева дупка в космоса в опит да осигури оцеляването на човечеството.",
         "release_year": 2014, "genre": "Sci-Fi", "director_name": "Кристофър Нолан", "rating": 8.7},
        {"title": "Дюн",
         "description": "Синът на благородна фамилия е натоварен със защитата на най-ценния актив и най-важния елемент в галактиката.",
         "release_year": 2021, "genre": "Sci-Fi", "director_name": "Дени Вилньов", "rating": 8.0},
        {"title": "Блейд Рънър 2049",
         "description": "Млад блейд рънър открива отдавна погребана тайна, която може да потопи остатъците от обществото в хаос.",
         "release_year": 2017, "genre": "Sci-Fi", "director_name": "Дени Вилньов", "rating": 8.0}
    ]

    print("Зареждане на филми...")
    with movies.batch.dynamic() as batch:
        for m in movies_data:
            batch.add_object(properties=m)

    print("Данните са успешно заредени в Weaviate!")


try:
    setup_database()
    load_sample_data()
except Exception as e:
    print(f"Възникна грешка при изпълнение: {e}")
finally:
    client.close()