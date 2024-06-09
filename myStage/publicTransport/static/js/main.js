// Function to initialize the Google Map and handle form submission for finding routes.
function initMap() {
  // Create a new map centered around Nairobi
  var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
      center: {lat: -1.2921, lng: 36.8219}  // Default center around Nairobi
  });

  // Initialize the DirectionsService and DirectionsRenderer objects
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);

  // Event listener for the form submission to find the route
  document.getElementById('destination-form').addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent the default form submission
      var destinationId = document.getElementById('id_destination').value; // Get the destination ID from the form

      // Check if the browser supports geolocation
      if (navigator.geolocation) {
          // Get the user's current location
          navigator.geolocation.getCurrentPosition(function(position) {
              var userLocation = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude
              };

              // Fetch the nearest station using an API call
              fetch('/get_nearest_station/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: JSON.stringify({destination_id: destinationId})
              })
              .then(response => response.json())
              .then(data => {
                  if (data.error) {
                      alert(data.error);
                  } else {
                      var stationLocation = {
                          lat: data.latitude,
                          lng: data.longitude
                      };

                      // Request directions from the user's location to the nearest station
                      directionsService.route({
                          origin: userLocation,
                          destination: stationLocation,
                          travelMode: 'WALKING'
                      }, function(response, status) {
                          if (status === 'OK') {
                              directionsRenderer.setDirections(response);
                              
                              // Fetch and display SACCO information
                              fetch('/get_sacco_info/', {
                                  method: 'POST',
                                  headers: {
                                      'Content-Type': 'application/json',
                                      'X-CSRFToken': getCookie('csrftoken')
                                  },
                                  body: JSON.stringify({destination_id: destinationId})
                              })
                              .then(response => response.json())
                              .then(saccoData => {
                                  var saccoInfo = document.getElementById('sacco-info');
                                  saccoInfo.innerHTML = `
                                      <h3>Sacco Information</h3>
                                      <p><strong>Sacco Name:</strong> ${saccoData.sacco_name}</p>
                                      <p><strong>Sacco Number:</strong> ${saccoData.sacco_number}</p>
                                  `;
                              });
                          } else {
                              window.alert('Directions request failed due to ' + status);
                          }
                      });
                  }
              });
          }, function() {
              handleLocationError(true, map.getCenter());
          });
      } else {
          handleLocationError(false, map.getCenter());
      }
  });
}

// Function to handle geolocation errors
function handleLocationError(browserHasGeolocation, pos) {
  window.alert(browserHasGeolocation ?
                'Error: The Geolocation service failed.' :
                'Error: Your browser doesn\'t support geolocation.');
}

// Utility function to get the CSRF token from cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // check if cookie string begin with the name we want
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
