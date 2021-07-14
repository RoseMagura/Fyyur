const deleteArtist = event => {
  fetch("/artists/" + event.target.value, { method: "DELETE" })
    .then(
      setTimeout(() => {
        window.location.href = "/artists";
      }, 1000)
    );
}

const deleteVenue = e => {
  venueId = e.target.value;
  fetch("/venues/" + venueId, { method: "DELETE" })
    .then(
      setTimeout(() => {
        window.location.href = "/venues";
      }, 1000)
    );
}

const deleteShow = evt => {
  const showId = evt.target.value;
  fetch("/shows/" + showId, { method: "DELETE" })
    .then(
      setTimeout(() => {
        window.location.href = "/shows";
      }, 1000)
    );
}

const openForm = () => {
  location.pathname += '/edit';
}

const deleteArtistBtn = document.getElementById('delete-artist');
const editBtns = document.getElementsByClassName('edit');

const deleteShowBtns = document.getElementsByClassName('delete-show');

const deleteVenueBtn = document.getElementById('delete-venue');

if (deleteArtistBtn !== null) {
  deleteArtistBtn.addEventListener('click', deleteArtist);
}

for (let i = 0; i < editBtns.length; i++) {
  editBtns[i].addEventListener('click', openForm);
}

if (deleteVenueBtn !== null) {
  deleteVenueBtn.addEventListener('click', deleteVenue);
}

for (let counter = 0; counter < deleteShowBtns.length; counter++) {
  deleteShowBtns[counter].addEventListener('click', deleteShow);
}