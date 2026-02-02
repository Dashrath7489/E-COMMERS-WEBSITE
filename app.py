from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Dash%407489@localhost/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)



# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html')  # Changed from home.html to index.html
    else:
        return redirect(url_for('login'))
    
    
# ye jo hai ye hashing password ke liye hai


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         if User.query.filter_by(email=email).first():
#             flash('User already exists!', 'warning')
#             return redirect(url_for('signup'))

#         hashed_password = generate_password_hash(password)
#         new_user = User(email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Signup successful! Please login.', 'success')
#         return redirect(url_for('login'))

#     return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('User already exists!', 'warning')
            return redirect(url_for('signup'))

        # ⚠️ Saving password as plain text (INSECURE)
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')




# ye jo hai ye hashing password ke liye hai


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'username' in session:
#         return redirect(url_for('home'))

#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = User.query.filter_by(email=email).first()
#         if user and check_password_hash(user.password, password):
#             session['username'] = email
#             flash("Login successful!", "success")
#             return redirect(url_for('home'))
#         else:
#             flash("Invalid credentials", "danger")

#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # Plain-text password check (INSECURE)
        if user and user.password == password:
            session['username'] = email
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
