# SkySearch - Flight Booking Web App
NYU CS-GY 6083 Spring 2026 - Problem Set 3, Problem 1

## Setup

### 1. Load the database
```bash
psql -U postgres -c "CREATE DATABASE flights_db;"
psql -U postgres -d flights_db -f flights.sql
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure database connection
```bash
cp .env.example .env
# Edit .env with your postgres password
```

Then export the variables before running:
```bash
export DB_PASSWORD=your_password_here
# or on Windows:
set DB_PASSWORD=your_password_here
```

### 4. Run the app
```bash
python app.py
```

Visit: http://127.0.0.1:5000

---

## Usage

| Step | Action |
|------|--------|
| (a) Start page | Enter origin code (e.g. `JFK`), destination (e.g. `LAX`), and a date range |
| (b) Results | All matching flights are listed with flight number, date, route, airline, and departure time |
| (c) Detail | Click any flight row to see seat capacity, booked count, available seats, and a visual seat map |

## Test queries (with provided data)
- JFK → LAX, 2025-12-29 to 2025-12-31 → returns AA101, AA205
- ATL → MIA, 2025-12-31 to 2025-12-31 → returns DL410
- SFO → ORD, 2025-12-31 to 2025-12-31 → returns UA302 (fully booked)

## Project structure
```
flights_app/
├── app.py               # Flask routes
├── requirements.txt
├── .env.example
├── templates/
│   ├── base.html        # Shared layout + CSS
│   ├── index.html       # Search form + results (parts a & b)
│   └── detail.html      # Seat availability (part c)
└── flights.sql          # Database schema + data
```
## Screenshots
<img width="1470" height="925" alt="q11" src="https://github.com/user-attachments/assets/98664127-61e3-436d-ab03-5ee33cc51e76" />
<img width="1470" height="925" alt="q12" src="https://github.com/user-attachments/assets/a494b27a-41b7-4e8d-a4d5-6abe811a6785" />
<img width="1470" height="925" alt="q13" src="https://github.com/user-attachments/assets/f901141f-6cc7-438a-b7f9-71655533e439" />
<img width="1470" height="925" alt="q14" src="https://github.com/user-attachments/assets/90de9409-6bd0-472c-b53a-e43568cc7d49" />




