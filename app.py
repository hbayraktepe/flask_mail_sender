import time

from flask import Flask, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

from mailer import Mailer
from mongodb_manager import MongoDBManager

app = Flask(__name__)
app.secret_key = "supersecretkey"

request_count = 0
last_reset_time = time.time()

mailer = Mailer()
mongodb_manager = MongoDBManager()


class MessageForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=1, max=500)]
    )


def validate_json(json_data):
    form = MessageForm(data=json_data, meta={"csrf": False})

    # Check the presence of columns
    expected_columns = {"name", "email", "message"}  # Expected columns
    received_columns = set(json_data.keys())  # Received columns

    unexpected_columns = received_columns - expected_columns

    if unexpected_columns:
        return False, f"Unexpected column(s): {', '.join(unexpected_columns)}"

    return form.validate(), form.errors


@app.before_request
def limit_requests():
    global request_count, last_reset_time

    # Get the current time
    current_time = time.time()

    # Reset the request count if more than a minute has passed
    if current_time - last_reset_time > 60:
        request_count = 0
        last_reset_time = current_time

    # Maximum number of requests
    max_requests = 120

    if request_count >= max_requests:
        return jsonify({"error": "Too many requests. Please try again later."}), 429

    request_count += 1


@app.route("/send-mail", methods=["POST"])
def index():
    json_data = request.json

    is_valid, errors = validate_json(json_data)

    if not json_data or not is_valid:
        return jsonify({"error": "Invalid JSON format or data", "errors": errors}), 400

    # Store the data in MongoDB
    response, status_code = mongodb_manager.store_data(
        json_data["name"], json_data["email"], json_data["message"]
    )

    if status_code == 200:
        # Call the function for sending email
        mailer.send_email(json_data["name"], json_data["email"], json_data["message"])

    return response, status_code


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
