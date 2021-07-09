from extensions import db


def seed_artists():
    print('seeding artists')
    artists = [{
    "id": 4,
    "name": "Guns N Petals",
    }, {
        "id": 5,
        "name": "Matt Quevedo",
    }, {
        "id": 6,
        "name": "The Wild Sax Band",
    }]
    for artist in artists:
        try:
            db.session.add(artist)
            db.session.commit()
            print('Successfully added', artist)
        except:
            db.session.rollback()
            print('Error with inserting', artist)

def seed_venues():
    print('seeding venue')

def seed_shows():
    print('seeding shows')


if __name__ == '__main__':
    seed_artists()
    seed_shows()
    seed_venues()
