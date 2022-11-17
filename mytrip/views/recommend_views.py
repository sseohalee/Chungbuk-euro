from datetime import datetime
from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from mytrip import db
from mytrip.models import Survey, User, SurveyResult

from ..views.recommend_algorithm.tour_recommend import tour
from ..views.recommend_algorithm.food_recommend import food
from ..views.recommend_algorithm.cafe_recommend import cafe

result={}

bp = Blueprint('recommend', __name__, url_prefix='/recommend')

# survey_view에서 데이터 저장후 recommend_view의 함수 호출
@bp.route('/recommend/<int:survey_id>/',methods=('POST','GET'))
def recommend(survey_id):
    print('추천 함수 실행 완료')
    # 데이터 읽은 다음에
    survey=Survey.query.get_or_404(survey_id)
    print('데이터 읽기 완료')
    # 관광지 추천
    tour_index, tour_si, tour_dong=tour(survey.region, survey.tour_keyword)
    tour_index=int(tour_index)
    print('관광지 추천 완료')
    # 점심, 저녁 맛집 추천
    lunch, dinner=food(tour_si, tour_dong, survey.food_cate)
    lunch,dinner=int(lunch),int(dinner)
    # 커피 추천
    cafe_index = cafe(tour_si, tour_dong, survey.food_keyword)
    cafe_index=int(cafe_index)

    # 데이터 생성
    survey_result=SurveyResult(survey_id=survey_id,region=survey.region,lunch=lunch,tour=tour_index,cafe=cafe_index, dinner=dinner)
    db.session.add(survey_result)
    db.session.commit()
    return redirect(url_for('survey.survey_complete'))


# 추천 알고리즘 통과 후 디비 저장