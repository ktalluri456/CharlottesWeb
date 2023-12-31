from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///team.db'
db = SQLAlchemy(app)

# create a class for Team Member that takes in a database model as a parameter for localized instance. 
class TeamMember(db.Model):

    # Each of the columns in the database are defined here.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    hometown = db.Column(db.String(120), nullable=False)
    personal_id = db.Column(db.String(120), unique=True, nullable=False)
    leadership_rating = db.Column(db.Integer, nullable=False)

# Define flask function to render home page where all the questions will be asked. 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        hometown = request.form['hometown']
        personal_id = request.form['personal_id']
        leadership_rating = int(request.form['leadership_rating']) # Use the request API to post the values that are entered to the database

        new_member = TeamMember(name=name, hometown=hometown, personal_id=personal_id, leadership_rating=leadership_rating)
        db.session.add(new_member)
        db.session.commit()

        return redirect(url_for('thank_you', personal_id=personal_id))   #After the database session is formed, it will call the thank you method and render the thank you page.
    return render_template('index.html')

@app.route('/thanks/<personal_id>')
def thank_you(personal_id):
    current_member = TeamMember.query.filter_by(personal_id=personal_id).first() # SQL code that will filter out for what we need
    if not current_member:
        return "Member not found", 404

    potential_matches = TeamMember.query.filter(
        TeamMember.id != current_member.id
    ).order_by(
        db.func.abs(TeamMember.leadership_rating - current_member.leadership_rating).desc()
    ).limit(5).all()

    return render_template('thank_you.html', current_member=current_member, matches=potential_matches)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)