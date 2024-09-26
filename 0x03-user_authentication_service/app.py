#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """Home Route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Creates a User"""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """Login route"""
    email = request.form.get('email')
    password = request.form.get('password')
    login = AUTH.valid_login(email, password)
    if login is False:
        abort(401)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", AUTH.create_session(email))
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile")
def profile():
    """User Profile route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Gets reset_password token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Updating a user's password route"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
