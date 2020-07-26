import telebot
import requests
import datetime

def launchBot():
    '''
    * Bot settings *
    - loading token
    - loading appid
    '''

    s_city = 'Yaroslavl,RU'

    try:
        token = '1246966197:AAEqDcStmSK5pV7R_lKTf3gsoM9A5IKl_6M'
        appid = 'b1991dbfa970987c677941054397038b'

        bot = telebot.TeleBot(token)

        '''
        * Bot handlers *
        - start
        - help
        - now
        - forecast DATA
        - another_text
        '''

        @bot.message_handler(commands=['start'])
        def start_handler(message):
            msg_text = 'Привет! Интересуешься погодой в городе Ярославль?\n' \
                       'Тогда ты пришел по адресу: введи команду /help для ознакомления с доступными тебе опциями.'
            bot.send_message(message.chat.id, msg_text)

        @bot.message_handler(commands=['help'])
        def help_handler(message):
            msg_text = 'Итак, ты можешь:\n' \
                       '/now - узнать, какая сейчас погода:\n' \
                       '/forecast ДАТА - получить прогноз погоды на конкретную дату в ' \
                       'следующие 5 дней (например, /forecast 25.07.2020)\n' \
                       'Если забудешь какую-либо команду - можешь еще раз заглянуть сюда через /help.'
            bot.send_message(message.chat.id, msg_text)

        @bot.message_handler(commands=['now'])
        def now_handler(message):
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/find",
                                   params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid, 'lang': 'ru'})
                data = res.json()
                print(str(data['list'][0]))
                msg_text = 'Погода сейчас: ' + str(data['list'][0]['weather'][0]['description']) + '\n' \
                                                                                                   'Температура воздуха: ' + str(
                    data['list'][0]['main']['temp']) + ' °C\n' \
                                                       'Давление: ' + str(data['list'][0]['main']['pressure']) + ' hPa\n' \
                                                                                                                 'Влажность: ' + str(
                    data['list'][0]['main']['humidity']) + ' %'

            except Exception as e:
                msg_text = 'Ошибка, сервис погоды временно не работает.\n' \
                           'Зайдите, пожалуйста, позже.'
                pass

            bot.send_message(message.chat.id, msg_text)

        @bot.message_handler(commands=['forecast'])
        def forecast_handler(message):
            msg_text = ''

            try:
                datetime.datetime.strptime(message.text.split()[1], '%Y-%m-%d')
            except Exception as e:
                msg_text = 'Некорректный формат даты: должен быть YYYY-MM-DD (Например, 2020-07-25).'

            try:
                date = message.text.split()[1]
                res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                                   params={'q': s_city, 'units': 'metric', 'APPID': appid, 'lang': 'ru'})
                data = res.json()
                for sub_data in data['list']:
                    if date in sub_data['dt_txt']:
                        msg_text = 'Погода на ' + date + ': ' + str(sub_data['weather'][0]['description']) + '\n' \
                                                                                                             'Температура воздуха: ' + str(
                            sub_data['main']['temp']) + ' °C\n' \
                                                        'Давление: ' + str(sub_data['main']['pressure']) + ' hPa\n' \
                                                                                                           'Влажность: ' + str(
                            sub_data['main']['humidity']) + ' %'
                        break

                if not msg_text:
                    msg_text = 'Ошибка: дата выходит за рамки рассматриваемого диапазона (5 дней).'

            except Exception as e:
                if not msg_text:
                    msg_text = 'Ошибка: сервис погоды временно не работает.\n' \
                               'Зайдите, пожалуйста, позже.'
                pass

            bot.send_message(message.chat.id, msg_text)

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            msg_text = 'К сожалению, я тебя не понимаю. Попробуй /help.'
            bot.send_message(message.from_user.id, msg_text)

        bot.polling(none_stop=True, interval=0)

        return bot
    except Exception as e:
        print('Ошибка загрузки конфига и инициализации бота.\n'
              'Пожалуйста, проверьте ваш конфиг файл config.txt:\n'
              'Все токены должны быть действительны и строки не должны содержать пробелы.\n')


'''
* Bot starting *
'''

if __name__ == '__main__':
    bot = launchBot()
