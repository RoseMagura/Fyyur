
# #  Artists
# #  ----------------------------------------------------------------
# @app.route('/artists')
# def artists():
#   # TODO: replace with real data returned from querying the database
#   data = Artist.query.all()
#   return render_template('pages/artists.html', artists=data)

# @app.route('/artists/search', methods=['GET', 'POST'])
# def search_artists():
#     # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
#     # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
#     # search for "band" should return "The Wild Sax Band".
#     search_str = request.args.get('search_term')
#     artist_query = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_str)))
#     artist_list = artist_query.all()
#     results_list = []
#     for artist in artist_list:
#         data = {
#             'id': artist.id,
#             'name':  artist.name,
#             'num_upcoming_shows': artist.num_upcoming_shows
#         }
#         results_list.append(data)

#     response={
#     'count': len(artist_list),
#     'data': results_list
#     }
#     return render_template('pages/search_artists.html', results=response, search_term=search_str)

# @app.route('/artists/<int:artist_id>')
# def show_artist(artist_id):
#   # shows the venue page with the given venue_id
#   # TODO: replace with real venue data from the venues table, using venue_id
#     artist = Artist.query.get(artist_id)
#     past_list = []
#     upcoming_list = []
#     up_entry ={}
#     entry ={}
#     past_shows = 0
#     upcoming_shows = 0
#     shows = artist.shows
#     for show in shows:
#       if (show.start_time > datetime.now()):
#           upcoming_shows += 1
#           up_entry =     {
#               "venue_id": show.venue_id,
#               "venue_name": show.venue_name,
#               "venue_image_link": show.venue_image_link,
#               "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
#             }
#           upcoming_list.append(up_entry)
#       elif (show.start_time < datetime.now()):
#           past_shows += 1
#           entry =     {
#               "venue_id": show.venue_id,
#               "venue_name": show.venue_name,
#               "venue_image_link": show.venue_image_link,
#               "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
#             }
#           past_list.append(entry)
#     data={
#         "id": artist.id,
#         "name": artist.name,
#         "genres": artist.genres.split(','),
#         "city": artist.city,
#         "state": artist.state,
#         "phone": artist.phone,
#         "website": artist.website,
#         "facebook_link": artist.facebook_link,
#         "seeking_venue": artist.seeking_venue,
#         "seeking_description": artist.seeking_description,
#         "image_link": artist.image_link,
#         "past_shows": past_list,
#         "upcoming_shows": upcoming_list,
#         "past_shows_count": past_shows,
#         "upcoming_shows_count": upcoming_shows,
#     }
#     return render_template('pages/show_artist.html', artist=data)

# #  Update
# #  ----------------------------------------------------------------
# @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
# def edit_artist(artist_id):
#     artist = Artist.query.get(artist_id)
#     form = ArtistForm(request.form)
#     artist.name = form.name.data
#     artist.genres = form.genres.data
#     artist.city = form.city.data

#     # artist= Artist(
#     #     "id": artist_id,
#     #     "name": form.name.data,
#     #     "genres": form.genres.data,
#     #     "city": form.city.data,
#     #     "state": form.state.data,
#     #     "phone": form.phone.data,
#     #     "facebook_link": form.facebook_link.data,
#     #     "image_link":'https://i.guim.co.uk/img/media/ad98f2dc808f18131e35e59c05ba6212671e8227/94_0_3061_1838/master/3061.jpg?width=1920&quality=85&auto=format&fit=max&s=c515d483b75926f0d68512f263c2c26f',
#     # )
#     # try:
#     db.session.add(artist)
#     db.session.commit()
#     flash('Updated artist information')
#     # except:
#     #     db.session.rollback()
#     #     flash('Error. Could not update artist information')
#     # finally:
#     #     db.session.close()
#     return render_template('forms/edit_artist.html', form=form, artist=artist)

# @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
# def edit_artist_submission(artist_id):
#     # TODO: take values from the form submitted, and update existing
#     # artist record with ID <artist_id> using the new attributes
#     form = ArtistForm(request.form)
#     artist = Artist.query.get(artist_id)
#     artist = {
#             "id": artist.id,
#             "name": artist.name,
#             "genres": artist.genres.split(','),
#             "city": artist.city,
#             "state": artist.state,
#             "phone": artist.phone,
#             "website": artist.website,
#             "facebook_link": artist.facebook_link,
#             "seeking_venue": artist.seeking_venue,
#             "seeking_description": artist.seeking_description,
#             "image_link": artist.image_link,
#             # "past_shows": past_list,
#             # "upcoming_shows": upcoming_list,
#             # "past_shows_count": past_shows,
#             # "upcoming_shows_count": upcoming_shows
#     }
#     return redirect(url_for('show_artist', artist_id=artist_id))

# @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
# def edit_venue(venue_id):
#   form = VenueForm(request.form)
#   v = Venue.query.get(venue_id)
#   venue={
#     "id": v.id,
#     "name": v.name,
#     "genres": v.genres,
#     "address": v.address,
#     "city": v.city,
#     "state": v.state,
#     "phone": v.phone,
#     "website": v.website,
#     "facebook_link": v.facebook_link,
#     "seeking_talent": v.seeking_talent,
#     "seeking_description": v.seeking_description,
#     "image_link": v.image_link
#   }
#   # TODO: populate form with values from venue with ID <venue_id>
#   return render_template('forms/edit_venue.html', form=form, venue=venue)

# @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
# def edit_venue_submission(venue_id):
#   # TODO: take values from the form submitted, and update existing
#   # venue record with ID <venue_id> using the new attributes
#   return redirect(url_for('show_venue', venue_id=venue_id))

# #  Create Artist
# #  ----------------------------------------------------------------

# @app.route('/artists/create', methods=['GET'])
# def create_artist_form():
#   form = ArtistForm()
#   return render_template('forms/new_artist.html', form=form)

# @app.route('/artists/create', methods=['POST'])
# def create_artist_submission():
#     # called upon submitting the new artist listing form
#     # TODO: insert form data as a new Venue record in the db, instead
#     # TODO: modify data to be the data object returned from db insertion
#     form = ArtistForm(request.form)
#     num_artists = Artist.query.count()
#     artist = Artist(
#         id = num_artists + 4,
#         name = form.name.data,
#         genres = form.name.data,
#         city = form.city.data,
#         state = form.state.data,
#         phone = form.phone.data,
#         facebook_link = form.facebook_link.data,
#         website = form.website.data,
#         seeking_venue = form.seeking_venue.data,
#         seeking_description = form.seeking_description.data,
#         image_link = form.image_link.data
# )

#     try:
#         db.session.add(artist)
#         db.session.commit()
#         # on successful db insert, flash success
#         flash('Artist ' + request.form['name'] + ' was successfully listed!')
#     # TODO: on unsuccessful db insert, flash an error instead.
#     except:
#         flash('An error occurred. Artist ' + form.name + ' could not be listed.')
#         db.rollback()
#     finally:
#         db.session.commit()
#     return render_template('pages/home.html')
