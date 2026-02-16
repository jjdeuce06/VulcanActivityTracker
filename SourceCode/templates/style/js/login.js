//this file will handle login click events, forma verification, and redirection
//will serve as api for login user account set up
//possibly hold password hashing functions but prob not


document.getElementById("createBtn").addEventListener("click", async () =>{
    const username = document.getElementById("user_entry").value;
    const password = document.getElementById("pass_entry").value;
    const errorDiv = document.getElementById("register-error");

    // Clear previous messages
    errorDiv.textContent = "";
    errorDiv.style.color = "red";

    if (!username || !password) 
        {
        errorDiv.textContent = "Please enter both username and password.";
        return;
    }

    if (password.length < 8)
    {
        errorDiv.textContent = "Password must be at least 8 characters long.";
        return;
    }

    //hash password before sending
    const hash = await hashPassword(password);
        //send to backend
        try {
        const response = await sendLoginData(username, hash);
        if (!response.ok) {
            // show backend error message like "Username already exists"
            errorDiv.textContent = response.error || "Registration failed";
            document.getElementById("user_entry").focus();
        } else {
            errorDiv.style.color = "green";
            errorDiv.textContent = "Registration successful!";
            backToLogin();
        }

    } catch (err) {
        console.error("Error sending login data:", err);
        errorDiv.textContent = "An unexpected error occurred. Try again.";
    }

});



/**Hash Process:
 * Two layers:

   1 Client-side hash → protects raw password

   2 Server-side slow hash → protects database

hash on frontend quick
send to backend
hash again with argon secure

then verify on backend upon login
store in db
*/


//STEP 1
async function hashPassword(password){
    const encoder = new TextEncoder().encode(password);
    const hashBuff = await crypto.subtle.digest("SHA-256", encoder);

    return Array.from(new Uint8Array(hashBuff)).map(b=>b.toString(16).padStart(2, "0")).join("");
}

//Step 2: API to send hash

async function sendLoginData(username, hashPassword){
    const response = await fetch("/login_api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: hashPassword
        })
    });

    let data = {};
    try {
        data = await response.json(); // parse server response even if error
    } catch (err) {
        console.warn("Server did not return JSON:", err);
    }

    // Return both HTTP status and JSON body
    return { ok: response.ok, status: response.status, ...data };
}

function backToLogin() {window.location.href = "/login";}