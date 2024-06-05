function fetchData(){
    $.get('update_data',function(response){
        $('#data-container').text(response.data);
    });
}
setInterval(fetchData,1000);

function copy() {
    let textarea = document.getElementById("data-container");
    textarea.select();
    document.execCommand("copy");

    // Get the snackbar DIV
  var x = document.getElementById("snackbar");

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
  }

function saveText() {
  // Get the snackbar DIV
  var x = document.getElementById("snackbar2");

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

document.addEventListener("DOMContentLoaded", function() {
    var playButton = document.getElementById("play-button");
    if (playButton) {
        playButton.addEventListener("click", function(event) {
            event.preventDefault();
            fetch('/playsound_route')
                .then(response => {
                    if (response.ok) {
                        // The request was successful, but we don't need to do anything with the response
                        return;
                    }
                    throw new Error('Network response was not ok');
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    var playButton = document.getElementById("reset-button");
    if (playButton) {
        playButton.addEventListener("click", function(event) {
            event.preventDefault();
            fetch('/reset')
                .then(response => {
                    if (response.ok) {
                        // The request was successful, but we don't need to do anything with the response
                        return;
                    }
                    throw new Error('Network response was not ok');
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    var playButton = document.getElementById("save-button");
    if (playButton) {
        playButton.addEventListener("click", function(event) {
            event.preventDefault();
            fetch('/save')
                .then(response => {
                    if (response.ok) {
                        // The request was successful, but we don't need to do anything with the response
                        return;
                    }
                    throw new Error('Network response was not ok');
                })
                .then(() => {
                    // Call your JavaScript function here without parameters
                    saveText();
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
});