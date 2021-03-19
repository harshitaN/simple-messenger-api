import flask
from flask import request, jsonify
from utils import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(InvalidParams)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/', methods=['GET'])
def home():
    return "<h1>Simple Messenger API</h1>"


@app.route('/api/send/', methods=['POST'])
def send_message():
    """
    Send message from recipient to sender
    """
    query_parameters = request.get_json()
    sender_id = query_parameters.get("sender_id")
    recipient_id = query_parameters.get("recipient_id")
    message = query_parameters.get("message")
    if not (recipient_id and sender_id and message):
        raise InvalidParams("Sender and recipient and message params are required", status_code=400)
    if sender_id == recipient_id:
        raise InvalidParams("Sender and recipient cannot be the same", status_code=400)
    date_time = int(datetime.now().timestamp())

    conn, cur = connect_db()
    cur.execute("INSERT INTO messages(sender_id, recipient_id, message, datetime) VALUES (?,?,?,?)",
                (int(sender_id), int(recipient_id), message, date_time))
    conn.commit()
    return jsonify({"message": "success"})


@app.route('/api/messages/all', methods=['GET'])
def get_all_messages():
    """
    Get all messages from all senders with time limit or count limit
    """
    query_parameters = request.args
    limit = query_parameters.get("limit")
    thirty_days = query_parameters.get("thirty_days")

    full_query = "".join(("SELECT * FROM messages ", get_limit_query(limit, thirty_days, True)))
    conn, cur = connect_db()
    all_messages = cur.execute(full_query).fetchall()
    return jsonify(all_messages)

@app.route('/api/messages/', methods=['GET'])
def get_recipient_messages():
    """
    Get all messages from a recipient to a sender with time limit or count limit
    """
    query_parameters = request.args
    limit = query_parameters.get("limit")
    thirty_days = query_parameters.get("thirty_days")
    sender_id = query_parameters.get("sender_id")
    recipient_id = query_parameters.get("recipient_id")
    if not (recipient_id and sender_id):
        raise InvalidParams("Sender and recipient params are required", status_code=400)

    full_query = "".join(("SELECT * FROM messages WHERE sender_id = ?  and recipient_id = ? ",
                         get_limit_query(limit, thirty_days, False)))
    conn, cur = connect_db()
    results = cur.execute(full_query, (int(sender_id), int(recipient_id))).fetchall()
    return jsonify(results)


app.run()