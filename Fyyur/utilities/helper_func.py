from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue


def format_genres(genres):
    return genres.replace('{', '').replace('}', '').replace('"', '')


def setup_show_form(form, default_artist='', default_venue=''):
    form.artist_id.choices = [(a.id) for a in Artist.query.all()]
    if default_artist != '':
        form.artist_id.default = default_artist
        form.artist_id.data = default_artist
        form.artist_id.process([])

    form.venue_id.choices = [(v.id) for v in Venue.query.all()]
    if default_venue != '':
        form.venue_id.default = default_venue
        form.venue_id.data = default_venue
        form.venue_id.process([])
    return form


def insert(db, record, success_msg='Successfully inserted into database',
           error_msg='Error with inserting into database'):
    try:
        db.session.add(record)
        db.session.commit()
        print(success_msg)
        result = success_msg
    except Exception as e:
        db.session.rollback()
        print(error_msg)
        print(e)
        result = error_msg
    finally:
        db.session.close()
    return result


def update(db, entity, id, obj, success_msg='Successfully updated record',
           error_msg='Error with updating record'):
    try:
        db.session.query(entity).filter(entity.id == id).\
            update(obj, synchronize_session="fetch")
        db.session.commit()
        result = success_msg
        print(result)
    except Exception as e:
        db.session.rollback()
        result = error_msg
        print(result, e)
    finally:
        db.session.close()
    return result


def delete(db, record, success_msg='Successfully deleted record',
           error_msg='Error with deleting record'):
    try:
        db.session.delete(record)
        db.session.commit()
        print(success_msg)
        result = success_msg
    except Exception as e:
        db.session.rollback()
        print(error_msg, e)
        result = error_msg
    finally:
        db.session.close()
    return result
