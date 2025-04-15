import telebot
import requests

TOKEN = '7564159586:AAGffBtWB3kqiO4EbOpAaeFLWKLL4olGMNM'
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/simple/price'
NEWS_API_KEY = 'f981170d5b7348f9821df72943a7165a'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['news'])
def crypto_news(message):
    url = f'https://newsapi.org/v2/everything?q=crypto OR bitcoin OR cryptocurrency&language=ru&pageSize=5&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code != 200:
        bot.send_message(message.chat.id, "Не удалось получить новости.")
        return

    data = response.json()
    articles = data.get('articles', [])
    
    if not articles:
        bot.send_message(message.chat.id, "Новостей не найдено.")
        return

    reply = "Последние новости о криптовалютах:\n\n"
    for article in articles:
        title = article.get('title')
        url = article.get('url')
        reply += f"• [{title}]({url})\n"

    bot.send_message(message.chat.id, reply, parse_mode='Markdown')

last_rate = {}
user_alerts = {}
user_thresholds = {}

def get_crypto_rate(base_currency, target_currency):
    try:
        url = f"{COINGECKO_API_URL}?ids={base_currency.lower()}&vs_currencies={target_currency.lower()}"
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        if base_currency.lower() in data and target_currency.lower() in data[base_currency.lower()]:
            return data[base_currency.lower()][target_currency.lower()]
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def check_for_changes(base_currency, target_currency, current_rate):
    global last_rate
    threshold = user_thresholds.get(base_currency, 1.0)

    if base_currency in last_rate:
        previous_rate = last_rate[base_currency]
        change_percentage = abs(current_rate - previous_rate) / previous_rate * 100

        if change_percentage >= threshold:
            return True
    last_rate[base_currency] = current_rate
    return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я помогу тебе отслеживать курсы криптовалют. Используй команду /help для получения списка команд.')

@bot.message_handler(commands=['help'])
def help(message):
    help_text = (
        "Я помогу тебе отслеживать курсы криптовалют. Вот что я могу:\n\n"
        "/start — Приветственное сообщение от бота.\n"
        "/rate <криптовалюта_источник> usd — Получение курса криптовалюты к доллару США. Пример:\n"
        "/rate bitcoin usd\n"
        "/set_alert <криптовалюта_источник> usd — Установить уведомление на изменение курса криптовалюты. Пример:\n"
        "/set_alert bitcoin usd\n"
        "/news - Получить свежие новости о криптовалютах\n"
        "/alerts — Показать активные уведомления.\n"
        "/remove_alert <криптовалюта> — Удалить уведомление для криптовалюты. Пример:\n"
        "/remove_alert bitcoin\n"
        "/set_threshold <криптовалюта_источник> <порог> — Установить порог для уведомлений (например, 2.0%).\n\n"
        "Используй /help для получения этого списка снова."
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['rate'])
def get_rate(message):
    args = message.text.split()[1:]
    
    if len(args) != 2:
        bot.reply_to(message, 'Использование: /rate <криптовалюта_источник> usd')
        return

    base_currency = args[0].lower()
    target_currency = args[1].lower()

    supported_cryptos = ['bitcoin', 'ethereum', 'dogecoin', 'solana', 'litecoin']

    if base_currency not in supported_cryptos or target_currency != 'usd':
        bot.reply_to(message, 'Поддерживаемые криптовалюты: bitcoin, ethereum, dogecoin, solana, litecoin. Валюта назначения: usd.')
        return

    rate = get_crypto_rate(base_currency, target_currency)

    if rate:
        bot.reply_to(message, f"Курс {base_currency} к {target_currency}: {rate}")

        if base_currency in user_alerts.get(message.chat.id, []):
            if check_for_changes(base_currency, target_currency, rate):
                bot.send_message(message.chat.id, f"Внимание! Курс {base_currency} изменился на более чем {user_thresholds.get(base_currency, 1.0)}%!")
    else:
        bot.reply_to(message, f"Не удалось получить курс для {base_currency}/{target_currency}. Проверьте правильность криптовалют.")

@bot.message_handler(commands=['set_alert'])
def set_alert(message):
    args = message.text.split()[1:]

    if len(args) != 2:
        bot.reply_to(message, 'Использование: /set_alert <криптовалюта_источник> usd')
        return

    base_currency = args[0].lower()
    target_currency = args[1].lower()

    supported_cryptos = ['bitcoin', 'ethereum', 'dogecoin', 'solana', 'litecoin']

    if base_currency not in supported_cryptos or target_currency != 'usd':
        bot.reply_to(message, 'Поддерживаемые криптовалюты: bitcoin, ethereum, dogecoin, solana, litecoin. Валюта назначения: usd.')
        return

    if message.chat.id not in user_alerts:
        user_alerts[message.chat.id] = []

    if base_currency not in user_alerts[message.chat.id]:
        user_alerts[message.chat.id].append(base_currency)
        bot.reply_to(message, f"Вы подписались на уведомления о курсе {base_currency}.")
    else:
        bot.reply_to(message, f"Вы уже подписаны на уведомления для {base_currency}.")

@bot.message_handler(commands=['set_threshold'])
def set_threshold(message):
    args = message.text.split()[1:]

    if len(args) != 2:
        bot.reply_to(message, 'Использование: /set_threshold <криптовалюта_источник> <порог>')
        return

    base_currency = args[0].lower()
    try:
        threshold = float(args[1])
        if threshold <= 0:
            bot.reply_to(message, 'Порог должен быть больше 0.')
            return
    except ValueError:
        bot.reply_to(message, 'Введите корректное значение порога (например, 2.0).')
        return

    user_thresholds[base_currency] = threshold
    bot.reply_to(message, f"Порог для {base_currency} установлен на {threshold}%.")

@bot.message_handler(commands=['my_thresholds'])
def my_thresholds(message):
    if not user_thresholds:
        bot.reply_to(message, 'У вас нет установленных порогов.')
        return
    response = "Текущие пороги:\n"
    for currency, threshold in user_thresholds.items():
        response += f"- {currency.upper()}: {threshold}%\n"

    bot.reply_to(message, response)

@bot.message_handler(commands=['alerts'])
def alerts(message):
    if message.chat.id not in user_alerts or not user_alerts[message.chat.id]:
        bot.reply_to(message, "У вас нет активных уведомлений.")
    else:
        active_alerts = ', '.join(user_alerts[message.chat.id])
        bot.reply_to(message, f"Активные уведомления: {active_alerts}")

@bot.message_handler(commands=['remove_alert'])
def remove_alert(message):
    args = message.text.split()[1:]

    if len(args) != 1:
        bot.reply_to(message, 'Использование: /remove_alert <криптовалюта>')
        return

    base_currency = args[0].lower()

    if message.chat.id in user_alerts and base_currency in user_alerts[message.chat.id]:
        user_alerts[message.chat.id].remove(base_currency)
        bot.reply_to(message, f"Вы удалили уведомление для {base_currency}.")
    else:
        bot.reply_to(message, f"Вы не подписаны на уведомления для {base_currency}.")

if __name__ == '__main__':
    bot.polling(none_stop=True)