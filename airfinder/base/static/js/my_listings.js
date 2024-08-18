const Deletes = document.querySelectorAll(".delete-link");

// Attach event listener to each delete icon
Deletes.forEach(Delete => {
    Delete.addEventListener("click", () => {
      const listingId = Delete.dataset.listingId;
      toggleDelete(listingId);
    });
  });

  function toggleDelete(listingId) {
    fetch('/toggle-delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is sent with request
      },
      body: JSON.stringify({ listingId })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }  


