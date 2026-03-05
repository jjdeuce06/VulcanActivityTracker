<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", async () => {
=======
document.addEventListener("DOMContentLoaded", () => {

>>>>>>> 1782402 (Settings page begun)
    const changeBtn = document.getElementById("changeUsernameBtn");
    const deleteBtn = document.getElementById("deleteAccountBtn");

    const usernameMessage = document.getElementById("usernameMessage");
    const deleteMessage = document.getElementById("deleteMessage");

<<<<<<< HEAD
    if (changeBtn) {
        changeBtn.addEventListener("click", async () => {
            const newUsernameInput = document.getElementById("newUsername");
            const newUsername = newUsernameInput.value.trim();

            usernameMessage.textContent = "";

            if (!newUsername) {
                usernameMessage.textContent = "Please enter a new username.";
                return;
            }

            try {
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

                if (result.success) {
                    localStorage.setItem("currentUser", newUsername);
                    usernameMessage.textContent = result.message;

                    const profileValues = document.querySelectorAll(".username-display");
                    profileValues.forEach(el => {
                        el.textContent = newUsername;
                    });
                } else {
                    usernameMessage.textContent = result.message || "Failed to update username.";
                }
            } catch (error) {
                console.error("Username update failed:", error);
                usernameMessage.textContent = "Something went wrong while updating your username.";
            }
        });
    }

    if (deleteBtn) {
        deleteBtn.addEventListener("click", async () => {
            const confirmDelete = confirm("Are you sure you want to delete your account?");
            if (!confirmDelete) return;

            deleteMessage.textContent = "";

            try {
                const response = await fetch("/settings_api/delete-account", {
                    method: "DELETE"
                });

                const result = await response.json();
                deleteMessage.textContent = result.message;

                if (result.success) {
                    window.location.href = "/";
                }
            } catch (error) {
                console.error("Delete account failed:", error);
                deleteMessage.textContent = "Something went wrong while deleting your account.";
            }
        });
    }

    await fillQuickStats();
});

async function fillQuickStats(){

  try {
    const response = await fetch("/settings_api/fillActivityStat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    populateQuick(data);
    fillDisplayInfo(data);

    return data;

  } catch (err) {
    console.error("Failed to load activities:", err);
  }

}
function populateQuick(data) {
  // Fill the activity count using the array length
  const activityCountDiv = document.querySelector("#settingAStat");
  activityCountDiv.textContent = data.activities ?? 0;

   const ClubsCount = document.querySelector("#settingCStat");
   ClubsCount.textContent = data.clubs ?? 0;

   const goalCount = document.querySelector("#settingGStat");
   goalCount.textContent = data.challenges ?? 0;

}

function fillDisplayInfo(data){

    const displayName = document.querySelector("#settings-displayname");
    displayName.textContent = data.name;
    const displayEmail = document.querySelector("#settings-email");
    displayEmail.textContent = data.email;

    const profileName = document.querySelector("#profile-name");
    profileName.textContent = data.name;
}
=======
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

        usernameMessage.textContent = result.message;

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
>>>>>>> 1782402 (Settings page begun)
