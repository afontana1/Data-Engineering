import json
from flask import jsonify, request
from app import app
from app import db
from models.user import User


@app.route("/users")
def users():
    """
    Get a list of users filtered by email.
    ---
    parameters:
      - name: email
        in: query
        type: string
        required: false
        description: Email address to filter users.
      - name: pageSize
        in: query
        type: integer
        required: false
        description: Page Size to return the number of records.
      - name: pageToken
        in: query
        type: integer
        required: false
        description: Page Token to get the records beyond this value.
    responses:
      200:
        description: List of users matching the filter.
    """
    page_token = (
        int(request.args.get("pageToken")) if request.args.get("pageToken") else None
    )
    search_email = request.args.get("email", "")
    page_size = (
        int(request.args.get("pageSize"))
        if request.args.get("pageSize") and int(request.args.get("pageSize")) <= 100
        else 25
    )
    # logic_on_true if cond else logic_on_false
    if search_email:
        # Query the database and filter users based on the pattern match
        if page_token:
            user_recs = (
                db.session.query(User)
                .filter(User.email.like(f"{search_email.lower()}%"))
                .filter(User.id > page_token)
                .order_by(User.id)
                .limit(page_size)
                .all()
            )
        else:
            user_recs = (
                db.session.query(User)
                .filter(User.email.like(f"{search_email.lower()}%"))
                .order_by(User.id)
                .limit(page_size)
                .all()
            )
    else:
        # Retrieve all users if no search query is provided
        if page_token:
            user_recs = (
                db.session.query(User)
                .filter(User.id > page_token)
                .order_by(User.id)
                .limit(page_size)
                .all()
            )
        else:
            user_recs = db.session.query(User).order_by(User.id).limit(page_size).all()

    users = []
    for user in user_recs:
        user.__dict__.pop("_sa_instance_state")
        users.append(user.__dict__)

    payload = {
        "records": users,
        "recordCount": len(users),
        "pageToken": users[-1]["id"] if len(users) == page_size else None,
    }

    return jsonify(payload), 200


@app.route("/users", methods=["POST"])
def add_users():
    users = json.loads(request.form["users"])
    users_ = []
    for user in users:
        users_.append(User(**user))
    db.session.add_all(users_)
    db.session.commit()
    return jsonify({"message": "Users added successfully..."}), 201


@app.route("/user", methods=["GET"])
def get_user():
    """
    Get user details.
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: ID of the user.
    responses:
      200:
        description: User details.
    """
    id = request.args.get("id")
    if id:
        user = User.query.get(id)
        user.__dict__.pop("_sa_instance_state")
        return jsonify(user.__dict__), 200


@app.route("/user", methods=["POST"])
def create_or_update_user():
    """
    Create or update a user.
    ---
    parameters:
      - name: id
        in: formData
        type: integer
        required: false
        description: ID of the user.
      - name: first_name
        in: formData
        type: string
        required: true
        description: First name of the user.
      - name: last_name
        in: formData
        type: string
        required: true
        description: Last name of the user.
      - name: username
        in: formData
        type: string
        required: true
        description: Username of the user.
      - name: email
        in: formData
        type: string
        required: true
        description: Email address of the user.
    responses:
      201:
        description: User added successfully.
      200:
        description: User updated successfully.
    """
    id = request.form["id"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    username = request.form["username"]
    email = request.form["email"]
    if id:
        user = User.query.get(id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        db.session.commit()
        return jsonify({"message": "User updated successfully..."}), 200
    else:
        user = User(
            first_name=first_name, last_name=last_name, username=username, email=email
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added successfully..."}), 201


@app.route("/user", methods=["DELETE"])
def delete_user():
    """
    Delete a user.
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: ID of the user.
    responses:
      204:
        description: User deleted successfully.
    """
    id = request.args.get("id")
    if id:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully..."}), 204
