//......................................
document.addEventListener('DOMContentLoaded', function() {
    // Track menu visibility
    let isDisplayed = false;
    const button = document.getElementById('dropdown-button');
    const dropdownMenu = document.getElementById('dropdown-menu');

    // Add click event listener to the button
    button.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents the document click listener from immediately hiding the menu
        toggleDropdown();
    });

    // Toggle dropdown menu visibility
    function toggleDropdown() {
        isDisplayed = !isDisplayed;
        dropdownMenu.classList.toggle('hidden', !isDisplayed);
    }

    // Close dropdown if clicking outside the menu
    document.addEventListener('click', function(event) {
        if (!button.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.add('hidden');
            isDisplayed = false;
        }
    });
});

