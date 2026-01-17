import sqlite3
import os
from typing import List, Dict, Any


class DatabaseManager:
    def __init__(self, db_path: str = None):
        # Автоматически определяем правильный путь
        if db_path is None:
            # Путь относительно расположения файла db_manager.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, 'travel_bot.db')
        else:
            self.db_path = db_path

        print(f"📁 Подключаемся к базе: {self.db_path}")
        print(f"📁 Файл существует: {os.path.exists(self.db_path)}")

    def _get_connection(self):
        """Получение соединения с базой данных"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"❌ Файл базы данных не найден: {self.db_path}")

        return sqlite3.connect(self.db_path)

    def get_attraction(self, attraction_id: int) -> Dict[str, Any]:
        """Получение достопримечательности по ID"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attractions WHERE id = ?', (attraction_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_attractions(self) -> List[Dict[str, Any]]:
        """Получение всех достопримечательностей"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attractions ORDER BY name')
            return [dict(row) for row in cursor.fetchall()]

    def get_attractions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Получение достопримечательностей по категории"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attractions WHERE category = ? ORDER BY name', (category,))
            return [dict(row) for row in cursor.fetchall()]

    def get_random_attraction(self) -> Dict[str, Any]:
        """Получение случайной достопримечательности"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attractions ORDER BY RANDOM() LIMIT 1')
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_route(self, route_id: int) -> Dict[str, Any]:
        """Получение маршрута по ID"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_route_attractions(self, route_id: int) -> List[Dict[str, Any]]:
        """Получение достопримечательностей маршрута"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.* FROM attractions a
                JOIN route_attractions ra ON a.id = ra.attraction_id
                WHERE ra.route_id = ?
                ORDER BY ra.order_index
            ''', (route_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_routes(self) -> List[Dict[str, Any]]:
        """Получение всех маршрутов"""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM routes ORDER BY name')
            return [dict(row) for row in cursor.fetchall()]

    def get_all_route_attractions(self):
        query = """
        SELECT ra.route_id, r.name as route_name, 
               a.id as attraction_id, a.name as attraction_name,
               ra.order_index
        FROM route_attractions ra
        JOIN routes r ON ra.route_id = r.id
        JOIN attractions a ON ra.attraction_id = a.id
        ORDER BY ra.route_id, ra.order_index
        """
        return self.fetch_all(query)

    def fetch_all(self, query, params=None):
        """Универсальный метод для SELECT-запросов"""
        if params is None:
            params = ()
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    def add_favorite(self, user_id: int, attraction_id: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO user_favorites (user_id, attraction_id)
                VALUES (?, ?)
            """, (user_id, attraction_id))
            conn.commit()

    def remove_favorite(self, user_id: int, attraction_id: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM user_favorites
                WHERE user_id = ? AND attraction_id = ?
            """, (user_id, attraction_id))
            conn.commit()

    def get_favorites(self, user_id: int) -> List[Dict]:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.* FROM attractions a
                JOIN user_favorites uf ON a.id = uf.attraction_id
                WHERE uf.user_id = ?
                ORDER BY uf.added_at DESC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    def is_favorite(self, user_id: int, attraction_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM user_favorites
                WHERE user_id = ? AND attraction_id = ?
            """, (user_id, attraction_id))
            return cursor.fetchone() is not None