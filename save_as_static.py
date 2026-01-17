# save_as_static.py — положи в корень проекта и запусти
import json
import os
from database.data_manager import DataManager

data_manager = DataManager()

# Получаем все данные
routes = data_manager.get_all_routes()
route_attractions = data_manager.get_all_route_attractions()
attractions = data_manager.get_all_attractions()

# Собираем маршруты с местами
full_routes = []
for route in routes:
    places = [a for a in route_attractions if a['route_id'] == route['id']]
    full_routes.append({
        "id": route['id'],
        "name": route['name'],
        "description": route['description'],
        "duration": route.get('duration', '2-3 часа'),
        "places_count": len(places),
        "places": [p['attraction_name'] for p in places]
    })

# Сохраняем в папку webapp
os.makedirs("webapp/static", exist_ok=True)

with open("webapp/static/data.json", "w", encoding="utf-8") as f:
    json.dump({
        "routes": full_routes,
        "attractions": attractions
    }, f, ensure_ascii=False, indent=2)

print("data.json успешно создан! Теперь можно заливать на GitHub Pages")