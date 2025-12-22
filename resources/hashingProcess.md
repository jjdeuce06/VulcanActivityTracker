# Password Authentication Design (Hashed-Before-Transmission)

## Overview

This project enforces a strict security requirement:

> **Plaintext passwords must never be transmitted over the API.**

To satisfy this requirement while still allowing secure authentication, the system uses a **two-stage hashing approach**:

1. **Client-side hashing** to protect the raw password in transit  
2. **Server-side password hashing (Argon2id)** to protect stored credentials  

This design ensures that:
- The server never sees plaintext passwords
- The database never stores reversible or fast hashes
- Secure login verification remains possible

---

## Threat Model

The system is designed to protect against:
- Network interception
- Database compromise
- Offline brute-force attacks

HTTPS is assumed and required for all authentication requests.

---

## Registration Flow

### Step 1: Client-Side Hashing

When a user registers, the client hashes the password **before transmission** using a fast cryptographic hash function:

```
password → SHA-256 → clientPasswordHash
```

Only `clientPasswordHash` is sent to the server.

---

### Step 2: Server-Side Hashing (Credential Storage)

Upon receiving the client hash, the server applies a **slow, memory-hard password hashing algorithm (Argon2id)**:

```
clientPasswordHash → Argon2id → storedPasswordHash
```

The server stores `storedPasswordHash` in the database.

Argon2id automatically provides:
- A unique salt per user
- Tunable cost parameters
- Constant-time verification

---

## Login Flow

### Step 1: Client-Side Hashing

During login, the client repeats the same hashing process:

```
password → SHA-256 → clientPasswordHash
```

The raw password is never transmitted.

---

### Step 2: Server-Side Verification

The server retrieves the stored hash and verifies it against the received client hash:

```
Argon2id.verify(storedPasswordHash, clientPasswordHash)
```

- Verification succeeds → authentication granted  
- Verification fails → authentication denied  

---

## Security Properties

### Network Security
- Plaintext passwords are never sent over the API
- HTTPS protects all authentication requests
- Client-side hashes are non-reversible

### Database Security
- Passwords are stored using Argon2id
- Salts and parameters are embedded in the hash
- Offline cracking is computationally expensive

### Defense in Depth
- Fast hashing protects transport
- Slow hashing protects storage
- Compromise of one layer does not expose credentials

---

## Implementation Notes

- Client-side hashing uses SHA-256 via the Web Crypto API
- Server-side hashing uses Argon2id
- Client-side hashes are treated as sensitive credentials
- Generic login error messages prevent account enumeration
- Login attempts should be rate-limited

---

## Limitations

- Client-side hashes function as password equivalents
- Replay attacks are possible without TLS or session controls
- HTTPS remains mandatory despite hashing

---

## Conclusion

This design satisfies the requirement that **plaintext passwords are never transmitted** while maintaining secure authentication. By combining client-side hashing with server-side Argon2id hashing, the system provides strong protection against both network-level and database-level threats.
