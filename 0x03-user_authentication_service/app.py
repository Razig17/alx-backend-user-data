#!/usr/bin/env python3
"""Flask app module"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


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
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect("/")
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
