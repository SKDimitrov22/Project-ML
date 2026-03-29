# Project-ML

Този проект демонстрира интеграция с Weaviate и използване на Weaviate агенти (Query & Transformation). **Забележка:** Всички трансформирани данни в този проект са тестови/примерни данни (sample data), а не продукционни.

## Изисквания

1. Python 3.9+ 
2. Настроени API ключове за Weaviate и Google AI Studio.

## Описание на колекциите и данните

Проектът работи с две основни колекции:
- **Director (Режисьор):** Съдържа `name` (име), `biography` (биография) и `awards` (брой награди).
- **Movie (Филм):** Съдържа `title` (заглавие), `description` (многоезично резюме), `release_year` (година), `genre` (жанр), `director_name` (връзка към режисьора) и `rating` (оценка). 
  - *Допълнително поле:* `target_audience` (целева аудитория), което се генерира автоматично от Weaviate Transformation Agent на базата на съществуващите данни.

Данните са напълно тестови (sample data), заредени директно в скрипта `01_load_data.py`.

## Инсталация

Ако нямате инсталирани зависимостите, можете да ги добавите в средата си (вече имате `weaviate_env`):
```bash
source weaviate_env/bin/activate
pip install streamlit weaviate-client python-dotenv
```
*(Забележка: специфичните `weaviate-agents` пакети също трябва да са инсталирани според вашата среда)*

## Конфигурация (Environment Variables)

Проектът използва `.env` файл за сигурно съхранение на ключове. Създайте файл `.env` в основната директория със следното съдържание:

```env
WEAVIATE_URL="https://вашият-weaviate-клъстер.weaviate.cloud"
WEAVIATE_API_KEY="вашият-weaviate-api-ключ"
GOOGLE_API_KEY="вашият-google-api-ключ"
```

## Инструкции за стартиране

Изпълнете скриптовете в следната последователност:

1. **Инициализация и зареждане на тестовите данни:**
   ```bash
   python 01_load_data.py
   ```
2. **Обогатяване на данните с Transformation Agent:**
   ```bash
   python 02_transform_data.py
   ```
3. **Стартиране на потребителския интерфейс (Streamlit):**
   ```bash
   streamlit run 03_app.py
   ```
