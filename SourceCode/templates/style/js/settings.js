document.addEventListener("DOMContentLoaded", () => {

    const changeBtn = document.getElementById("changeUsernameBtn");
    const deleteBtn = document.getElementById("deleteAccountBtn");

    const usernameMessage = document.getElementById("usernameMessage");
    const deleteMessage = document.getElementById("deleteMessage");

    changeBtn.addEventListener("click", async () => {

        const newUsername = document.getElementById("newUsername").value;

        const response = await fetch("/settings_api/change-username", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: newUsername
            })
        });

        const result = await response.json();

        if(result.success){
            localStorage.setItem("currentUser", newUsername);
            usernameMessage.textContent = result.message;
        }
    });


    deleteBtn.addEventListener("click", async () => {

        const confirmDelete = confirm("Are you sure you want to delete your account?");

        if (!confirmDelete) return;

        const response = await fetch("/settings_api/delete-account", {
            method: "DELETE"
        });

        const result = await response.json();

        deleteMessage.textContent = result.message;

        if(result.success){
            window.location.href = "/";
        }

    });

});