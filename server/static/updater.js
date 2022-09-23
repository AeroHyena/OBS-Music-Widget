// This file listens to the backend, and updates the widget when a new song has started playing

// Use this function to force an image update without refreshing the page
function refresh_image(url)
{
    let timestamp = new Date().getTime();
    let image = document.getElementById("cover_art");
    let query_string = "?t=" + timestamp; 
    image.src = url + query_string
}



const socket = new WebSocket("ws://" + location.host + "/update");
const image_url = "http://localhost:5000/static/image.jpg"
console.log("Communication between server and browser is initialized")




// Listen for data being pushed from the backend
socket.addEventListener("message", package => {
    let song = "";
    let artists = "";
    let artists_done = false;

    // Seperate data into song and artists variables
    for (let i = 0; i < package.data.length; i++)
    {
        if (artists_done == false)
        {
            // Artists
            while (package.data[i] != ";")
            {
                artists += package.data[i];
                i++;
            };
            i++;
            artists_done = true;
        };

        // Song
        song += package.data[i]
    };

    // Update widget
    refresh_image(image_url)
    document.getElementById("song_title").innerHTML = song;
    document.getElementById("artists").innerHTML = artists;
    console.log("Widget is successfully updated")
});
