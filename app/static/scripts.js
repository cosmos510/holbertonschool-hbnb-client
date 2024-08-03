// Function to get a cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// Function to check if the user is logged in
function isLoggedIn() {
  const token = getCookie('access_token');
  return !!token;
}

// Function to get the Authorization header
function getAuthHeader() {
  const token = getCookie('access_token');
  return token ? `Bearer ${token}` : '';
}

// Handle the login form submission
document.getElementById('login-form').addEventListener('submit', async function(event) {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const response = await fetch('/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
  });

  const data = await response.json();

  if (response.ok) {
      // Store the JWT token in a cookie
      document.cookie = `access_token=${data.access_token}; path=/; secure`;
      // Redirect to the home page
      window.location.href = '/';
  } else {
      alert('Invalid credentials');
  }
});

// Example of making a request to a protected route
async function fetchProtectedData() {
  const response = await fetch('/protected', {
      method: 'GET',
      headers: {
          'Authorization': getAuthHeader(),
      },
  });

  const data = await response.json();

  if (response.ok) {
      console.log('Protected data:', data);
  } else {
      console.log('Error fetching protected data:', data);
  }
}

// Display user status on the home page
document.addEventListener('DOMContentLoaded', (event) => {
  const userStatus = document.getElementById('user-status');

  if (userStatus) {
      if (isLoggedIn()) {
          userStatus.textContent = 'You are logged in!';
      } else {
          userStatus.textContent = 'You are not logged in. Please log in.';
      }
  }

  // Optionally fetch protected data on home page load
  if (isLoggedIn()) {
      fetchProtectedData();
  }
});
document.addEventListener('DOMContentLoaded', () => {
  fetch('/countries')
      .then(response => response.json())
      .then(data => {
          const countryFilter = document.getElementById('country-filter');
          data.forEach(country => {
              const option = document.createElement('option');
              option.value = country.code; // Ensure this matches your API response
              option.textContent = country.name;
              countryFilter.appendChild(option);
          });
      })
      .catch(error => {
          console.error('Error fetching countries:', error);
      });
});

document.addEventListener('DOMContentLoaded', function () {
  const reviewForm = document.getElementById('review-form');
  const placeId = new URLSearchParams(window.location.search).get('id');
  const reviewText = document.getElementById('review-text');
  const reviewRating = document.getElementById('review-rating');

  // Function to get a cookie by name
  function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
  }

  reviewForm.addEventListener('submit', async function (event) {
      event.preventDefault();

      const token = getCookie('jwt_token');
      const userId = getCookie('user_id');  // Get the user_id from the cookie

      if (!token) {
          console.error('User is not logged in');
          window.location.href = '/login';
          return;
      }

      if (!userId) {
          console.error('User ID is missing');
          console.log('Current cookies:', document.cookie);  // Debug log
          return;
      }

      const reviewData = {
          user_id: userId,  // Use the user_id from the cookie
          comment: reviewText.value,
          rating: reviewRating.value,
          place_id: placeId
      };

      console.log('Submitting review data:', reviewData);  // Debugging log
      console.log('JWT token:', token);  // Debugging log

      try {
          const response = await fetch(`/places/${placeId}/reviews`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify(reviewData)
          });

          console.log('Submit review response status:', response.status);  // Debugging log

          if (!response.ok) {
              const errorText = await response.text();
              console.error('Failed to submit review:', errorText);
              return;
          }

          const newReview = await response.json();
          console.log('Review submitted:', newReview);

          // Optionally, you can re-fetch reviews and update the review list
          fetchReviews();

          // Clear the form
          reviewText.value = '';
          reviewRating.value = '';

      } catch (error) {
          console.error('Error submitting review:', error);
      }
  });

  async function fetchReviews() {
      const token = getCookie('jwt_token');

      try {
          const response = await fetch(`/places/${placeId}/reviews`, {
              method: 'GET',
              headers: {
                  'Authorization': `Bearer ${token}`
              }
          });

          console.log('Reviews response status:', response.status);  // Debugging log

          if (!response.ok) {
              console.error('Failed to fetch reviews');
              return;
          }

          const reviews = await response.json();
          console.log('Reviews:', reviews);  // Log the reviews data
          renderReviews(reviews);

      } catch (error) {
          console.error('Error fetching reviews:', error);
      }
  }

  function renderReviews(reviews) {
      const reviewListSection = document.getElementById('review-list');
      reviewListSection.innerHTML = '';
      if (reviews.length === 0) {
          const noReviews = document.createElement('p');
          noReviews.textContent = 'No reviews available for this place.';
          reviewListSection.appendChild(noReviews);
      } else {
          reviews.forEach(review => {
              const reviewCard = document.createElement('div');
              reviewCard.classList.add('review-card');

              const reviewerName = document.createElement('p');
              reviewerName.innerHTML = `<strong>${review.user_id}</strong>`;

              const reviewText = document.createElement('p');
              reviewText.textContent = review.comment;

              const reviewRating = document.createElement('p');
              reviewRating.innerHTML = `<strong>Rating:</strong> ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}`;

              reviewCard.appendChild(reviewerName);
              reviewCard.appendChild(reviewText);
              reviewCard.appendChild(reviewRating);

              reviewListSection.appendChild(reviewCard);
          });
      }
  }

  // Initial fetch to display current reviews
  fetchReviews();
});