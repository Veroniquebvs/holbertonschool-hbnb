/* 
=========== FUNCTIONS ==========
*/

// Fonction pour jouer le son du fouet
function playWhip() {
    const whipSound = new Audio("sounds/fouet.mp3");
    whipSound.currentTime = 0; // Réinitialise pour pouvoir cliquer plusieurs fois vite
    whipSound.play().catch(err => console.log("Audio bloqué ou introuvable:", err));
}

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

    places.forEach(place => {
        const card = document.createElement("article");
        card.classList.add("place-card");

        card.innerHTML = `
            <img src="${place.image_url || 'images/default.jpg'}" alt="${place.title}" class="place-img">
            <h3>${place.title}</h3>
            <p>Price: $${place.price}</p>
            <p>${place.description}</p>
            <a href="place.html?id=${place.id}" class="details-button click-sound">View Details</a>
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

    const img = document.createElement("img");
    img.src = place.image_url || "images/default.jpg";
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
            ${place.amenities.map(a => `<li>⛓️ ${a.name}</li>`).join("")}
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

// FETCH AMENITIES
async function fetchAmenities(token) {
    const response = await fetch("http://localhost:5000/api/v1/amenities/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            ...(token && { "Authorization": `Bearer ${token}` })
        }
    });

    if (!response.ok) throw new Error("Failed to fetch amenities");
    return response.json();
}

// SUBMIT PLACE
async function submitPlace(token, placeData) {
    const response = await fetch("http://localhost:5000/api/v1/places/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(placeData)
    });

    if (!response.ok) throw new Error("Failed to create place");
    return response.json();
}

// CREATE USER
async function createUser(userData) {
    const response = await fetch("http://localhost:5000/api/v1/users/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    });

    if (!response.ok) throw new Error("Failed to create user");
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

    // Redirect to login if not authenticated on index.html
    if (!token && document.getElementById("places-list")) {
        window.location.href = 'login.html';
        return;
    }
    // LOGIN
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            playWhip();
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
            playWhip();

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

        try {
            const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`);
            const place = await response.json();

            // Création du bloc place
            const infoEl = document.createElement("div");
            infoEl.classList.add("place-card");

            infoEl.innerHTML = `
                <img src="${place.image_url || 'images/default.jpg'}" 
                    alt="${place.title}" 
                    class="place-img">

                <h2>${place.title}</h2>
                <p>${place.description}</p>
            `;
        // Ajoute au dessus du formulaire
            addReviewSection.insertBefore(infoEl, addReviewSection.firstChild);

        // Message utilisateur
            if (token) {
                const user = await fetchCurrentUser(token);
                const welcomeEl = document.createElement("p");
                welcomeEl.classList.add("welcome-message");
                welcomeEl.textContent = `Hello ${user.first_name} 🌹 Share your experience with this place!`;
                    addReviewSection.insertBefore(welcomeEl, infoEl);
            }

        } catch (error) {
            console.error("Failed to load place info", error);
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

    // ADD PLACE FORM
    const addPlaceForm = document.getElementById("add-place-form");
    if (addPlaceForm) {
        const secureToken = checkAuthentication();

        // Load amenities as checkboxes
        try {
            const amenities = await fetchAmenities(secureToken);
            const amenitiesContainer = document.getElementById("amenities-list");
            amenities.forEach(amenity => {
                const label = document.createElement("label");
                label.style.display = "flex";
                label.style.alignItems = "center";
                label.style.gap = "0.5rem";
                label.style.margin = "0.3rem 0";
                label.innerHTML = `
                    <input type="checkbox" value="${amenity.id}"> 🌸 ${amenity.name}
                `;
                amenitiesContainer.appendChild(label);
            });
        } catch (error) {
            console.error("Failed to load amenities", error);
        }

        // Submit form
        addPlaceForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            playWhip();

            const selectedAmenities = Array.from(
                document.querySelectorAll("#amenities-list input[type='checkbox']:checked")
            ).map(cb => cb.value);

            const placeData = {
                title: document.getElementById("title").value,
                description: document.getElementById("description").value,
                price: parseFloat(document.getElementById("price").value),
                latitude: parseFloat(document.getElementById("latitude").value),
                longitude: parseFloat(document.getElementById("longitude").value),
                amenities: selectedAmenities,
                image_url: document.getElementById("image_url").value
            };

            try {
                await submitPlace(secureToken, placeData);
                alert("Place added successfully!");
                window.location.href = "index.html";
            } catch (error) {
                alert("Failed to add place");
            }
        });
    }

    // ADD USER FORM
    const addUserForm = document.getElementById("add-user-form");
    if (addUserForm) {
        addUserForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const userData = {
                first_name: document.getElementById("first_name").value,
                last_name: document.getElementById("last_name").value,
                email: document.getElementById("email").value,
                password: document.getElementById("password").value
            };

            try {
                await createUser(userData);
                alert("Account created successfully!");
                window.location.href = "login.html";
            } catch (error) {
                alert("Failed to create account. Email may already be registered.");
            }
        });
    }
});
