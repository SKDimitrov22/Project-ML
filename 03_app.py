import streamlit as st
import weaviate
import os
from dotenv import load_dotenv
from weaviate_agents.query import QueryAgent

# Зареждане на ключовете
load_dotenv()

# Настройки на страницата
st.set_page_config(page_title="Филмов Асистент", page_icon="🎬")
st.title("🎬 Интелигентен Филмов Асистент")
st.markdown("Този асистент използва **Weaviate Query Agent** и търси автономно в колекциите `Movie` и `Director`.")

# Странична лента (Sidebar)
st.sidebar.header("📂 Колекции в употреба")
st.sidebar.markdown("- **Movie** (Филми, Резюмета, Аудитория)\n- **Director** (Режисьори, Награди)")
st.sidebar.info(
    "💡 **Примерни тестови заявки:**\n\n"
    "1️⃣ *Обикновено търсене:*\nКои филми са излезли преди 2015?\n\n"
    "2️⃣ *Multi-collection:*\nКой е режисьор на Интерстелар и какви награди има?\n\n"
    "3️⃣ *Follow-up:*\nА кой е най-новият му филм?\n\n"
    "4️⃣ *Агрегация:*\nКолко филма има с рейтинг над 8.5?\n\n"
    "5️⃣ *Свободна форма:*\nПрепоръчай ми нещо разтоварващо с роботи."
)


# Инициализация на агента (кешира се, за да е бързо)
@st.cache_resource
def init_agent():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
        headers={"X-Goog-Studio-Api-Key": os.getenv("GOOGLE_API_KEY")}
    )

    agent = QueryAgent(
        client=client,
        collections=["Movie", "Director"],
        system_prompt="You are a helpful movie assistant. Always answer in Bulgarian language. Use only facts from the databases."
    )
    return client, agent


try:
    client, agent = init_agent()
except Exception as e:
    st.error(f"Грешка при свързване: {e}")
    st.stop()

# Пазене на историята на чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показване на старите съобщения
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Поле за нов въпрос
if prompt := st.chat_input("Задайте своя въпрос тук..."):
    # Добавяме въпроса на потребителя
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерираме отговор
    with st.chat_message("assistant"):
        with st.spinner("Асистентът мисли и търси в базите данни..."):
            try:
                # Извикваме агента
                response = agent.run(prompt)

                # Взимаме финалния отговор
                answer_text = response.final_answer if hasattr(response, 'final_answer') else str(response)

                st.markdown(answer_text)
                st.session_state.messages.append({"role": "assistant", "content": answer_text})
            except Exception as e:
                st.error(f"Възникна грешка при заявката: {e}")