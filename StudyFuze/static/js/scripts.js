const card = document.getElementById("card");

function swipeLeft() {
    card.classList.add("swipe-left");
    setTimeout(() => resetCard(), 300); // Reset card after animation
}

function swipeRight() {
    card.classList.add("swipe-right");
    setTimeout(() => resetCard(), 300); // Reset card after animation
}

function resetCard() {
    card.classList.remove("swipe-left", "swipe-right");
    // Load new profile data here if needed
}
