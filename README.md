# Travel Booking System

A learning project for browsing trips and recording sample bookings.

## Stack
Python 3, Flask, Flask-SQLAlchemy (SQLite), HTML, CSS, vanilla JavaScript.

## Changes in this customized version
- Searchable destination cards and trip duration/price filters
- Seat availability and booking confirmation
- Persistent booking records with safe server-side validation
- Responsive layout and demo data

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000. The app creates a local SQLite database and sample trips on first run.

## Source and attribution
Feature inspiration: [Mi71am/travelling_booking](https://github.com/Mi71am/travelling_booking), MIT License. This repository contains a simplified, reworked implementation for practice; original copyright notice is retained in LICENSE.

Demo only: use fictional data. No real bookings or payments are processed.
