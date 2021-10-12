import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = ''
vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})


def send_photo(user_id, message, attachments):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': ','.join(attachments),
                                'random_id': randrange(10 ** 7), })
