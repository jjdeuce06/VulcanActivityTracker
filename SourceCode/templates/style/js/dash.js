document.addEventListener("DOMContentLoaded", () => {
    const username = localStorage.getItem("currentUser");
    console.log("user from dash:", username);
    if (username) {
        document.getElementById("user-name").textContent = username;
    }
});