# test/hardcoded_jwt_secret.py
import jwt
import datetime

# Vulnerable: hard-coded JWT secret key
JWT_SECRET = "this_is_a_super_secret_key_that_should_not_be_committed"

def create_token(user_id):
    payload = {"sub": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

if __name__ == "__main__":
    print(create_token("user-123"))
