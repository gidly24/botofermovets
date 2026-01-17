import math


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Расчет расстояния между двумя точками в километрах
    Используем формулу гаверсинусов
    """
    R = 6371  # Радиус Земли в км

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return round(distance, 2)


def create_yandex_map_link(lat: float, lon: float, place_name: str = "") -> str:
    """Создание ссылки на Яндекс Карты"""
    name_param = f"&text={place_name}" if place_name else ""
    return f"https://yandex.ru/maps/?pt={lon},{lat}&z=15{name_param}"


def create_google_map_link(lat: float, lon: float, place_name: str = "") -> str:
    """Создание ссылки на Google Maps"""
    name_param = f"&q={place_name}" if place_name else ""
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}{name_param}"


def find_nearby_attractions(user_lat: float, user_lon: float, attractions: dict, max_results: int = 5):
    """Нахождение ближайших достопримечательностей"""
    attractions_with_distance = []

    for attr_id, attraction in attractions.items():
        if attraction.get('coordinates'):
            lat, lon = attraction['coordinates']
            dist = calculate_distance(user_lat, user_lon, lat, lon)
            attractions_with_distance.append((dist, attr_id, attraction))

    # Сортируем по расстоянию
    attractions_with_distance.sort(key=lambda x: x[0])

    return [(attr_id, attr, dist) for dist, attr_id, attr in attractions_with_distance[:max_results]]