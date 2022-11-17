from mytrip import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Survey(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user=db.relationship('User', backref=db.backref('survey_set'))
    gender=db.Column(db.String(10),nullable=True)
    age=db.Column(db.String(10),nullable=True)
    member=db.Column(db.String(10),nullable=True)
    region=db.Column(db.String(10),nullable=True)
    tour_keyword=db.Column(db.String(200),nullable=True)
    food_cate=db.Column(db.String(200),nullable=True)
    food_keyword=db.Column(db.String(200),nullable=True)
    survey_date=db.Column(db.DateTime(), nullable=False)

class SurveyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id=db.Column(db.Integer, db.ForeignKey('survey.id', ondelete='CASCADE'))
    survey = db.relationship('Survey', backref=db.backref('surveyResult_set'))
    region=db.Column(db.Integer, nullable=False)
    lunch=db.Column(db.Integer,nullable=True)
    tour=db.Column(db.Integer,nullable=True)
    cafe=db.Column(db.Integer,nullable=True)
    dinner=db.Column(db.Integer,nullable=True)


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)