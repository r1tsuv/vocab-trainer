document.addEventListener("DOMContentLoaded", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    console.log("Current theme on load:", currentTheme);

    // Show page after applying the correct theme
    document.documentElement.style.opacity = "1";

    const themeToggle = document.createElement("button");
    themeToggle.innerText = currentTheme === "dark" ? "☀ Light Mode" : "🌙 Dark Mode";
    themeToggle.classList.add("btn");
    themeToggle.style.position = "fixed";
    themeToggle.style.top = "10px";
    themeToggle.style.right = "10px";

    themeToggle.addEventListener("click", () => {
        const newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        themeToggle.innerText = newTheme === "dark" ? "☀ Light Mode" : "🌙 Dark Mode";
    });

    document.body.appendChild(themeToggle);
});

