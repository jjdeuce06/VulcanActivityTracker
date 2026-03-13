function backToLogin() {
  window.location.href = "/login";
}

// SAME hashing pattern as register/login
async function hashPassword(password) {
  const encoder = new TextEncoder().encode(password);
  const hashBuff = await crypto.subtle.digest("SHA-256", encoder);

  return Array.from(new Uint8Array(hashBuff))
    .map(b => b.toString(16).padStart(2, "0"))
    .join("");
}

async function submitNewPassword() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");
  const password = document.getElementById("new_password").value;
  const errorDiv = document.getElementById("reset-error");

  if (errorDiv) {
    errorDiv.textContent = "";
    errorDiv.style.color = "red";
  }

  if (!token) {
    if (errorDiv) errorDiv.textContent = "Missing reset token.";
    else alert("Missing reset token.");
    return;
  }

  if (!password) {
    if (errorDiv) errorDiv.textContent = "Please enter a new password.";
    else alert("Please enter a new password.");
    return;
  }

  try {
    // SAME PATTERN AS REGISTER
    const hashedPassword = await hashPassword(password);

    const response = await fetch(`/password_api/reset-password/${token}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        password: hashedPassword
      })
    });

    const data = await response.json();

    if (!response.ok) {
      if (errorDiv) {
        errorDiv.textContent = data.error || "Failed to reset password.";
      } else {
        alert(data.error || "Failed to reset password.");
      }
      return;
    }

    if (errorDiv) {
      errorDiv.style.color = "green";
      errorDiv.textContent = data.message || "Password reset successful.";
    } else {
      alert(data.message || "Password reset successful.");
    }

    setTimeout(() => {
      backToLogin();
    }, 1200);

  } catch (err) {
    console.error("Reset password error:", err);
    if (errorDiv) {
      errorDiv.textContent = "An unexpected error occurred. Try again.";
    } else {
      alert("An unexpected error occurred. Try again.");
    }
  }
}