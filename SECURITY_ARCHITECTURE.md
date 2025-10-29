# FinLynq — Security Summary

- Use HTTPS in production
- Set a strong SECRET_KEY and never commit it
- Replace in-memory USERS with real DB and hashed passwords (bcrypt/argon2)
- Verify payment provider webhooks via HMAC signature
