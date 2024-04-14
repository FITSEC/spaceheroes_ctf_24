function validateTokenAndFetchData(id, token) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: 'validate_token.php',
      type: 'POST',
      dataType: 'json',
      data: { id: id, token: token },
      success: function(response) {
          //console.log('Validation Response:', response)
          if (response && response.valid === true) {
    getUsernameFromDatabase(id)
      .then(usernameResponse => {
        if (Array.isArray(usernameResponse)) {
          //console.log('api-response:',usernameResponse)
          resolve(usernameResponse); // Access username only if array
        } else {
          // Handle case where usernameResponse is not an array
          console.error('Unexpected response format from getUsernameFromDatabase');
          // Decide how to proceed (e.g., reject the promise)
        }
      })
      .catch(reject);
        } else {
          //console.error('validate else call');
          reject(new Error('Invalid token or ID mismatch call from js file to validate.php'));
        }
      },
      error: function(xhr, status, error) {
        //console.error('Error validating token:', error);
        reject(error);
      }
    });
  });
}

function getUsernameFromDatabase(id) {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: 'api.php',
      type: 'POST',
      dataType: 'json',
      data: { id: id }, 
      success: function(response) {
        resolve(response);
      },
      error: function(xhr, status, error) {
        reject(error);
      }
    });
  });
}

const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');
const token = urlParams.get('token');

if (token) {
  validateTokenAndFetchData(id, token)
    .then(response => {
      sessionStorage.setItem('username', response[0].username);

      // Update welcome message
      const welcomeMessage = document.getElementById('welcomeMessage');
      if (sessionStorage.getItem('username')) {
        welcomeMessage.textContent = "Welcome, " + sessionStorage.getItem('username') + "!";
      } else {
        console.error('Username not found in session storage');
      }
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      // Handle error (e.g., redirect to login or display an error message)
      window.location.href = 'login.php'; // Example error handling
    });
} else {
  console.error('Missing token');
  window.location.href = 'login.php';
}

