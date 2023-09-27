import os
import cv2
import asyncio

import numpy as np

from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile
from aiogram import Bot, Dispatcher

from bot.utils import BOT_TOKEN


count = 0
classfile = 'classnames.txt'


with open(classfile, 'rt', encoding='UTF-8') as f:
    classnames = f.read().rstrip('\n').split('\n')

configpath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightspath = 'frozen_inference_graph.pb'


net = cv2.dnn_DetectionModel(weightspath, configpath)
net.setInputSize(100, 100)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


dp = Dispatcher()


bot = Bot(BOT_TOKEN)

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/stream',
                   description='Запуск видеопотока'),

        BotCommand(command='/getframe',
                   description='Получить кадр'),

        BotCommand(command='/stop',
                   description='Остановка видеопотока'),
    ]

    await bot.set_my_commands(main_menu_commands)

def streaming():
    global cap
    global flag
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        global succes, img
        _, img = cap.read()
        thres = 0.45
        nms_thres = 0.55
        classids, confs, bbox = net.detect(img, confThreshold=thres)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1, -1)[0])
        confs = list(map(float, confs))
        indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_thres)

        for i in indices:
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
            cv2.putText(img, classnames[classids[i] - 1].upper(), (box[0] + 5, box[1] - 5),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

        if flag is False:
            break


@dp.message(Command(commands='stream'))
async def livestream(message: Message):
    global flag
    flag = True
    loop = asyncio.get_event_loop()

    await message.answer(text='Stream running. . .')
    await loop.run_in_executor(None, streaming)


@dp.message(Command(commands='stop'))
async def stop_stream(message: Message):
    await message.answer(text='Stoped!')
    global flag
    flag = False
    cap.release()


@dp.message(Command(commands='getframe'))
async def save_frame(message: Message):
    global count
    global img
    name = 'screen/frame' + str(count) + '.jpg'
    cv2.imwrite(name, img)
    entry = max((e for e in os.scandir('screen') if e.is_file(follow_symlinks=False)),
                key=lambda e: getattr(e.stat(), 'st_birthtime', None) or e.stat().st_ctime)
    last_file = FSInputFile(entry.path)
    await message.answer_photo(photo=last_file)
    count += 1


async def start() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    asyncio.run(start())