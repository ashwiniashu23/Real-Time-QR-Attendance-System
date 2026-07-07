window.addEventListener("load", updateStatus)

// Check For Adblocker
async function updateStatus() {
    let isEnabled = await AdBlockChecker.checkAdBlock();

    isEnabled ? alert("Please Disable Your Adblocker") : "none";

}


//Updating Window screen and size
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("input[name='height']").value = window.screen.height;
    document.querySelector("input[name='width']").value = window.screen.width;
});

var message;
//Validating email format and seding otp
async function runPythonFunction() {
    var email = document.getElementById('email').value;
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email == "" || !emailPattern.test(email)) {
        alert("Enter Proper Email");
        return;
    }

    button = document.getElementById('otp');
    button.disabled = true;

    setTimeout(function () {
        button.disabled = false;
    }, 60000);
    startCountdown()

    var csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value; // If js written outside then it won't take csrf automatically

    const response = await fetch("/otp", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrf_token // Include CSRF token if needed
        },
        body: `custom_data=${email}`
    });
    
    document.getElementById("insert-otp").innerHTML = `<input required="" placeholder="" onkeydown="goToNext(event,this)" id="user-otp" name="otp" type="otp" class="input">
        <span>OTP</span>`;
    
    alert("The last process of otp");
    return 0;
}


// Count Down function for email
function startCountdown() {
    let timerDisplay = document.getElementById("otp");
    let timeleft = 59;

    let timeInterval = setInterval(function () {
        let minutes = Math.floor(timeleft / 60);
        let seconds = timeleft % 60;
        timerDisplay.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}  `
        timeleft--;

        if (timeleft < 0) {
            clearInterval(timeInterval);
            timerDisplay.textContent = "Get Otp"
        }
    }, 1000);
}


// Collecting Fingerprint of device and browser
document.addEventListener("DOMContentLoaded", function () {

    const fpPromise = FingerprintJS.load();
    let a = "";

    fpPromise
        .then(fp => fp.get()) // Get the unique identifier
        .then(result => {
            const deviceFingerprint = result.visitorId; // This is the unique fingerprint
            document.querySelector("input[name='unique']").value = deviceFingerprint;

            // You can store it in localStorage or send it to your backend
            // localStorage.setItem("device_fingerprint", deviceFingerprint);
        });
});

function goToNext(event, currentInput) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent form submission
        const inputs = document.querySelectorAll('input');
        const index = Array.from(inputs).indexOf(currentInput);
        if (index < inputs.length - 1) {
            inputs[index + 1].focus();
        }
    }
}

async function emailfun(event, currentInput) {
    if (event.key === "Enter") {
        await runPythonFunction();
        setTimeout(function () {
            console.log("Waited 3 seconds");
        }, 3000);

        goToNext(event, currentInput);
        email =  document.getElementById("email");
        email.setAttribute("onkeydown","goToNext(event,this)");

    }
}