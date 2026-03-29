import weaviate
import os
import time
from dotenv import load_dotenv
from weaviate.classes.config import DataType
from weaviate_agents.transformation import TransformationAgent
from weaviate_agents.transformation.classes import AppendPropertyOperation

load_dotenv()

# Свързване с Weaviate
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    headers={"X-Goog-Studio-Api-Key": os.getenv("GOOGLE_API_KEY")}
)

try:
    print("Подготовка на трансформацията...")

    # 1. Първо дефинираме операцията
    operation = AppendPropertyOperation(
        property_name="target_audience",
        data_type=DataType.TEXT,
        view_properties=["title", "description", "genre"],
        instruction="Въз основа на заглавието, резюмето и жанра, определи кратка целева аудитория за филма на български език (напр. 'Фенове на дълбоката фантастика', 'За възрастни', 'Любители на екшъна'). Максимум 3-5 думи."
    )

    # 2. Инициализираме агента
    print("Инициализиране на Transformation Agent...")
    agent = TransformationAgent(
        client=client,
        collection="Movie",
        operations=[operation]
    )

    # 3. Стартираме го
    print("Стартиране на асинхронна трансформация...")
    response = agent.update_all()

    # Взимаме ID-то директно от обекта!
    workflow_id = response.workflow_id

    print(f"✅ Операцията започна! Workflow ID: {workflow_id}")
    print("Проверка на статуса (може да отнеме минута)...")

    # Проверяваме статуса на всеки 5 секунди
    # Проверяваме статуса на всеки 5 секунди
    # Проверяваме статуса на всеки 5 секунди
    while True:
        status_dict = agent.get_status(workflow_id=workflow_id)

        # Взимаме статуса безопасно от речника
        current_status = str(status_dict.get('status', 'неизвестен')).lower()

        print(f"Текущ статус: {current_status}")

        if current_status in ['completed', 'failed', 'success']:
            break
        time.sleep(5)

    print("Процесът приключи. Данните са обогатени!")

except Exception as e:
    print(f"Възникна грешка по време на трансформацията: {e}")

finally:
    client.close()