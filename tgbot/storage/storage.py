import json
from pathlib import Path

from config_consts import PROJECT_PATH


class Storage:
    _path: Path = f"{PROJECT_PATH}/storage.json"
    _storage: dict = {}

    def __init__(self):
        self.load_local_storage()

    def write_local_storage(self):
        with open(self._path, 'w', encoding='utf8') as output_file:
            json.dump(self._storage, output_file)

    def load_local_storage(self):
        with open(self._path, 'r', encoding='utf8') as input_file:
            self._storage = json.load(input_file)

    def create_user(self, user_id, username='', first_name='', last_name='', snils=None):
        if self._storage.get(str(user_id)):
            return

        self._storage[str(user_id)] = {
            'user_id': user_id, 'username': username, 'first_name': first_name,
            'last_name': last_name, 'is_active': True, 'snils': snils,
            'notify_time': 120, 'sum_points': 0,
            'universities': {}  # {university_name:  [(program_name, url), ...]}
        }
        self.write_local_storage()

    def update_user(self, user_id, **kwargs):
        for key, value in kwargs.items():
            self._storage[str(user_id)][key] = value
        self.write_local_storage()

    def add_university(self, user_id, university):
        if not self._storage[str(user_id)]['universities'].get(university):
            self._storage[str(user_id)]['universities'][university] = []
            self.write_local_storage()

    def update_university_program(self, user_id, **kwargs):
        self.add_university(user_id, kwargs['university'])
        if not self._storage[str(user_id)]['universities'].get(kwargs['university']):
            self._storage[str(user_id)]['universities'][kwargs['university']] = []

        self._storage[str(user_id)]['universities'][kwargs['university']].append(
            {k: v for k, v in kwargs.items() if k != 'university'}
        )
        self.write_local_storage()

    def get_users(self):
        return self._storage.items()

    def get_user_by_id(self, user_id):
        return self._storage.get(user_id)

    def __repr__(self):
        return f'STORAGE<storage={self._storage}>'


STORAGE = Storage()
