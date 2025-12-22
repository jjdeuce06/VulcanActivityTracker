//this file will handle login click events, forma verification, and redirection
//will serve as api for login user account set up
//possibly hold password hashing functions but prob not


document.getElementById("loginBtn").addEventListener("click", async () =>{
    const username = document.getElementById("user_entry").value;
    const password = document.getElementById("pass_entry").value;

    console.log("Username:", username);
    console.log("Password:", password);

    //hash password before sending
    const hash = await hashPassword(password);
    //send to backend
    try {
        const response = await sendLoginData(username, hash);
        console.log("Response:", response);
    } catch (err) {
        console.error("Error sending login data:", err);
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

    console.log("Hashed Pass:", hashBuff);

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
    console.log("Sending Data", username, hashPassword);

    if(!response.ok){ throw new Error(`HTTP error ${response.status}`);}
        return await response.json();
}
