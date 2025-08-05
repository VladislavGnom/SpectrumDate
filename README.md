# SpectrumDate - Платформа для знакомств на Django

<img src="https://github.com/user-attachments/assets/cfb621d9-a2eb-4f2a-8c22-7238da2b887d" alt="Project LOGO" width="300px">

<img width="1024" height="583" alt="Image" src="https://github.com/user-attachments/assets/56379b31-863e-4787-b68e-c92aa51d74ab" />

<img width="1024" height="583" alt="Image" src="https://github.com/user-attachments/assets/6587b171-bd7e-4759-9043-644558a20906" />

<img width="1024" height="637" alt="Image" src="https://github.com/user-attachments/assets/86c84d61-d067-435d-81ff-426190ae6d61" />

<img width="1024" height="634" alt="Image" src="https://github.com/user-attachments/assets/ba8a7ab5-f85c-4db1-b3ec-9ce8c39306bb" />

## Описание проекта

SpectrumDate - это современная платформа для знакомств, разработанная на Django с использованием WebSockets для реального взаимодействия между пользователями.

**Ключевые возможности:**
- 🔐 Система регистрации и аутентификации
- 💌 Лента пользователей с функцией "Лайк/Дизлайк"
- 💬 Система чатов с историей сообщений
- 🌐 Онлайн-статусы в реальном времени
- 🤝 Уведомления о взаимных симпатиях
- 📱 Адаптивный интерфейс

## Технологический стек

### Бэкенд
- **Python 3.10+**
- **Django 5.2**
- **Django Channels** для WebSocket-взаимодействия
- **Redis** как бэкенд для Channels
- **Daphne** ASGI-сервер

### Фронтенд
- HTML5, CSS3, JavaScript
- WebSocket API для чатов и онлайн-статусов
- Pillow для обработки изображений

### База данных
- SQLite (в разработке)
- PostgreSQL (планируется для продакшена)

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SpectrumDate/spectrumIT.git
cd spectrumIT
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Запустите сервер:
```bash
python manage.py runserver
```

6. Для работы WebSockets запустите Daphne:
```bash
daphne spectrum.asgi:application --port 8000
```

## Функционал

### Основные модули
- **Лента пользователей** - просмотр анкет и выбор "Нравится/Не нравится"
- **Система чатов** - обмен сообщениями с взаимными симпатиями
- **Онлайн-статусы** - отображение активности в реальном времени

### Последние обновления
- Добавлена валидация пустых сообщений на фронтенде
- Реализована базовая функциональность чатов через WebSockets
- Добавлены стили для интерфейса чатов
- Реализованы онлайн-статусы через WebSockets

## Планы по развитию

- 📅 Добавление функционала постов и историй
- 📷 Поддержка медиафайлов в чатах
- 🔄 Улучшение механизма переподключения WebSockets
- 🎨 Обновление дизайна интерфейса (текущие стили не финальные)
- 🔍 Расширенные фильтры поиска
- 🤝 Редактирование личной информации в профиле пользователя
- 📱 Оптимизация для мобильных устройств

## Участие в разработке

Мы приветствуем вклад в проект! Для участия:

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request


**Примечание:** Проект находится в активной разработке.
