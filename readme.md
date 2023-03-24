# Reddit scraper, vk poster

Качает картинки с реддита и постит их в паблик вк

# Quick start

- Создаём `.env` с нужными настройками (пример в `.env.example`)
- `$ python3 -m venv .venv`
- `$ source .venv/bin/activate`
- `$ pip install -r requirements.txt` or `$ pip install requests "pydantic[dotenv]"`
- `$ python main.py`

## TODO:
- Выбор сабреддита
- Умная лента (мемы из разных сабреддитов)
- Аппенд к уже существующим постам, вместо тупого добавления в очередь на публикацию
- Придумать как постить гифки
- Интеграция с телегой