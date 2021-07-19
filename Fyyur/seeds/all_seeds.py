from Fyyur.utilities.helper_func import insert
from Fyyur.seeds.artist_data import artists
from Fyyur.seeds.venue_data import venues
from Fyyur.seeds.show_data import shows


def seed_artists(db):
    print('seeding artists')
    for artist in artists:
        print(artist)
        insert(db, artist)


def seed_venues(db):
    print('seeding venue')
    for venue in venues:
        insert(db, venue)


def seed_shows(db):
    print('seeding shows')
    for show in shows:
        insert(db, show)


if __name__ == '__main__':
    seed_artists()
    seed_shows()
    seed_venues()
