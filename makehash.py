import bcrypt

users = [
    {
        "id": "staff123",
        "password": "staff123",   
        "status": "staff"
    },
    {
        "id": "dinesh",
        "password": "dinesh@123",   
        "status": "staff"
    },
    {
        "id": "admin",
        "password": "admin123",   
        "status": "admin"
    },
    {
        "id": "happy",
        "password": "123",   
        "status": "staff"
    }
]

# Hash the passwords
for user in users:
    user['password'] = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Output the updated list with hashed passwords
for user in users:
    print(f"ID: {user['id']}, Hashed Password: {user['password']}, Status: {user['status']}")
