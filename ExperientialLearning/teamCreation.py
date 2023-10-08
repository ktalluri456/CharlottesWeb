from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///team.db'
db = SQLAlchemy(app)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    hometown = db.Column(db.String(120), nullable=False)
    personal_id = db.Column(db.String(120), unique=True, nullable=False)
    leadership_rating = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        hometown = request.form['hometown']
        personal_id = request.form['personal_id']
        leadership_rating = int(request.form['leadership_rating'])
        
        new_member = TeamMember(name=name, hometown=hometown, personal_id=personal_id, leadership_rating=leadership_rating)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():  # <-- This ensures the app context is present
        db.create_all()
    app.run(debug=True)