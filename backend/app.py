from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# Utility to connect to the database
def connect_db():
    conn = sqlite3.connect('payment_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

### Endpoints ###

# 1. Register a new user
@app.route('/registerUser', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing 'username' or 'password'"}), 400

    hashed_password = hash_password(password)
    
    with connect_db() as conn:
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return jsonify({"message": "User registered successfully"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Username already exists"}), 400

# 2. Connect user (login)
@app.route('/connectUser', methods=['POST'])
def connect_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing 'username' or 'password'"}), 400

    hashed_password = hash_password(password)
    
    with connect_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                            (username, hashed_password)).fetchone()
        if user:
            return jsonify({"message": "User connected successfully", "user_id": user['id']}), 200
        return jsonify({"error": "Invalid username or password"}), 401

# 3. Connect RFID tag to a user
@app.route('/connectTagWithUser', methods=['POST'])
def connect_tag_with_user():
    data = request.json
    tag_id = data.get('tag_id')
    user_id = data.get('user_id')

    if not tag_id or not user_id:
        return jsonify({"error": "Missing 'tag_id' or 'user_id'"}), 400

    with connect_db() as conn:
        conn.execute("INSERT OR REPLACE INTO tags (tag_id, user_id) VALUES (?, ?)", (tag_id, user_id))
        conn.commit()
        return jsonify({"message": "Tag connected to user successfully"}), 200

# 4. Disconnect RFID tag
@app.route('/disconnectTag', methods=['POST'])
def disconnect_tag():
    data = request.json
    tag_id = data.get('tag_id')

    if not tag_id:
        return jsonify({"error": "Missing 'tag_id'"}), 400

    with connect_db() as conn:
        conn.execute("DELETE FROM tags WHERE tag_id = ?", (tag_id,))
        conn.commit()
        return jsonify({"message": "Tag disconnected successfully"}), 200

# 5. Add balance to user account
@app.route('/addBalance', methods=['POST'])
def add_balance():
    data = request.json
    tag_id = data.get('tag_id')
    amount = data.get('amount')

    if not tag_id or amount is None:
        return jsonify({"error": "Missing 'tag_id' or 'amount'"}), 400

    with connect_db() as conn:
        cursor = conn.execute("SELECT user_id FROM tags WHERE tag_id = ?", (tag_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Tag not associated with any user"}), 404

        user_id = user['user_id']
        conn.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
        conn.commit()
        return jsonify({"message": "Balance added successfully"}), 200

# 6. Remove balance from user account
@app.route('/removeBalance', methods=['POST'])
def remove_balance():
    data = request.json
    tag_id = data.get('tag_id')
    amount = data.get('amount')

    if not tag_id or amount is None:
        return jsonify({"error": "Missing 'tag_id' or 'amount'"}), 400

    with connect_db() as conn:
        cursor = conn.execute("SELECT user_id, balance FROM users INNER JOIN tags ON users.id = tags.user_id WHERE tag_id = ?", (tag_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Tag not associated with any user"}), 404
        if user['balance'] < amount:
            return jsonify({"error": "Insufficient balance"}), 400

        user_id = user['user_id']
        conn.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
        conn.commit()
        return jsonify({"message": "Balance deducted successfully"}), 200

# 7. Get user balance
@app.route('/getBalance', methods=['GET'])
def get_balance():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing 'user_id'"}), 400

    with connect_db() as conn:
        cursor = conn.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            return jsonify({"balance": user['balance']}), 200
        return jsonify({"error": "User not found"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
