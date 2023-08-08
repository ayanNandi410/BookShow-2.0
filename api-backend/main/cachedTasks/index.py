from ..models import Venue
from main.db import db
from app import cache

def UniqueList(d):
    L = []
    for x in d:
        if x.city not in L:
            L.append(x.city)
    return L

@cache.cached(timeout=300, key_prefix="getAllCities")
def get_all_cities():
    cities = db.session.query(Venue.city).all()
    return UniqueList(cities)