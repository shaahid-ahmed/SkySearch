from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "dbname":   os.getenv("DB_NAME", "flights_db"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def get_airports():
    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT airport_code, name, city FROM Airport ORDER BY city, airport_code")
        airports = cur.fetchall()
        cur.close()
        conn.close()
        return airports
    except Exception:
        return []


@app.route("/", methods=["GET", "POST"])
def index():
    flights  = None
    error    = None
    form     = {}
    airports = get_airports()

    if request.method == "POST":
        origin      = request.form.get("origin", "").strip().upper()
        destination = request.form.get("destination", "").strip().upper()
        date_from   = request.form.get("date_from", "").strip()
        date_to     = request.form.get("date_to", "").strip()
        form = {"origin": origin, "destination": destination,
                "date_from": date_from, "date_to": date_to}

        if not all([origin, destination, date_from, date_to]):
            error = "Please fill in all fields."
        else:
            try:
                conn = get_conn()
                cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cur.execute("""
                    SELECT
                        f.flight_number,
                        f.departure_date,
                        fs.origin_code,
                        fs.dest_code,
                        fs.departure_time,
                        fs.airline_name,
                        fs.duration
                    FROM Flight f
                    JOIN FlightService fs ON fs.flight_number = f.flight_number
                    WHERE fs.origin_code  = %s
                      AND fs.dest_code    = %s
                      AND f.departure_date BETWEEN %s AND %s
                    ORDER BY f.departure_date, fs.departure_time
                """, (origin, destination, date_from, date_to))
                flights = cur.fetchall()
                cur.close()
                conn.close()
                if not flights:
                    error = f"No flights found from {origin} to {destination} in that date range."
            except Exception as e:
                error = f"Database error: {e}"

    return render_template("index.html", flights=flights, error=error, form=form, airports=airports)


@app.route("/flight/<flight_number>/<departure_date>")
def flight_detail(flight_number, departure_date):
    error  = None
    detail = None

    try:
        conn = get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Flight + aircraft info
        cur.execute("""
            SELECT
                f.flight_number,
                f.departure_date,
                f.plane_type,
                fs.airline_name,
                fs.origin_code,
                fs.dest_code,
                fs.departure_time,
                fs.duration,
                ac.capacity,
                o.name  AS origin_name,
                o.city  AS origin_city,
                d.name  AS dest_name,
                d.city  AS dest_city
            FROM Flight f
            JOIN FlightService fs ON fs.flight_number  = f.flight_number
            JOIN Aircraft      ac ON ac.plane_type      = f.plane_type
            JOIN Airport        o ON o.airport_code     = fs.origin_code
            JOIN Airport        d ON d.airport_code     = fs.dest_code
            WHERE f.flight_number  = %s
              AND f.departure_date = %s
        """, (flight_number, departure_date))
        detail = cur.fetchone()

        if detail:
            # Booked seats count
            cur.execute("""
                SELECT COUNT(*) AS booked
                FROM Booking
                WHERE flight_number  = %s
                  AND departure_date = %s
            """, (flight_number, departure_date))
            booked_row = cur.fetchone()
            booked = booked_row["booked"] if booked_row else 0
            detail = dict(detail)
            detail["booked"]    = booked
            detail["available"] = detail["capacity"] - booked

            # Booked seat numbers
            cur.execute("""
                SELECT b.seat_number, p.passenger_name
                FROM Booking b
                JOIN Passenger p ON p.pid = b.pid
                WHERE b.flight_number  = %s
                  AND b.departure_date = %s
                ORDER BY b.seat_number
            """, (flight_number, departure_date))
            detail["seats"] = cur.fetchall()

        cur.close()
        conn.close()
    except Exception as e:
        error = f"Database error: {e}"

    return render_template("detail.html", detail=detail, error=error)


if __name__ == "__main__":
    app.run(debug=True)
