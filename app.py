from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2

app = Flask(__name__)
app.secret_key = "supersecretkey"

# 🔗 Database Connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="car_rental_db",
        user="postgres",
        password="Y@sser2105"
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('user_login'))

    return render_template('register.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Login"

    return render_template('user_login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('user_login'))

    return render_template('dashboard.html')

@app.route('/user_logout')
def user_logout():
    session.pop('user', None)
    return redirect(url_for('user_login'))

# 🏠 Home
@app.route('/')
def home():
    return render_template('index.html')

# 🚗 Booking
@app.route('/book', methods=['POST'])
def book():
    name = request.form.get('name')
    car = request.form.get('car')
    days = request.form.get('days')
    mobile = request.form.get('mobile')

    if not name or not car or not days:
        return "All fields are required!"

    days = int(days)

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
    "INSERT INTO bookings (customer_name, car, days, total_amount, mobile) VALUES (%s, %s, %s, %s, %s)",
    (name, car, days, total, mobile)
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

# 🔐 Admin Panel
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM bookings ORDER BY id DESC")
    bookings = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('admin.html', bookings=bookings)

# 🔑 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['admin'] = username
            return redirect(url_for('admin'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')

# 📩 Contact Form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            return "All fields are required!"

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )

        conn.commit()
        cur.close()
        conn.close()

        return "Message Sent Successfully!"

    return render_template('contact.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

# ❌ Delete Booking
@app.route('/delete/<int:id>')
def delete_booking(id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM bookings WHERE id=%s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('admin'))

# ▶ Run App
if __name__ == "__main__":
    app.run(debug=True)














# from flask import Flask, render_template, request
# from flask import session, redirect, url_for
# import psycopg2

# def get_db_connection():
#     conn = psycopg2.connect(
#         host="localhost",
#         database="car_rental_db",
#         user="postgres",
#         password="Y@sser2105"
#     )
#     return conn

# app = Flask(__name__)

# app.secret_key = "supersecretkey"

# #  Home Route
# @app.route('/')
# def home():
#     return render_template('index.html')

# #  Booking Route
# @app.route('/book', methods=['POST'])
# def book():
#     name = request.form['name']
#     car = request.form['car']
#     days = int(request.form['days'])

#     prices = {
#         "Swift": 1000,
#         "Wagonr": 1000,
#         "Dzire": 1000,
#         "Ertiga": 2500,
#         "Innova Crysta": 4500
#     }

#     price = prices.get(car)

#     if not price:
#         return "Invalid Car Selected"

#     total = price * days

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "INSERT INTO bookings (customer_name, car, days, total_amount) VALUES (%s, %s, %s, %s)",
#         (name, car, days, total)
#     )

#     conn.commit()
#     cur.close()
#     conn.close()

#     return render_template(
#     'confirmation.html',
#     name=name,
#     car=car,
#     days=days,
#     total=total
# )

# @app.route('/admin')
# def admin():
#     if 'admin' not in session:
#         return redirect(url_for('login'))

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM bookings ORDER BY id DESC;")
#     bookings = cur.fetchall()

#     cur.close()
#     conn.close()

#     return render_template('admin.html', bookings=bookings)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
#         user = cur.fetchone()

#         cur.close()
#         conn.close()

#         if user:
#             session['admin'] = username
#             return redirect(url_for('admin'))
#         else:
#             return "Invalid Credentials"

#     return render_template('login.html')

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         message = request.form.get('message')

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute(
#             "INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)",
#             (name, email, message)
#         )
#         conn.commit()

#         cur.close()
#         conn.close()

#         return "Message Sent Successfully!"

#     return render_template('contact.html')

# @app.route('/logout')
# def logout():
#     session.pop('admin', None)
#     return redirect(url_for('login'))

# @app.route('/delete/<int:id>')
# def delete_booking(id):
#     if 'admin' not in session:
#         return redirect(url_for('login'))

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute("DELETE FROM bookings WHERE id = %s", (id,))
#     conn.commit()

#     cur.close()
#     conn.close()

#     return redirect(url_for('admin'))

# if __name__ == "__main__":
#     app.run(debug=True)