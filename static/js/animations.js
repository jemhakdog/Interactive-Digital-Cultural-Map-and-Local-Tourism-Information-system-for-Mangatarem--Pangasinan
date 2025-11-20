document.addEventListener('DOMContentLoaded', function() {
    const text = "Discover Mangatarem";
    const typingTextElement = document.getElementById('typing-text');
    const cursorElement = document.querySelector('.cursor');
    let index = 0;

    function type() {
        if (index < text.length) {
            typingTextElement.textContent += text.charAt(index);
            index++;
            setTimeout(type, 100); // Adjust typing speed here
        } else {
            // Optional: Stop blinking after typing is done, or keep it
            // cursorElement.style.display = 'none'; 
        }
    }

    // Start typing after a short delay
    setTimeout(type, 500);
});
