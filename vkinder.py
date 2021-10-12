import requests

TOKEN_FOR_VKUSER = ''


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = TOKEN_FOR_VKUSER
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_user_info(self, user_id):
        user_info_url = self.url + 'users.get'
        user_params = {
            'user_ids': user_id,
            'fields': 'city',
            'name_case': 'nom'
        }
        response = requests.get(user_info_url, params={**self.params, **user_params}).json()
        return response

    def users_search(self, get_user_info, sex, status, age_from, age_to):
        candidate_id_list = []
        for items in get_user_info['response']:
            city_id = items.get('city')['id']
        users_search_url = self.url + 'users.search'
        user_params = {
            'count': 10,
            'sex': sex,
            'city': city_id,
            'status': status,
            'age_from': age_from,
            'age_to': age_to
        }
        response = requests.get(users_search_url, params={**self.params, **user_params}).json()
        candidate_id_list = [item.get('id') for item in response['response']['items']]
        return candidate_id_list

    def get_photos(self, candidate_id):
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': candidate_id,
            'album_id': 'profile',
            'extended': '1',
            'count': '1000',
            'photo_sizes': '1'
        }
        response = requests.get(photos_url, params={**self.params, **photos_params}).json()
        photo_list = []
        most_popular_photo_list = []
        for value in response.values():
            items = value.get('items')
            for item in items:
                like_id_list = []
                likes = item.get('likes')
                like = likes.get('count')
                like_id_list.append(like)
                photo_id = item.get('id')
                like_id_list.append(photo_id)
                photo_list.append(like_id_list)
        photo_list.sort()
        if len(photo_list) >= 3:
            most_popular_photo_list.append(photo_list[-1])
            most_popular_photo_list.append(photo_list[-2])
            most_popular_photo_list.append(photo_list[-3])
        elif len(photo_list) == 2:
            most_popular_photo_list.append(photo_list[-1])
            most_popular_photo_list.append(photo_list[-2])
        else:
            most_popular_photo_list.append(photo_list[-1])
        return most_popular_photo_list

    @staticmethod
    def messages_send(get_photos, candidate_id):
        if len(get_photos) == 3:
            photo_1 = f'photo{candidate_id}_{get_photos[0][1]}'
            photo_2 = f'photo{candidate_id}_{get_photos[1][1]}'
            photo_3 = f'photo{candidate_id}_{get_photos[2][1]}'
            attachments = [photo_1, photo_2, photo_3]
        elif len(get_photos) == 2:
            photo_1 = f'photo{candidate_id}_{get_photos[0][1]}'
            photo_2 = f'photo{candidate_id}_{get_photos[1][1]}'
            attachments = [photo_1, photo_2]
        elif len(get_photos) == 1:
            photo_1 = f'photo{candidate_id}_{get_photos[0][1]}'
            attachments = [photo_1]
        return attachments
