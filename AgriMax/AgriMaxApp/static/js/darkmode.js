// Handle dark mode switching
document.addEventListener("DOMContentLoaded", () => {
    const themeToggleButtons = document.querySelectorAll("#theme-toggle"); // Select all elements with ID 'theme-toggle'
    const sunIcon = document.getElementById("sun-icon");
    const moonIcon = document.getElementById("moon-icon");
    const rootElement = document.documentElement;

    // Initialize theme based on user's previous preference or system preference
    const userTheme = localStorage.getItem("theme");
    const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    const currentTheme = userTheme || systemTheme;

    // Set the initial theme
    setTheme(currentTheme);

    // Add click event listener to each theme toggle button
    themeToggleButtons.forEach(button => {
        button.addEventListener("click", () => {
            const newTheme = rootElement.classList.contains("dark") ? "light" : "dark";
            setTheme(newTheme);
        });
    });

    // Function to set the theme
    function setTheme(theme) {
        if (theme === "dark") {
            rootElement.classList.add("dark");
            sunIcon.classList.add("hidden");
            moonIcon.classList.remove("hidden");
        } else {
            rootElement.classList.remove("dark");
            sunIcon.classList.remove("hidden");
            moonIcon.classList.add("hidden");
        }
        localStorage.setItem("theme", theme);
    }
});
