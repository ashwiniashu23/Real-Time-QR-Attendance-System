window.addEventListener("load", updateStatus)

// Check For Adblocker
async function updateStatus()
{
    let isEnabled = await AdBlockChecker.checkAdBlock();

    isEnabled ? alert("Please Disable Your Adblocker") : "none";

}




function checkCheckbox()
{
    const checkbox = document.getElementById('blind-input');
    checkbox.checked = true; // This will check the checkbox
    console.log("Clicked")
}

function togglePasswordVisibility()
{
  const passwordInput = document.getElementById('password-input');
  const checkbox = document.getElementById('blind-input');

  // Toggle the input type between password and text
  if (checkbox.checked)
  {
        passwordInput.type = 'text';  // Show password
  }
  else
  {
        passwordInput.type = 'password';  // Hide password
  }
}

document.addEventListener("DOMContentLoaded", function(){
    document.querySelector("input[name='height']").value = window.screen.height;
    document.querySelector("input[name='width']").value = window.screen.width;
});

document.addEventListener("DOMContentLoaded", function () {
const fpPromise = FingerprintJS.load();
let a = "";
fpPromise
    .then(fp => fp.get()) // Get the unique identifier
    .then(result => {
    const deviceFingerprint = result.visitorId; // This is the unique fingerprint
    document.getElementById("info").value = deviceFingerprint;
    // You can store it in localStorage or send it to your backend
    // localStorage.setItem("device_fingerprint", deviceFingerprint);
});
});




