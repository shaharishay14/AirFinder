const loginBtn = document.querySelector("#login");
const registerBtn = document.querySelector("#register");
const loginForm = document.querySelector(".login-form");
const registerForm = document.querySelector(".register-form");


document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const autoClick = urlParams.get('autoClick');
    if (autoClick === 'register') {
        registerBtn.click();
    }
});

loginBtn.addEventListener("click", () => {
  loginBtn.style.backgroundColor = "#21264D";
  registerBtn.style.backgroundColor = "rgba(255,255,255,0.2)";

  loginForm.style.left = "50%";
  registerForm.style.left = "-50%";

  loginForm.style.opacity = 1;
  registerForm.style.opacity = 0;
});


registerBtn.addEventListener("click", () => {
    loginBtn.style.backgroundColor = "rgba(255,255,255,0.2)";
    registerBtn.style.backgroundColor = "#21264D";
  
    loginForm.style.left = "150%";
    registerForm.style.left = "50%";
  
    loginForm.style.opacity = 0;
    registerForm.style.opacity = 1;
  });

//View Password
function myLogPassword() {
    var input = document.getElementById('logPassword');
    var icon = document.getElementById('log-pass-icon');
    // Toggle the input type and corresponding icon
    if (input.type === 'password') {
        input.type = 'text';
        icon.name = 'eye-outline'; // Icon when the password is visible
    } else {
        input.type = 'password';
        icon.name = 'eye-off-outline'; // Icon when the password is hidden
    }
}

function myRegPassword() {
    var input = document.getElementById('regPassword');
    var icon = document.getElementById('reg-pass-icon');
    // Toggle the input type and corresponding icon
    if (input.type === 'password') {
        input.type = 'text';
        icon.name = 'eye-outline'; // Icon when the password is visible
    } else {
        input.type = 'password';
        icon.name = 'eye-off-outline'; // Icon when the password is hidden
    }
}



function changeIconLog(value) {
    var icon = document.getElementById('log-pass-icon');
    if (value) {
        icon.name = 'eye-off-outline'; // Change icon when there is input
    } else {
        icon.name = 'lock-closed-outline'; // Default icon
    }
}

function changeIconReg(value) {
    var icon = document.getElementById('reg-pass-icon');
    if (value) {
        icon.name = 'eye-off-outline'; // Change icon when there is input
    } else {
        icon.name = 'lock-closed-outline'; // Default icon
    }
}