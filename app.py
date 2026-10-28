
#!/usr/bin/env python3

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


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True) or {}

    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_id = max((event.id for event in events), default=0) + 1
    event = Event(new_id, data["title"])
    events.append(event)

    return jsonify(event.to_dict()), 201


@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        event.title = data["title"]

    return jsonify(event.to_dict()), 200


@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
