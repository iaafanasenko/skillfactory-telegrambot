import telebot
from extensions import Converter, APIException
from config import TOKEN, exchanges


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию введите команду боту в следующем формате: \n \
<имя валюты>  <в какую валюту перевести>  <количество переводимой валюты> \n\n \
Для того, чтобы посмотреть список всех доступных валют, введите команду: \n \
/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException('Неверное количество параметров. \n\n\
Введите команду боту в следующем формате: \n\
<имя валюты>  <в какую валюту перевести>  <количество переводимой валюты>')

        base, quote, amount = values
        total = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в команде:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        bot.reply_to(message, f'Конвертация: {base} - {quote}. Количество: {amount}. \n\
Итог: {total}')


bot.polling()
