from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title is required and must be a non-empty string"
        }), 400

    new_id = max(
        [event.id for event in events],
        default=0
    ) + 1

    new_event = Event(new_id, title.strip())
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "Title is required and must be a non-empty string"
        }), 400

    for event in events:
        if event.id == event_id:
            event.title = title.strip()

            return jsonify(event.to_dict()), 200

    return jsonify({
        "error": "Event not found"
    }), 404


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event.id == event_id:
            events.remove(event)

            return jsonify({
                "message": "Event deleted successfully"
            }), 204

    return jsonify({
        "error": "Event not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)