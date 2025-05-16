
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
try:
    from flask_login import LoginManager, login_user, logout_user, login_required, current_user
except ImportError:
    raise ImportError("flask_login is not installed. Please install it with 'pip install flask-login'")
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import io
import csv

# Import forms
from forms import ContactForm, LoginForm, PredictionForm
# Import prediction functionality
from predict_model import predict_climate_risk
# Import models and db
from models import db, User, Contact, Prediction

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///climate_risk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Set login_view attribute
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html', now=datetime.now())

@app.route('/about')
def about():
    return render_template('about.html', now=datetime.now())

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = PredictionForm()
    result = None

    if form.validate_on_submit():
        # Get form data
        city = form.city.data
        population = form.population.data
        temperature_increase = form.temperature_increase.data
        urban_density = form.urban_density.data
        infrastructure = form.infrastructure.data

        # Make prediction
        result = predict_climate_risk(
            city=city,
            population=population,
            temperature_increase=temperature_increase,
            urban_density=urban_density,
            infrastructure=infrastructure
        )

        # Save prediction to database if user is logged in
        if current_user.is_authenticated:
            prediction = Prediction(
                user_id=current_user.id,
                city=city,
                population=population,
                temperature_increase=temperature_increase,
                urban_density=urban_density,
                infrastructure=infrastructure,
                risk_level=result.get('risk_level', 'unknown'),
                risk_score=result.get('risk_score', 0)
            )
            db.session.add(prediction)
            db.session.commit()
            flash('Prediction saved to your account', 'success')

    return render_template('predict.html', form=form, result=result, now=datetime.now())

@app.route('/download-report/<city>')
def download_report(city):
    """Generate and download a CSV report for a city"""
    # Get the most recent prediction for this city
    prediction = None
    
    if current_user.is_authenticated:
        prediction = Prediction.query.filter_by(
            user_id=current_user.id, 
            city=city
        ).order_by(Prediction.date.desc()).first()
        
        if not prediction:
            flash('No prediction data available for the specified city.', 'warning')
            return redirect(url_for('index'))
    # For non-authenticated users, we'll use sample data (handled below)
    
    # Create a CSV string
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['Urban Climate Risk Report'])
    writer.writerow(['Generated on', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    
    if prediction:
        # Use actual prediction data
        writer.writerow(['City', 'Population', 'Temperature Increase', 'Urban Density', 'Infrastructure', 'Risk Level', 'Risk Score'])
        writer.writerow([
            prediction.city,
            prediction.population,
            prediction.temperature_increase,
            prediction.urban_density,
            prediction.infrastructure,
            prediction.risk_level,
            f"{prediction.risk_score}%"
        ])
        temp_increase = prediction.temperature_increase
    else:
        # Use sample data
        writer.writerow(['City', 'Population', 'Temperature Increase', 'Urban Density', 'Infrastructure', 'Risk Level', 'Risk Score'])
        writer.writerow([city, '500000', '1.5', 'medium', 'moderate', 'medium', '55%'])
        temp_increase = 1.5
    
    writer.writerow([])
    writer.writerow(['Future Projections (2023-2030)'])
    writer.writerow(['Year', 'Projected Temperature (°C)', 'Projected Rainfall (mm)', 'Projected Flood Risk (%)'])
    
    # Generate some sample projection data
    base_temp = 25.0
    base_rain = 800
    base_risk = 30
    
    for i, year in enumerate(range(2023, 2031)):
        projected_temp = round(base_temp + (i * temp_increase / 8), 1)
        projected_rain = round(base_rain - (i * 25))
        projected_risk = min(100, round(base_risk + (i * 3)))
        writer.writerow([year, projected_temp, projected_rain, f"{projected_risk}%"])
    
    # Create response with CSV data
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={city}_climate_report.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Save contact message to database
        contact = Contact(
            name=form.name.data or '',
            email=form.email.data or '',
            message=form.message.data or ''
        )
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, now=datetime.now())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password:  # This checks for None and empty string
            password_str: str = user.password  # Type annotation to help type checker
            if check_password_hash(password_str, form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid email or password', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, now=datetime.now())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/climate-data', methods=['GET'])
def climate_data():
    # This would typically come from a database or API
    # For demo purposes, we'll return mock data
    data = {
        'temperature': [
            {'year': 2023, 'value': 25.8},
            {'year': 2024, 'value': 26.2},
            {'year': 2025, 'value': 26.7},
            {'year': 2026, 'value': 27.1},
            {'year': 2027, 'value': 27.6},
            {'year': 2028, 'value': 28.0},
            {'year': 2029, 'value': 28.5},
            {'year': 2030, 'value': 29.0}
        ],
        'rainfall': [
            {'year': 2023, 'value': 800},
            {'year': 2024, 'value': 750},
            {'year': 2025, 'value': 900},
            {'year': 2026, 'value': 650},
            {'year': 2027, 'value': 1000},
            {'year': 2028, 'value': 850},
            {'year': 2029, 'value': 700},
            {'year': 2030, 'value': 600}
        ]
    }
    return jsonify(data)

# Add the jinja context processor for current year
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Flask 2.0+ uses this instead of @app.before_first_request
with app.app_context():
    db.create_all()
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            name='Admin User',
            email='admin@example.com',
            password=generate_password_hash('password'),  # Change in production
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
