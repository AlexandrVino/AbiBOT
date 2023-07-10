import json
from pathlib import Path

from config_consts import PROJECT_PATH


class Storage:
    path: Path = f"{PROJECT_PATH}/storage.json"
    storage: dict = {}

    def __init__(self):
        self.load_local_storage()

    def write_local_storage(self):
        with open(self.path, 'w', encoding='utf8') as output_file:
            json.dump(self.storage, output_file)

    def load_local_storage(self):
        with open(self.path, 'r', encoding='utf8') as input_file:
            self.storage = json.load(input_file)

    def create_user(self, user_id, username='', first_name='', last_name='', snils=None):
        if self.storage.get(str(user_id)):
            return

        self.storage[str(user_id)] = {
            'user_id': user_id, 'username': username, 'first_name': first_name,
            'last_name': last_name, 'is_active': True, 'snils': snils,
            'notify_time': 60 * 30,
            'universities': {}  # {university_name:  [(program_name, url), ...]}
        }
        self.write_local_storage()

    def update_user(self, user_id, **kwargs):
        for key, value in kwargs.items():
            self.storage[str(user_id)][key] = value
        self.write_local_storage()

    def add_university(self, user_id, university):
        if not self.storage[str(user_id)]['universities'].get(university):
            self.storage[str(user_id)]['universities'][university] = []
            self.write_local_storage()

    def update_university_program(self, user_id, **kwargs):
        self.add_university(user_id, kwargs['university'])
        if not self.storage[str(user_id)]['universities'].get(kwargs['university']):
            self.storage[str(user_id)]['universities'][kwargs['university']] = []

        self.storage[str(user_id)]['universities'][kwargs['university']].append(
            {k: v for k, v in kwargs.items() if k != 'university'}
        )
        self.write_local_storage()

    def __repr__(self):
        return f'STORAGE<storage={self.storage}>'


STORAGE = Storage()
