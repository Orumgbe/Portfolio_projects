let block1 = document.getElementById("one");
let block2 = document.getElementById("two");
let block3 = document.getElementById("three");
let block4 = document.getElementById("four");
let block5 = document.getElementById("five");
let block6 = document.getElementById("six");
let block7 = document.getElementById("seven");
let block8 = document.getElementById("eight");
let block9 = document.getElementById("nine");

document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('#content');

    // Element to display the character count
    const countElement = document.createElement('small');
    textarea.parentElement.appendChild(countElement);

    textarea.addEventListener('input', function() {
        const characterCount = textarea.value.length;
        const limit = 150;

        countElement.textContent = `${characterCount} / ${limit}`;

        // Disable the textarea if the character limit is exceeded
        if (characterCount > limit) {
            textarea.value = textarea.value.substring(0, limit);
            textarea.disabled = true;
        } else {
            textarea.disabled = false;
        }
    });
});
