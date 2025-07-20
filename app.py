from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daily_reports.db'
db = SQLAlchemy(app)

class DailyReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(100), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.String(50), nullable=False)
    end_time = db.Column(db.String(50), nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    incident = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    checker_signature = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        report = DailyReport(
            driver_name=request.form['driver_name'],
            vehicle_number=request.form['vehicle_number'],
            start_time=request.form['start_time'],
            end_time=request.form['end_time'],
            mileage=request.form['mileage'],
            incident='incident' in request.form,
            notes=request.form['notes'],
            checker_signature=request.form['checker_signature']
        )
        db.session.add(report)
        db.session.commit()
        return redirect('/')
    reports = DailyReport.query.order_by(DailyReport.created_at.desc()).all()
    return render_template('index.html', reports=reports)

if __name__ == '__main__':
    app.run(debug=True)
