document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    // Toggle to sign-up form
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            container.classList.add("active");
        });
    }

    // Toggle to sign-in form
    loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
    });

    // Handle Sign In form submission
    const signInForm = document.querySelector('.sign-in form');
    if (signInForm) {
        signInForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            try {
                const formData = new FormData(signInForm);
                const response = await fetch(signInForm.action, {
                    method: 'POST',
                    body: formData,
                    // This is important to follow redirects
                    redirect: 'follow'
                });

                if (response.redirected) {
                    // Follow the server's redirect
                    window.location.href = response.url;
                } else if (!response.ok) {
                    // Handle error responses
                    const text = await response.text();
                    throw new Error(text);
                }
            } catch (error) {
                alert(error.message || 'An error occurred during sign in');
            }
        });
    }


});

document.addEventListener('DOMContentLoaded', () => {
    const personalInfoForm = document.getElementById('personalInfoForm');

    if (personalInfoForm) {
        personalInfoForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            try {
                const formData = new FormData(personalInfoForm);
                const response = await fetch('/personal_info', {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.text();
                if (response.ok) {
                    alert('Information saved successfully!');
                    window.location.href = '/home';
                } else {
                    throw new Error(result || 'Failed to save information');
                }
            } catch (error) {
                alert(error.message);
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent default form submission

            const formData = new FormData(signupForm);
            const response = await fetch(signupForm.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                // Optionally handle successful signup here
                alert("Account created successfully! Redirecting to Sign In...");
                window.location.href = '/'; // Redirect to sign-in page
            } else {
                const errorMessage = await response.text();
                alert(errorMessage); // Show error message
            }
        });
    }
});
