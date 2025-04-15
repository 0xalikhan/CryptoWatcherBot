# CryptoWatcherBot 🚀

**CryptoWatcherBot** — Telegram-бот для отслеживания курсов криптовалют и получения свежих новостей. Работает с популярными монетами и позволяет настраивать гибкие уведомления.

---

## ✨ Возможности

- 📈 **/rate** — Получение актуального курса криптовалюты  
- 🔔 **/set_alert** — Установка уведомлений на изменение курса  
- ❌ **/remove_alert** — Удаление уведомлений  
- 🧾 **/alerts** — Просмотр активных уведомлений  
- ⚙️ **/set_threshold** — Настройка порога изменения курса  
- 📊 **/my_thresholds** — Просмотр текущих порогов  
- 📰 **/news** — Последние новости криптомира  
- 🆘 **/help** — Справка по командам  

---

## 💰 Поддерживаемые криптовалюты

- 🟡 `bitcoin`  
- 🟣 `ethereum`  
- 🐶 `dogecoin`  
- 🔵 `solana`  
- ⚪ `litecoin`  

---

## ▶️ Примеры использования

```bash
/rate bitcoin usd
```
> 📊 Покажет курс биткоина к доллару США.

```bash
/set_alert ethereum usd
```
> 🔔 Установит уведомление на изменение курса Ethereum.

```bash
/set_threshold bitcoin 2.0
```
> ⚙️ Уведомления при изменении курса биткоина более чем на 2%.

```bash
/remove_alert dogecoin usd
```
> ❌ Удалит уведомление на Dogecoin.

```bash
/news
```
> 📰 Последние новости из мира крипты.

---

## ⚙️ Установка и запуск

1. Клонируй репозиторий:
```bash
git clone https://github.com/твой_профиль/CryptoWatcherBot.git
cd CryptoWatcherBot
```

2. Установи зависимости:
```bash
pip install -r requirements.txt
```

3. Укажи свои ключи в `main.py`:
```python
TOKEN = "твой_telegram_token"
NEWS_API_KEY = "твой_newsapi_ключ"
```

4. Запусти бота:
```bash
python main.py
```

---

## 🔗 Используемые API

- [CoinGecko API](https://www.coingecko.com/) — курсы криптовалют  
- [NewsAPI.org](https://newsapi.org/) — крипто-новости
