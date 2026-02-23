//this file will handle login click events, forma verification, and redirection
//will serve as api for login user account set up
//possibly hold password hashing functions but prob not
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");
    var myInput = document.getElementById("pass_entry");
    var emailInput = document.getElementById("email_entry");
    const errorDiv = document.getElementById("register-error");

    emailInput.onfocus = function()
    {
        // Clear previous messages
        errorDiv.textContent = "";
        errorDiv.style.color = "red";
    }

    myInput.onfocus = function() 
    {
        document.getElementById("message").style.display = "block";
        // Clear previous messages
        errorDiv.textContent = "";
        errorDiv.style.color = "red";
    }

    myInput.onkeyup = function() 
    {
        // Validate lowercase letters
        var lowerCaseLetters = /[a-z]/g;
        if(myInput.value.match(lowerCaseLetters)) 
        {  
            letter.classList.remove("invalid");
            letter.classList.add("valid");
        } 
        else 
        {
            letter.classList.remove("valid");
            letter.classList.add("invalid");
        }
            
        // Validate capital letters
        var upperCaseLetters = /[A-Z]/g;
        if(myInput.value.match(upperCaseLetters)) 
        {  
            capital.classList.remove("invalid");
            capital.classList.add("valid");
        } 
        else 
        {
            capital.classList.remove("valid");
            capital.classList.add("invalid");
        }

        // Validate numbers
        var numbers = /[0-9]/g;
        if(myInput.value.match(numbers)) 
        {  
            number.classList.remove("invalid");
            number.classList.add("valid");
        } 
        else 
        {
            number.classList.remove("valid");
            number.classList.add("invalid");
        }

        // Validate length
        if(myInput.value.length >= 8) 
        {  
            length.classList.remove("invalid");
            length.classList.add("valid");
        } 
        else 
        {
            length.classList.remove("valid");
            length.classList.add("invalid");
        }
    };

function validateEmail(email) 
{
    if (!email.includes("@pennwest.edu"))
    {
        return false;
    }
    return true;
}

document.getElementById("createBtn").addEventListener("click", async () =>{
    const username = document.getElementById("user_entry").value;
    const password = document.getElementById("pass_entry").value;
    const email = document.getElementById("email_entry").value;
    const errorDiv = document.getElementById("register-error");
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");

    // Clear previous messages
    errorDiv.textContent = "";
    errorDiv.style.color = "red";

    if (!username || !password || !email) 
    {
        errorDiv.textContent = "Please enter username, email and password.";
        return;
    }

    if (letter.classList.contains("invalid") || 
        capital.classList.contains("invalid") || 
        number.classList.contains("invalid") || 
        length.classList.contains("invalid")) 
    {
        errorDiv.textContent = "Password does not meet all requirements.";
        return;
    }

    if (!validateEmail(email))
    {
        errorDiv.textContent = "Please enter a valid PennWest email.";
        return;
    }

    

    //hash password before sending
    const hash = await hashPassword(password);
        //send to backend
        try {
        const response = await sendLoginData(email, username, hash);
        if (!response.ok) {
            // show backend error message like "Username already exists"
            errorDiv.textContent = response.error || "Registration failed";
            document.getElementById("user_entry").focus();
        } 
        else 
        {
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

async function sendLoginData(email, username, hashPassword){
    const response = await fetch("/login_api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
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