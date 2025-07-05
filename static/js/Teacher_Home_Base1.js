// Get modal element
const modal = document.getElementById("logoutModal");
const logoutBtn = document.getElementById("logoutBtn");
const closeBtn = document.querySelector(".close");
const cancelButton = document.querySelector(".cancel-button");

// Open modal
logoutBtn.onclick = function () {
    modal.style.display = "block";
};

// Close modal on 'x' button
closeBtn.onclick = function () {
    modal.style.display = "none";
};

// Close modal on cancel button
cancelButton.onclick = function () {
    modal.style.display = "none";
};

// Close modal if clicked outside of it
window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};