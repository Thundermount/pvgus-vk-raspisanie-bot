import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime, date, time, timedelta
import random
import threading
from get_schedule import *

token = "вставьте свой токен бота"

vk = vk_api.VkApi(token=token)


api = vk.get_api()

board1 = VkKeyboard(one_time=True)
board1.add_button('Сегодня', color=VkKeyboardColor.PRIMARY)
board1.add_button('Завтра', color=VkKeyboardColor.PRIMARY)
board1.add_button('Вчера', color=VkKeyboardColor.PRIMARY)

indexes = dict()


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":random.getrandbits(64)})
def write_msg_k(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'keyboard':keyboard,"random_id":random.getrandbits(64)})

today = datetime.today()
def get_day(day):
    return day.strftime('%d.%m.%Y')

def dialogue(event):
    index = indexes[event.user_id]['index']
    group_name = indexes[event.user_id]['group']
    date = indexes[event.user_id]['date']
    print(group_name + date)
    if(index == 0):
        write_msg(event.user_id,"Введите название группы")
    if(index == 1):
        group_name = event.text
        write_msg_k(event.user_id,"Выберите день",board1.get_keyboard())
    if(index == 2):
        if event.text == "Сегодня":
            date = get_day(today)
        elif event.text == "Завтра":
            date = get_day(today + timedelta(days=1))
        elif event.text == "Вчера":
            data = get_day(today - timedelta(days=1))
        else:
            write_msg(event.user_id,"Выберите день")
            index = 1
    index+=1
    if(index == 3):
        index = 1
        try:
            sc = get_schedule(date,group_name)
            print(sc)
            write_msg(event.user_id,sc)
        except:
            pass
        write_msg(event.user_id,"Введите название группы")
        
    indexes[event.user_id]['index'] = index
    indexes[event.user_id]['group'] = group_name
    indexes[event.user_id]['date'] = date

# Основной цикл
def loop():
    vk = vk_api.VkApi(token=token)
    api = vk.get_api()
    longpoll = VkLongPoll(vk)
    for event in longpoll.listen():
        try:
            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:
            
                # Если оно имеет метку для меня( то есть бота)
                if event.to_me:
                    if not indexes.get(event.user_id):
                        indexes[event.user_id] = dict()
                        indexes[event.user_id]['index'] = 0
                        indexes[event.user_id]['group'] = ""
                        indexes[event.user_id]['date'] = ""
                    tr = threading.Thread(target=dialogue, args=(event,))
                    tr.start()
                    #dialogue(event)
        except:
            loop()

loop()