from main.db import db

from flask_caching import Cache
cache = Cache() # cache is imported from this file to use anywhere

def UniqueList(d):
    L = []
    for x in d:
        if x.city not in L:
            L.append(x.city)
    return L

@cache.cached(timeout=300, key_prefix="getAllCities")
def get_all_cities():
    from main.models import Venue
    cities = db.session.query(Venue.city).all()

    return UniqueList(cities)


@cache.memoize(timeout=300)
def getShowsByName(name):
    from main.models import Show
    shows = db.session.query(Show).filter(Show.name.ilike(f'%{name}%')).all()
    return shows