window.addEventListener("DOMContentLoaded", async () => {
  const statusDiv = document.getElementById("status");
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  if (!token) {
    statusDiv.textContent = "Missing verification token.";
    return;
  }

  try {
    const response = await fetch(`/login_api/verify-email/${token}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });

    const data = await response.json();

    if (!response.ok) {
      statusDiv.textContent = data.error || "Verification failed.";
      return;
    }

    statusDiv.textContent = data.message || "Account verified successfully.";

    setTimeout(() => {
      window.location.href = "/login";
    }, 1500);

  } catch (err) {
    console.error(err);
    statusDiv.textContent = "An unexpected error occurred.";
  }
});