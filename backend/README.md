# Flask RFID Payment System API Documentation

This documentation provides an overview of the Flask API endpoints used to manage a payment system where RFID tags can be linked to user accounts for transactions.

## Table of Contents

1. [Overview](#overview)
2. [Database Structure](#database-structure)
3. [API Endpoints](#api-endpoints)
   - [Register User](#register-user)
   - [Connect User (Login)](#connect-user-login)
   - [Connect RFID Tag to User](#connect-rfid-tag-to-user)
   - [Disconnect RFID Tag](#disconnect-rfid-tag)
   - [Add Balance](#add-balance)
   - [Set Balance](#set-balance)
   - [Get User Balance](#get-user-balance)
   - [Get User of Tag](#get-user-of-tag)
4. [Run the Application](#run-the-application)

---

## Overview

The Flask RFID Payment System API allows users to:
- Register and authenticate user accounts.
- Associate RFID tags with users.
- Perform balance-related transactions, such as adding and removing funds.

The API communicates with an SQLite database to store user information, RFID tag associations, and balances.

---

## Database Structure

### Tables:
- **users**: Stores user information.
  - `id`: Unique identifier for the user.
  - `username`: User's name (unique).
  - `password`: Hashed password.
  - `balance`: User's account balance.

- **tags**: Stores RFID tag associations.
  - `tag_id`: Unique identifier for the RFID tag.
  - `user_id`: ID of the user associated with the tag.

---

## API Endpoints

### 1. **Register User**

**Endpoint**: `/registerUser`  
**Method**: `POST`  
**Description**: Registers a new user with a username and password.

**Request Body**:

```json
{
  "username": "string",
  "password": "string"
}
```

**Responses:**
- `201`: User registered successfully.
- `400`: Username already exists or missing required fields.

### 2. **Connect User (Login)**

**Endpoint**: `/connectUser`
**Method**: `POST`
**Description**: Authenticates a user with a username and password.

**Request Body**:

```json
{
  "username": "string",
  "password": "string"
}
```

**Responses**:
- `200`: User connected successfully with user_id.
- `401`: Invalid username or password.
- `400`: Missing required fields.

### 3. **Connect RFID Tag to User**

**Endpoint**: `/connectTagWithUser`
**Method**: `POST`
**Description**: Links an RFID tag to a user.

**Request Body**:

```json
{
  "tag_id": "string",
  "user_id": "integer"
}
```

**Responses**:

- `200`: Tag connected to user successfully.
- `400`: Missing required fields.

### 4. **Disconnect RFID Tag**

**Endpoint**: `/disconnectTag`
**Method**: `POST`
**Description**: Unlinks an RFID tag from any associated user.

**Request Body**:

```json
{
  "tag_id": "string"
}
```

**Responses**:

- `200`: Tag disconnected successfully.
- `400`: Missing required fields.

### 5. **Add Balance**

**Endpoint**: `/addBalance`
**Method**: `POST`
**Description**: Adds balance to a user's account using an RFID tag.

**Request Body**:

```json
{
  "tag_id": "string",
  "amount": "float"
}
```

**Responses**:

- `200`: Balance added successfully.
- `400`: Missing required fields.
- `404`: Tag not associated with any user.

### 6. **Set Balance**

**Endpoint**: `/setBalance`
**Method**: `POST`
**Description**: Set balance from a user's account using an RFID tag.

**Request Body**:

```json
{
  "tag_id": "string",
  "amount": "float"
}
```

**Responses**:

- `200`: Balance set successfully.
- `400`: Missing required fields.
- `404`: Tag not associated with any user.

### 7. **Get User Balance**

**Endpoint**: `/getBalance`
**Method**: `GET`
**Description**: Retrieves the balance of a user.

**Query Parameters**:

- `user_id`: User's ID.

**Responses**:

- `200`: Returns the user's balance.
- `400`: Missing required fields.
- `404`: User not found.

### 8. **Get User of Tag**

**Endpoint**: `/getUserOfTag`
**Method**: `GET`
**Description**: Retrieves the user associated with a tag.

**Query Parameters**:

- `tag_id`: Tag's ID.

**Responses**:

- `200`: Returns the tag's associated user.
- `400`: Missing required fields.
- `404`: Tag not found.



## Run the Application

1. **Install `UV`**
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Create a venv**

```
uv venv
```

3. **Install dependencies**

```uv pip sync requirements.txt```

4. **Run the backend**

```
source .venv/bin/activate
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

5. (Optional) **Add backend as a linux service with `systemctl`**

Put the following (and modify as needed) in `/etc/systemd/system/flask-drink-payment.service` :

```
[Unit]
Description=Flask Drink Payment System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/objetconnecte
ExecStart=/home/ubuntu/objetconnecte/.venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
Restart=always
Environment="PATH=/home/ubuntu/objetconnecte/.venv/bin"
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

Then, restart services with `sudo systemctl daemon-reload`
