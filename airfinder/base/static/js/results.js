
const heartIcons = document.querySelectorAll(".like-button .heart-icon");


// Attach event listener to each heart icon
heartIcons.forEach(heartIcon => {
  heartIcon.addEventListener("click", () => {
    heartIcon.classList.toggle("liked");
    const listingId = heartIcon.dataset.listingId;
    const liked = heartIcon.classList.contains("liked");
    toggleLike(listingId, liked);
  });
});

function toggleLike(listingId, liked) {
  fetch('/toggle-like', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is sent with request
    },
    body: JSON.stringify({ listingId, liked })
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