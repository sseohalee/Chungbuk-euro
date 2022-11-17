from datetime import datetime

from flask import Blueprint, render_template, request, url_for

from werkzeug.utils import redirect

from mytrip import db
from mytrip.models import Survey, User

bp = Blueprint('survey', __name__, url_prefix='/survey')

@bp.route('/survey/')
def survey_start():
    return render_template('survey/survey.html')
#url_for('survey.survey_start')

@bp.route('/survey/complete/')
def survey_complete():
    return render_template('survey/survey_complete.html')


@bp.route('/create/<int:user_id>/',methods=('POST',))
def create(user_id):
    # 받아온 정보 변수에 저장
    #content = request.form['content']
    gender=request.form['gender']
    age=request.form['age']
    member = request.form['member']
    region = request.form['region']
    tour_keyword_list = request.form.getlist('tour_keyword')
    tour_keyword='|'.join(tour_keyword_list)
    food = request.form['food']
    food_keyword = request.form['food_keyword']


    # 객체 만들어서 디비에 저장
    #survey = Survey(content=content, create_date=datetime.now())
    survey=Survey(user_id=user_id,gender=gender,age=age,member=member,region=region,tour_keyword=tour_keyword,food_cate=food, food_keyword=food_keyword, survey_date=datetime.now())
    db.session.add(survey)
    db.session.commit()
    print('데이터 저장 완료')
    return redirect(url_for('recommend.recommend', survey_id=survey.id))
