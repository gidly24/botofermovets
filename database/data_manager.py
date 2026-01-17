# database/data_manager.py — ИСПРАВЛЕННАЯ ВЕРСИЯ (всё остальное оставь как есть!)

import os
import sys

# Добавляем корень проекта и папку database в путь
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, current_dir)  # ← Это ключевая строчка!

# Теперь импорт работает из любой точки
from db_manager import DatabaseManager


class DataManager:
    def __init__(self):
        db_path = os.path.join(current_dir, 'travel_bot.db')
        self.db = DatabaseManager(db_path)
        print(f"DataManager инициализирован: {db_path}")
        print(f"Файл существует: {os.path.exists(db_path)}")

    def get_attraction(self, attraction_id: int):
        return self.db.get_attraction(attraction_id)

    def get_all_attractions(self):
        return self.db.get_all_attractions()

    def get_attractions_by_category(self, category: str):
        return self.db.get_attractions_by_category(category)

    def get_random_attraction(self):
        return self.db.get_random_attraction()

    def get_route(self, route_id: int):
        return self.db.get_route(route_id)

    def get_route_attractions(self, route_id: int):
        return self.db.get_route_attractions(route_id)

    def get_all_routes(self):
        return self.db.get_all_routes()
    def get_all_route_attractions(self):
        return self.db.get_all_route_attractions()

    # Для обратной совместимости со старым кодом
    @property
    def attractions(self):
        """Возвращает словарь с достопримечательностями в старом формате"""
        all_attrs = self.get_all_attractions()
        result = {}
        for attr in all_attrs:
            result[str(attr['id'])] = {
                'name': attr['name'],
                'description': attr['description'],
                'address': attr['address'],
                'price': attr['price'],
                'work_time': attr['work_time'],
                'coordinates': [attr['latitude'], attr['longitude']],
                'category': attr['category'],
                'tags': attr['tags'].split(',') if attr['tags'] else []
            }
        return result

    @property
    def routes(self):
        """Возвращает маршруты в старом формате"""
        all_routes = self.get_all_routes()
        result = {}
        for route in all_routes:
            attractions_list = self.get_route_attractions(route['id'])
            result[str(route['id'])] = {
                'name': route['name'],
                'description': route['description'],
                'duration': route['duration'],
                'difficulty': route['difficulty'],
                'category': route['category'],
                'attractions': [str(attr['id']) for attr in attractions_list]
            }
        return result