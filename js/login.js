const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const usernameError = document.getElementById('usernameError');
const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');

const validateUsername = () => {
    const value = usernameInput.value.trim();
    if (!value) {
        usernameError.textContent = 'Username is required.';
        return false;
    }
    if (value.length < 3) {
        usernameError.textContent = 'Username must be at least 3 characters.';
        return false;
    }
    usernameError.textContent = '';
    return true;
};

const validateEmail = () => {
    const value = emailInput.value.trim();
    const gmailPattern = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    if (!value) {
        emailError.textContent = 'Gmail address is required.';
        return false;
    }
    if (!gmailPattern.test(value)) {
        emailError.textContent = 'Please enter a valid Gmail address.';
        return false;
    }
    emailError.textContent = '';
    return true;
};

const validatePassword = () => {
    const value = passwordInput.value;
    if (!value) {
        passwordError.textContent = 'Password is required.';
        return false;
    }
    if (value.length < 6) {
        passwordError.textContent = 'Password must be at least 6 characters.';
        return false;
    }
    passwordError.textContent = '';
    return true;
};

loginForm.addEventListener('submit', (event) => {
    const usernameValid = validateUsername();
    const emailValid = validateEmail();
    const passwordValid = validatePassword();

    if (!usernameValid || !emailValid || !passwordValid) {
        event.preventDefault();
    }
});

usernameInput.addEventListener('input', validateUsername);
emailInput.addEventListener('input', validateEmail);
passwordInput.addEventListener('input', validatePassword);
