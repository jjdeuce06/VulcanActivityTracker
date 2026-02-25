function logout() {
      fetch('/login_api/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => {
        if (response.ok) {
          window.location.href = "/login";
        } else {
          alert('Logout failed. Please try again.');
        }
      }).catch(error => {
        console.error('Error during logout:', error);
        alert('An error occurred. Please try again.');
      });
    }