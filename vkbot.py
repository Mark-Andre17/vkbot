from vk_api.longpoll import VkLongPoll, VkEventType
from vkinder import VkUser
from Send_messages import TOKEN, vk, write_msg, send_photo
from databaseVK import session, Candidates

longpoll = VkLongPoll(vk)


def speak_vk_bot():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            request = event.text.lower()

            if request == 'привет':
                write_msg(event.user_id, 'Привет! Найти тебе кандидата?')

                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        request = event.text.lower()

                        if request == 'нет':
                            write_msg(event.user_id, 'Хорошо, напиши мне "Привет", когда передумаешь ;)')
                            break
                        elif request != 'нет' and request != 'да':
                            write_msg(event.user_id, 'Я не понимаю вашего ответа, напишите мне "Да" или "Нет"')
                        elif request == 'да':
                            write_msg(event.user_id,
                                      'Выберите пол кандидата из списка:\n1 - женщина;\n2 - мужчина;\n0 - неважно.')
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    request = event.text.lower()
                                    sex = int(request)
                                    if int(request) > 2:
                                        write_msg(event.user_id, 'Вы ввели неверную цифру')
                                    else:
                                        write_msg(
                                            event.user_id,
                                            'Вы семейное положение из списка:\n1 - не женат(не замужем);'
                                            '\n2 - встречается;\n3 - помолвлен(-а);\n4 - женат (замужем);'
                                            '\n5 - всё сложно;\n6 - в активном поиске;'
                                            '\n7 - влюблен(-а);\n8 - в гражданском браке.'
                                        )
                                        for event in longpoll.listen():
                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                request = event.text.lower()
                                                status = int(request)
                                                if int(request) > 8:
                                                    write_msg(event.user_id, 'Вы ввели неверную цифру')
                                                else:
                                                    write_msg(event.user_id, 'Введите минимальный возраст кандидата')
                                                    for event in longpoll.listen():
                                                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                            request = event.text.lower()
                                                            age_from = int(request)
                                                            if int(request) < 0:
                                                                write_msg(event.user_id, 'Вы ввели неверную цифру')
                                                            else:
                                                                write_msg(event.user_id,
                                                                          'Введите максимальный возраст кандидата')
                                                            for event in longpoll.listen():
                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                    request = event.text.lower()
                                                                    age_to = int(request)
                                                                    if int(request) < 0:
                                                                        write_msg(event.user_id,
                                                                                  'Вы ввели неверную цифру')
                                                                    else:
                                                                        write_msg(event.user_id, 'Поехали!')
                                                                        vk_client = VkUser(TOKEN, '5.130')
                                                                        get_user_info = vk_client.get_user_info(
                                                                            event.user_id)
                                                                        users_search = vk_client.users_search(
                                                                            get_user_info, sex, status, age_from,
                                                                            age_to)
                                                                        sess = session()
                                                                        sess.query(
                                                                            Candidates).delete()
                                                                        candidates_list = []
                                                                        while True:
                                                                            for candidate_id in users_search:
                                                                                get_photos = vk_client.get_photos(
                                                                                    candidate_id)
                                                                                get_attachments = vk_client.messages_send(
                                                                                    get_photos, candidate_id)
                                                                                send_photo(event.user_id,
                                                                                           f'Кандидат vk.com/id{candidate_id}',
                                                                                           get_attachments)
                                                                                users_search.remove(candidate_id)
                                                                                candidates_data = Candidates(
                                                                                    name=f'vk.com/id{candidate_id}')
                                                                                sess.add(candidates_data)
                                                                                sess.commit()
                                                                                add_result = sess.query(
                                                                                    Candidates).all()
                                                                                for item in add_result:
                                                                                    name = item.name
                                                                                    candidates_list.append(name)
                                                                                write_msg(
                                                                                    event.user_id,
                                                                                    'Продолжить поиск?')

                                                                                for event in longpoll.listen():
                                                                                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                                        request = event.text.lower()

                                                                                        if request == 'да':
                                                                                            break
                                                                                        else:
                                                                                            write_msg(
                                                                                                event.user_id,
                                                                                                f'Поиск закончен. '
                                                                                                f'Вот список всех '
                                                                                                f'найденных '
                                                                                                f'пользователей:'
                                                                                                f'{candidates_list} '
                                                                                            )
                                                                            break
