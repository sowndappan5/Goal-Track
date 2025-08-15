// Import Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, updateProfile } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";


// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyA2Gu3QUPTYXw-nGJfQ6qz4TBKZjfvdmdg",
    authDomain: "learning-tracker-23c7a.firebaseapp.com",
    projectId: "learning-tracker-23c7a",
    storageBucket: "learning-tracker-23c7a.appspot.com", // Fixed storage bucket URL
    messagingSenderId: "947363035210",
    appId: "1:947363035210:web:970e0bde13879dc7db0eb3",
    measurementId: "G-DNWD5M75RV"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

document.getElementById('signUpButton').addEventListener('click', (event) => {
    event.preventDefault(); // Prevent form submission
    register();
});

document.getElementById('signInButton').addEventListener('click', (event) => {
    event.preventDefault(); // Prevent form submission
    login();
});

// Register
function register() {
    const email = document.getElementById('userSignUpEmailId').value;
    const password = document.getElementById('userSignUpPass').value;
    const name = document.getElementById('userName').value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            const user = userCredential.user;

            // Update user profile with name
            return updateProfile(user, {
                displayName: name
            }).then(() => {
                window.location.href = "home";
            });
        })
        .catch((error) => {
            alert("Registration failed: " + error.message);
        });
}

// Login
function login() {
    const email = document.getElementById('userEmailId').value;
    const password = document.getElementById('userPass').value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            window.location.href = "home";
        })
        .catch((error) => {
            alert("Login failed: " + error.message); // Fixed incorrect alert message
        });
}
