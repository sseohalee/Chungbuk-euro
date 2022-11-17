import pandas as pd
import numpy as np

from openpyxl import load_workbook
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from flask import Blueprint, render_template, request, url_for

#CSV로딩
def get_data_from_csv():
    data_restaurant = pd.read_csv("/home/ubuntu/projects/trip/mytrip/static/data/fin.csv", encoding='cp949', thousands = ',', index_col=0)
    data_trip = pd.read_csv("/home/ubuntu/projects/trip/mytrip/static/data/trip.csv", encoding='cp949', index_col=0)

    return data_restaurant, data_trip

#토크나이저 실행 / 코사인 유사도 분류
def data_analyzing_sklearn(data, index_name):
    count_vect = CountVectorizer(min_df=2, ngram_range=(1, 2))
    count_fit = count_vect.fit_transform(data[index_name].astype('U'))
    count_cosine = cosine_similarity(count_fit, count_fit)
    count_cosine_ordering = count_cosine.argsort()[:, ::-1]

    return count_cosine, count_cosine_ordering

#최종 점수 출력
def data_score_trip(cosine, data):
    #Score 종합계산
    restaurant_score = (
            + cosine * 0.3
    )

    sorted_ind = restaurant_score.argsort()[:, ::-1]

    return sorted_ind, data

#추천 결과 출력
def find_best_location(df, sorted_ind, top_n=3):
    place_title = df
    place_index = place_title.index.values

    similar_indexes = sorted_ind[0, :(top_n)]
    similar_indexes = similar_indexes.reshape(-1)
    return df.iloc[similar_indexes]


def tour(region, tour_keyword):
    tour_keyword_list=tour_keyword.split('|')
    
    # 데이터 로딩
    data_restaurant, data_trip = get_data_from_csv()
    if region!='랜덤':
        data_trip = data_trip[(data_trip['si_2'] == region)]
    # 입력값 시(동) 이름 / 음식 종류 입력값으로.
    data_trip=data_trip[data_trip['sort'].isin(tour_keyword_list)]
    print(data_trip)
    if len(data_trip)==0:
        data_restaurant, data_trip = get_data_from_csv()
        data_trip = data_trip[(data_trip['si_2'] == region)]
    if len(data_trip)>2:
        cosine_cate, cosine_cate_sorted = data_analyzing_sklearn(data_trip, 'sort')
        data_trip_score, data_trip = data_score_trip(cosine_cate_sorted, data_trip)
        best_location=find_best_location(data_trip, data_trip_score, 5)
        print(best_location)
    else:
        best_location=data_trip
    #넘길 때 관광지 인덱스랑 위치(동) 보내기
    return best_location.index[0], best_location.iloc[0]['si'], best_location.iloc[0]['dong']

"""
53번 라인
data_trip = data_trip[(data_trip['si']=='괴산군')]
data_trip = data_trip[data_trip['sort']=='자연명소']

이런식으로 코드 넣어보면서 테스트
1. 저거는 오류 -> 괴산군에 sort가 자연명소인 데이터가 없어서
2. 해결방법: trip.csv 수정 (설문조사에 사용한 키워드(액티비티, 휴양 등등)로 바꾸기)
3. 데이터 없을 때 해결할 코드 넣기

"""


