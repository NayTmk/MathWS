# MathWS  
  
**MathWS** — асинхронний API для гри з вирішенням математичних прикладів у режимі реального часу.    
Проєкт створено як практику моїх навичок і реалізацію власної ідеї, яка, на мою думку, має потенціал.  
  
---  
  
## Опис  
  
MathWS — це серверна частина гри, яка дозволяє користувачам створювати та брати участь у математичних сесіях, вирішувати приклади й змагатися в реальному часі.    
API побудовано на основі FastAPI із використанням асинхронного доступу до бази даних та авторизації через JWT і cookies.  
  
---  
  
## Функціонал  
  
- Реєстрація та авторизація користувача (JWT + OAuth2)  
- Аутентифікація через cookie для WebSocket-з'єднань  
- CRUD для ігрових сесій, статистики та даних користувача  
- Асинхронна робота з базою даних  
- Механізм оновлення даних у реальному часі через WebSocket  
  
---  
  
## Технології  
  
| Категорія | Використані технології           |     |
| --------- | -------------------------------- | --- |
| Backend   | FastAPI, SQLModel, Alembic       |     |
| Database  | PostgreSQL                       |     |
| Auth      | JWT, OAuth2, Cookies             |     |
| Async     | asyncio, SQLAlchemy AsyncSession |     |
  
---  
  
## Встановлення та запуск

### 1. Клонування репозиторію  
```bash
git clone <посилання-на-репозиторій>
cd <назва-папки>
```

### 2. Створіть файл `.env`  
Скопіюйте зразок і відредагуйте змінні:
```bash
cp env_example .env
# або вручну створіть .env і вставте значення зі env_example
```

### 3. (Опціонально) Віртуальне середовище для локальної роботи без Docker  
Якщо хочете запускати без Docker:
```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
> Але рекомендую запуск через Docker — нижче основні команди для цього.

### 4. Перевірте Docker і Docker Compose  
- Переконайтесь, що Docker встановлений і працює.

Перевірка:
```bash
docker --version
docker compose version   # або docker-compose --version
```

### 5. Запуск через Docker (рекомендовано)  
У кореневій директорії:
```bash
docker compose up --build
```
Або для фонового режиму:
```bash
docker compose up --build -d
```

### 6. Перевірка після запуску
- Документація OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Сторінка гри: [http://localhost:8000/game](http://localhost:8000/game)
- Adminer (якщо задіяно в docker-compose): [http://localhost:8080](http://localhost:8080)

### 7. Міграції бази даних (якщо запускається локально)
```bash
# приклад для alembic
alembic upgrade head
```

### 8. Зупинка і очищення
```bash
docker compose down
# або з видаленням томів і образів
docker compose down --volumes --rmi local
```