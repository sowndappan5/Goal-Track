document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register'); // Ensure this button exists
    const loginBtn = document.getElementById('login');
    
    // Toggle to sign-up form
    if (registerBtn) { // Check if registerBtn exists
        registerBtn.addEventListener('click', () => {
            container.classList.add("active");
        });
    }

    // Toggle to sign-in form
    loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
    });

    // Redirect to personal_info.html on Sign In button click
    const signInForm = document.querySelector('.sign-in form');
    if (signInForm) { // Check if signInForm exists
        signInForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent default form submission
            window.location.href = 'personal_info.html'; // Redirect to personal_info.html
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const personalInfoForm = document.getElementById('personalInfoForm');
    const academicInfoForm = document.getElementById('academicInfoForm');

    // Redirect to demo.html on form submission
    if (personalInfoForm) {
        personalInfoForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent default form submission
            
            // Validate Personal Info fields
            const namePersonal = document.getElementById('name-personal').value;
            const agePersonal = document.getElementById('age-personal').value;
            const locationPersonal = document.getElementById('location-personal').value;

            // Validate Academic Info fields
            const collegeNameAcademic = document.getElementById('collegeName-academic').value;
            const course = document.getElementById('course').value;
            const yearOfStudy = document.getElementById('yearOfStudy').value;
            const graduationYear = document.getElementById('graduation-academic').value;

            // Check if all fields are filled
            if (namePersonal && agePersonal && locationPersonal && collegeNameAcademic && course && yearOfStudy && graduationYear) {
                window.location.href = 'demo.html'; // Redirect to demo.html if all fields are valid
            } else {
                alert("Please fill in all fields."); // Alert if any field is missing
            }
        });
    }
});

