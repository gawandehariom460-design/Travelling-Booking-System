import os
from datetime import date
from secrets import token_hex

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-this-key"),
    SQLALCHEMY_DATABASE_URI="sqlite:///travel_bookings.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)
CSRFProtect(app)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(240), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(12), unique=True, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"), nullable=False)
    travellers = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Date, default=date.today, nullable=False)
    trip = db.relationship("Trip")

def seed_trips():
    if Trip.query.count() == 0:
        db.session.add_all([
            Trip(title="Konkan Coast Escape", destination="Maharashtra", days=4, price=8999, seats=18, description="Sea forts, local food and quiet beach mornings."),
            Trip(title="Himalayan Valley Trail", destination="Himachal Pradesh", days=6, price=15999, seats=12, description="Mountain viewpoints, village walks and cool evenings."),
            Trip(title="Heritage Jaipur", destination="Rajasthan", days=3, price=7499, seats=20, description="Colourful markets, forts and a guided old-city walk."),
            Trip(title="Meghalaya Green Route", destination="Meghalaya", days=5, price=13999, seats=10, description="Waterfalls, forest paths and living-root bridges."),
        ])
        db.session.commit()

@app.route("/")
def home():
    seed_trips()
    term = request.args.get("q", "").strip()
    query = Trip.query
    if term:
        query = query.filter(Trip.destination.ilike(f"%{term}%") | Trip.title.ilike(f"%{term}%"))
    return render_template("index.html", trips=query.order_by(Trip.price).all(), term=term)

@app.post("/book/<int:trip_id>")
def book(trip_id):
    seed_trips()
    trip = db.get_or_404(Trip, trip_id)
    try:
        travellers = int(request.form.get("travellers", "1"))
    except ValueError:
        travellers = 0
    if not 1 <= travellers <= trip.seats:
        flash("Choose a valid number of travellers within the available seats.", "error")
        return redirect(url_for("home"))
    trip.seats -= travellers
    booking = Booking(reference=token_hex(4).upper(), trip=trip, travellers=travellers)
    db.session.add(booking)
    db.session.commit()
    flash(f"Demo booking confirmed. Reference: {booking.reference}", "success")
    return redirect(url_for("home"))

with app.app_context():
    db.create_all()
    seed_trips()

if __name__ == "__main__":
    app.run(debug=False)
