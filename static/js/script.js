async function fetchSong() {
    try {
        const response = await fetch('/song');
        const data = await response.json();
        if (!data.error && data.cover) {
            document.getElementById('album-cover').src = data.cover;
            document.getElementById('song-info').innerText = `${data.song} - ${data.artist}`;
        } else {
            document.getElementById('song-info').innerText = "No song currently playing";
            document.getElementById('album-cover').src = ""; // Reset image if no song
        }
    } catch (error) {
        console.error('Error fetching song:', error);
    }
}

setInterval(fetchSong, 5000); // Update every 5 seconds
fetchSong();

//Toggle vinyl position when clicked
let vinylMoved = false;

function toggleVinylPosition() {
    const vinyl = document.querySelector('.vinyl-spinner');
    const albumCover = document.querySelector('#album-cover');

    if (vinylMoved) {
        vinyl.style.left = '40%';
        vinyl.style.animationPlayState = 'running';
        albumCover.style.zIndex = '1'; //Moves album cover behind 
        vinyl.style.zIndex = '2'; //Brings vinyl to the top
    } else {
        vinyl.style.left = '20%';
        vinyl.style.animationPlayState = 'paused'; // Stop spinning when fully outside
        albumCover.style.zIndex = '2'; //Bring album cover to the top
        vinyl.style.zIndex = '1'; //Move vinyl behind the album
    }

    vinylMoved = !vinylMoved;
}

// Attach click event to the album cover
document.querySelector("#album-cover").addEventListener("click", toggleVinylPosition);