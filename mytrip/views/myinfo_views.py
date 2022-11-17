from flask import Blueprint, render_template, request, url_for, g

from werkzeug.utils import redirect

from mytrip import db
from mytrip.models import Survey, User, SurveyResult

from ..views.recommend_algorithm.tour_recommend import get_data_from_csv

bp = Blueprint('myinfo', __name__, url_prefix='/myinfo')


@bp.route('/all')
def myinfo():
    #question_list=Question.query.order_by(Question.create_date.desc())
    #question = Question.query.get_or_404(question_id)
    region_name = {
        '괴산군': 'goesan',
        '단양군': 'danyang',
        '보은군': 'boeun',
        '영동군': 'yeongdong',
        '옥천군': 'okcheon',
        '음성군': 'eumseong',
        '제천시': 'jecheon',
        '진천군': 'jincheon',
        '증평군': 'jeungpyeong',
        '청주시': 'cheongju',
        '충주시': 'chungju'
    }
    return render_template('myinfo/myinfo.html',region_name=region_name)

@bp.route('/schedule/<int:survey_id>/',methods=('GET',))
def schedule(survey_id):
    survey=Survey.query.get_or_404(survey_id)
    data_restaurant,data_trip=get_data_from_csv()

    result=SurveyResult.query.filter_by(survey_id=survey.id).first()
    tour_data = data_trip.loc[result.tour]
    tour = {
        'name': tour_data['name'],
        'cate': tour_data['sort'],
        'region': tour_data['si_2']
    }
    lunch_data = data_restaurant.loc[result.lunch]
    lunch = {
        'name': lunch_data['name'],
        'cate': lunch_data['naver_store_type'],
        'star': lunch_data['naver_star_point'],
        'qty': format(int(lunch_data['naver_visitor_review_qty']), ","),
        'lat':lunch_data['lon'],
        'lng':lunch_data['lat']
    }
    dinner_data = data_restaurant.loc[result.dinner]
    dinner = {
        'name': dinner_data['name'],
        'cate': dinner_data['naver_store_type'],
        'star': dinner_data['naver_star_point'],
        'qty': format(int(dinner_data['naver_visitor_review_qty']), ","),
        'lat': dinner_data['lon'],
        'lng': dinner_data['lat']
    }
    cafe_data = data_restaurant.loc[result.cafe]
    cafe = {
        'name': cafe_data['name'],
        'cate': cafe_data['naver_store_type'],
        'star': cafe_data['naver_star_point'],
        'qty': format(int(cafe_data['naver_visitor_review_qty']), ","),
        'lat': cafe_data['lon'],
        'lng': cafe_data['lat']
    }

    return render_template('myinfo/myinfo_schedule.html', survey=survey, tour=tour, lunch=lunch, dinner=dinner, cafe=cafe)


#마이 페이지는 survey db 이용해서 나타내기
#일정 클릭시 survey_id 넘겨줘서 결과 출력하기