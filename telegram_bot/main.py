from model import ClassPredictor
from telegram_token import token
import torch
from config import reply_texts
import numpy as np
from PIL import Image
from io import BytesIO
import datetime

import warnings
warnings.filterwarnings("ignore")


model = ClassPredictor()


def send_prediction_on_photo(bot, update):
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    image_stream = BytesIO()
    image_file.download(out=image_stream)

    class_ = model.predict(image_stream)
    # здесь делаем нормальное название класса,
    # т.е. убираем цифры и нижнее подчеркивание
    class_ = (str(class_)).lower()[10:]
    class_ = class_.replace('_', ' ')

    # теперь отправим результат
    update.message.reply_text('I think it\'s a ' + class_)
    print("[{}] Sent Answer to user, predicted: {}".format(datetime.datetime.now(), class_))

def start(bot, update):
    update.message.reply_text('Hello! Here I try to classify dogs. I know such breeds of dogs:\n\
- chihuahua;\n- japanese spaniel;\n- maltese dog;\n- pekinese;\n- shih-tzu;\n\
- blenheim spaniel;\n- papillon;\n- toy terrier;\n- rhodesian ridgeback;\n- afghan hound;\n\
- basset;\n- beagle;\n- bloodhound;\n- bluetick;\n- black-and-tan coonhound;\n\
- walker hound;\n- redbone;\n- borzoi;\n- irish wolfhound;\n- italian greyhound\n\
- whippet;\n- ibizian hound;\n- norwegian elkhound;\n- saluki;\n- scottish deerhound\n\
- weimarane;\n- staffordshire bullterrier;\n- american staffordshire terrier;\n\
- bedlington terrier;\n- border terrier;\n- kerry blue terrier;\n- irish terrier;\n\
- norfolk terrier;\n- norwish terrier;\n- yorkshire terrier;\n- wire-haired fox terrier;\n\
- lakeland terrier;\n- sealyham terrier;\n- airedale;\n- cairn;\n- australian terrier;\n\
- dandie dinmont;\n- boston bull;\n- miniature schnauzer;\n- giant schnauzer;\n\
- standard schnauzer;\n- scotch terrier;\n- tibetan terrier;\n- silky_terrier;\n\
- soft-coated wheaten terrier;\n- west highland white terrier;\n- lhasa;\n\
- flat-coated retriever;\n- curly-coated retriever;\n- golden retriever;\n\
- labarador retriever;\n- chesapeake bay retriever;\n- german short-haired pointer;\n\
- vizsla;\n- english setter;\n- irish settler;\n- gordon setter;\n- britanny spaniel;\n\
- clumber;\n- english springer;\n- welsh springer spaniel;\n- cocker spaniel;\n\
- sussex spaniel;\n- irish water spaniel;\n- kuvasz;\n- schipperke.')
    print("[{}] I have greeted someone just now.".format(datetime.datetime.now()))

if __name__ == '__main__':
    from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
    import logging

    # Включим самый базовый логгинг, чтобы видеть сообщения об ошибках
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    # используем прокси, так как без него у меня ничего не работало(
    REQUEST_KWARGS={
        'proxy_url': 'http://51.79.31.19:8080/'
    }
    updater = Updater(token=token, request_kwargs=REQUEST_KWARGS)
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.start_polling()
