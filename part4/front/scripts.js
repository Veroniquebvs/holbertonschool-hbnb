/* 
=========== FUNCTIONS ==========
*/

// LOGIN
async function loginUser(email, password) {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
        throw new Error("Login failed");
    }

    return response.json();
}


// COOKIES
function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        let [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
  }

// LIST OF PLACES
async function fetchPlaces(token) {
    const response = await fetch("http://localhost:5000/api/v1/places/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            ...(token && { "Authorization": `Bearer ${token}` })
        }
    });

    if (!response.ok) {
        throw new Error("Failed to fetch places");
    }

    return response.json();

  }

// DISPLAY PLACES
 function displayPlaces(places) {
    const container = document.getElementById("places-list");
    if (!container) return;
    container.innerHTML = "";

    const placeImages = {
        "8018ba82-3b86-42de-96b5-b4d03d57e0bd": "images/paris_pink.jpg",
        "52ad2451-2229-49af-a414-7633fc2e9622": "images/maison_bord_mer.jpg",
        "808b5f78-6b7b-4252-9ff5-7100e36ad0d3": "images/studio.jpg"
    };

    places.forEach(place => {
        const card = document.createElement("article");
        card.classList.add("place-card");

        card.innerHTML = `
            <img src="${placeImages[place.id] || 'images/default.jpg'}" alt="${place.title}" class="place-img">
            <h3>${place.title}</h3>
            <p>Price: $${place.price}</p>
            <p>${place.description}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        container.appendChild(card);
    });

  }

// FILTERED PLACES
function setupFilter(places) {
    const filter = document.getElementById("price-filter");
    if (!filter) return;
    filter.addEventListener("change", () => {
        const value = filter.value;

        let filteredPlaces;

        if (value === "all") {
            filteredPlaces = places;
        } else {
            filteredPlaces = places.filter(place => place.price <= parseInt(value));
        }

        displayPlaces(filteredPlaces);
    });
}

// GET PLACE ID
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// FETCH PLACE DETAILS
async function fetchPlaceDetails(token, placeId) {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            ...(token && { "Authorization": `Bearer ${token}` })
        }
    });

    if (!response.ok) {
        throw new Error("Failed to fetch place details");
    }

    const data = await response.json();
    displayPlaceDetails(data);
}

// DISPLAY PLACE DETAILS
function displayPlaceDetails(place) {
    const container = document.getElementById("place-details");
    if (!container) return;
    container.innerHTML = "";

    const placeImages = {
        "8018ba82-3b86-42de-96b5-b4d03d57e0bd": "images/paris_pink.jpg",
        "52ad2451-2229-49af-a414-7633fc2e9622": "images/maison_bord_mer.jpg",
        "808b5f78-6b7b-4252-9ff5-7100e36ad0d3": "images/studio.jpg"
    };

    const img = document.createElement("img");
    img.src = placeImages[place.id] || "images/default.jpg";
    img.alt = place.title;
    img.classList.add("place-img");
    container.appendChild(img);

    const title = document.createElement("h2");
    title.textContent = place.title;

    const description = document.createElement("p");
    description.textContent = place.description;

    const price = document.createElement("p");
    price.textContent = `Price: $${place.price}`;

    const amenities = document.createElement("div");
    amenities.innerHTML = `
        <h3>Amenities</h3>
        <ul class="amenities-list">
            ${place.amenities.map(a => `<li>🌸 ${a.name}</li>`).join("")}
        </ul>
`;

    const location = document.createElement("p");
    location.textContent = `Latitude: ${place.latitude} | Longitude: ${place.longitude}`;

    container.appendChild(title);
    container.appendChild(description);
    container.appendChild(price);
    container.appendChild(amenities);
    container.appendChild(location);

    
    // REVIEWS
    if (place.reviews && place.reviews.length > 0) {
        const reviewTitle = document.createElement("h3");
        reviewTitle.textContent = "Reviews";
        container.appendChild(reviewTitle);

        place.reviews.forEach(review => {
            const reviewEl = document.createElement("article");
            reviewEl.classList.add("review-card");
            reviewEl.innerHTML = `
                <p><strong>${review.user_name}</strong></p>
                <p>Rating: ${"♥".repeat(review.rating)}${"♡".repeat(5 - review.rating)}</p>
                <p>${review.text}</p>
            `;
        container.appendChild(reviewEl);
    });
    }
}

// CHECK AUTHENTICATION
function checkAuthentication() {
    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
        return null;
    }

    return token;
}
// SUBMIT REVIEW
async function submitReview(token, placeId, reviewText, reviewRating) {
        const response = await fetch(`http://localhost:5000/api/v1/reviews/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: reviewRating
            })
        });

        if (!response.ok) {
            throw new Error("Failed to submit review");
        }

        return response.json();
    }

// GET CURRENT USER INFO
async function fetchCurrentUser(token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.sub;

    const response = await fetch(`http://localhost:5000/api/v1/users/${userId}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) throw new Error("Failed to fetch user");
    return response.json();
}

/*
=========== MAIN CODE ==========
*/

document.addEventListener('DOMContentLoaded', async() => {
    const loginForm = document.getElementById('login-form');
    const token = getCookie("token");
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById("add-review");
    // LOGIN
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const data = await loginUser(email, password);

                document.cookie = "token=" + data.access_token + "; path=/; SameSite=Lax";
                window.location.href = "index.html";

            } catch (error) {
                alert("Invalid email or password");
            }
          });
      }
    // Manage login
    const loginLink = document.querySelector(".login-button");
    if (loginLink && token) {
        loginLink.style.display = "none";
    }
    // load the places
    try {
        if (document.getElementById("places-list")) {
        const places = await fetchPlaces(token);

        displayPlaces(places);
        setupFilter(places);
        }

    } catch (error) {
        console.error(error);
    }

    // Form management
    if (addReviewSection) {
        if (!token) {addReviewSection.style.display = "none";
        } else {
            addReviewSection.style.display = "block";
        }
    }

    // Load data
    if (placeId) {
        fetchPlaceDetails(token, placeId)
            .catch(error => console.error(error));
    }

    // Review form

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const secureToken = checkAuthentication();
    
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('comment').value;
            const reviewRating = parseInt(document.getElementById('rating').value);

            try {
                await submitReview(secureToken, placeId, reviewText, reviewRating);
                alert("Review submitted successfully!");
                reviewForm.reset();
            } catch (error) {
                alert("Failed to submit review");
            }
        });
    }

    // HEART RATING
    const hearts = document.querySelectorAll(".heart");
    const ratingInput = document.getElementById("rating");

    hearts.forEach(heart => {
        heart.addEventListener("click", () => {
            const value = heart.dataset.value;
            ratingInput.value = value;

            hearts.forEach(h => {
                if (h.dataset.value <= value) {
                    h.textContent = "♥";
                    h.classList.add("active");
                } else {
                    h.textContent = "♡";
                    h.classList.remove("active");
                }
            });
        });
    });

    // add button review by placeId
    const addReviewBtn = document.getElementById("add-review-btn");
    if (addReviewBtn && placeId) {
        
        addReviewBtn.href = `add_review.html?id=${placeId}`;
    }

    // Display place info on add_review page
    if (addReviewSection && placeId) {
        const placeImages = {
            "8018ba82-3b86-42de-96b5-b4d03d57e0bd": "images/paris_pink.jpg",
            "52ad2451-2229-49af-a414-7633fc2e9622": "images/maison_bord_mer.jpg",
            "808b5f78-6b7b-4252-9ff5-7100e36ad0d3": "images/studio.jpg"
        };

        await fetchPlaceDetails(token, placeId);
        const placeTitle = document.querySelector("#place-details h2");
        if (placeTitle) {
            const infoEl = document.createElement("div");
            infoEl.classList.add("place-card");
            infoEl.innerHTML = `
                <img src="${placeImages[placeId] || 'images/default.jpg'}" alt="${placeTitle.textContent}" class="place-img">
                <h2>${placeTitle.textContent}</h2>
            `;
            addReviewSection.insertBefore(infoEl, addReviewSection.firstChild);
        }
        // welcome message
        if (token) {
        const user = await fetchCurrentUser(token);
        const welcomeEl = document.createElement("p");
        welcomeEl.classList.add("welcome-message");
        welcomeEl.textContent = `Hello ${user.first_name} ! 🌸 We'd love to hear your thoughts — share your experience below!`;
        addReviewSection.insertBefore(welcomeEl, addReviewSection.firstChild);
        }
    }

    // LOGOUT
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        if (token) {
            logoutBtn.style.display = "inline-block";
        }
        logoutBtn.addEventListener("click", () => {
            document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
            window.location.href = "login.html";
        });
    } 

    // DARK MODE
    const darkModeBtn = document.getElementById("dark-mode-btn");
    if (darkModeBtn) {
        if (localStorage.getItem("darkMode") === "true") {
            document.body.classList.add("dark-mode");
            darkModeBtn.innerHTML = "☀";
        } else {
            darkModeBtn.innerHTML = "☾";
        }

        darkModeBtn.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");
            const isDark = document.body.classList.contains("dark-mode");
            darkModeBtn.innerHTML = isDark ? "☀" : "☾";
            localStorage.setItem("darkMode", isDark);
        });
    }
});
