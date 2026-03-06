from flask import Flask, render_template, request
from flask import session, redirect, url_for
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="car_rental_db",
        user="postgres",
        password="Y@sser2105"
    )
    return conn

app = Flask(__name__)

app.secret_key = "supersecretkey"

#  Home Route
@app.route('/')
def home():
    return render_template('index.html')

#  Booking Route
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    car = request.form['car']
    days = int(request.form['days'])

    prices = {
        "Swift": 1000,
        "Wagonr": 1000,
        "Dzire": 1000,
        "Ertiga": 2500,
        "Innova Crysta": 4500
    }

    price = prices.get(car)

    if not price:
        return "Invalid Car Selected"

    total = price * days

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO bookings (customer_name, car, days, total_amount) VALUES (%s, %s, %s, %s)",
        (name, car, days, total)
    )

    conn.commit()
    cur.close()
    conn.close()

    return render_template(
    'confirmation.html',
    name=name,
    car=car,
    days=days,
    total=total
)

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM bookings ORDER BY id DESC;")
    bookings = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('admin.html', bookings=bookings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['admin'] = username
            return redirect(url_for('admin'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/delete/<int:id>')
def delete_booking(id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM bookings WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True)