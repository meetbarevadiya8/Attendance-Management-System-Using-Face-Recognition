// script.js

const textElement = document.querySelector('.typing');
const text = "Welcome";
let index = 0;

function type() {
    if (index < text.length) {
        textElement.innerHTML += text.charAt(index);
        index++;
        setTimeout(type, 200); // Typing speed (200 ms)
    }
}

// Function to move the text up
function moveUp() {
    const container = document.querySelector('.container');
    container.style.transform = 'translateY(-20px)'; // Move up by 20px
    container.style.transition = 'transform 0.5s'; // Smooth transition
}

// Start typing
type();

// Add event listener to the button
document.getElementById('moveUpBtn').addEventListener('click', moveUp);
