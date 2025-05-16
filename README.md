
# Urban Climate Risk Predictor

A machine learning project that predicts climate risks for urban areas through 2030.

## Project Structure

```
urban_climate_risk_predictor/
│
├── static/               # Static files (CSS, JS, images)
│   ├── css/              # CSS stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Image files
│
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── predict.html      # Prediction page
│   ├── about.html        # About page
│   ├── contact.html      # Contact page
│   ├── login.html        # Login page
│   └── dashboard.html    # Admin dashboard
│
├── models/               # Trained ML models
│   └── climate_model.pkl # Pickled model file
│
├── notebooks/            # Jupyter notebooks
│   └── train.ipynb       # Model training notebook
│
├── app.py                # Main Flask application
├── forms.py              # Flask-WTF form definitions
├── models.py             # Database models
├── predict_model.py      # Prediction functionality
└── requirements.txt      # Project dependencies
```

## Installation Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd urban_climate_risk_predictor
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

6. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Required Packages
- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- pickle
