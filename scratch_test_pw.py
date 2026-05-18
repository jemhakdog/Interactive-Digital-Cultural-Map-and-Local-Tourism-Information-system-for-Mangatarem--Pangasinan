import sqlite3

def get_user_and_token():
    conn = sqlite3.connect("instance/mangatarem.db")
    c = conn.cursor()
    c.execute("SELECT id, email FROM user WHERE email LIKE '%jem%'")
    users = c.fetchall()
    print("Users found:", users)
    
    if not users:
        print("No users found.")
        return

    # For each user, let's see if they have a token
    c.execute("SELECT user_id, token, expires_at, used FROM password_reset_token")
    tokens = c.fetchall()
    print("Tokens:", tokens)

if __name__ == "__main__":
    get_user_and_token()
