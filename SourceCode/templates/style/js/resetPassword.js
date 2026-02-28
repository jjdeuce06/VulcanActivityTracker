function backToLogin() {window.location.href = "/login";}


function resetPassword() {
    const email = document.getElementById("user_entry").value.trim();
    fetch("/password_api/reset-password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  })
  .then(async (response) => {
    const text = await response.text(); // read body no matter what

    if (!response.ok) {
      console.error("Server error:", response.status, text);
      throw new Error(`HTTP ${response.status}: ${text.slice(0, 300)}`);
    }

    // Try parse JSON only if it looks like JSON
    try {
      return JSON.parse(text);
    } catch {
      throw new Error("Expected JSON but got: " + text.slice(0, 300));
    }
  })
  .then((data) => {
    if (data.success) {
      alert("Password reset request sent. Please check your email.");
      window.location.href = "/login";
    } else {
      alert(data.error || "Error resetting password. Please try again.");
    }
  })
  .catch((err) => {
    console.error(err);
    alert("Server error. Check console for details.");
  });
}