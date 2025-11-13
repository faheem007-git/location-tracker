from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def mask_phone(phone):
    """Mask phone number except last 3 digits."""
    if len(phone) <= 3:
        return phone
    return "*" * (len(phone) - 3) + phone[-3:]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update", methods=["POST"])
def update_position():
    data = request.json
    phone = data.get("phone")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not (phone and latitude and longitude):
        return jsonify({"error": "Missing data"}), 400

    tracker = Tracker.query.filter_by(phone=phone).first()
    if tracker:
        tracker.latitude = latitude
        tracker.longitude = longitude
        tracker.updated_at = datetime.utcnow()
    else:
        tracker = Tracker(phone=phone, latitude=latitude, longitude=longitude)
        db.session.add(tracker)

    db.session.commit()
    return jsonify({"status": "updated"})


@app.route("/positions")
def positions():
    data = Tracker.query.all()
    return jsonify([
        {
            "phone": mask_phone(t.phone),
            "latitude": t.latitude,
            "longitude": t.longitude,
            "updated_at": t.updated_at.strftime("%H:%M:%S"),
        }
        for t in data
    ])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0",port=port)
