from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'steps.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class StepRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        steps = request.form.get('steps')
        date = request.form.get('date')
        if steps and date:
            try:
                new_record = StepRecord(steps=int(steps), date=date)
                db.session.add(new_record)
                db.session.commit()
            except:
                pass
        return redirect(url_for('index'))
    
    records = StepRecord.query.order_by(StepRecord.date.desc()).all()
    total = db.session.query(db.func.sum(StepRecord.steps)).scalar() or 0
    return render_template('index.html', records=records, total_steps=total)

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    record = StepRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)