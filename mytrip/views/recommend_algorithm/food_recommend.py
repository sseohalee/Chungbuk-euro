import pandas as pd
import numpy as np



from openpyxl import load_workbook
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#CSV로딩
def get_data_from_csv():
    data_restaurant = pd.read_csv("/home/ubuntu/projects/trip/mytrip/static/data/fin.csv", encoding='cp949', thousands=',', index_col=0)
    data_trip = pd.read_csv("/home/ubuntu/projects/trip/mytrip/static/data/trip.csv", encoding='cp949', index_col=0)

    return data_restaurant, data_trip

def data_arrange_restaurant(data_restaurant):
    data_restaurant

#최종 점수 출력
def data_score_restaurant(data_restaurant):

    #Score 종합계산
    data_restaurant = data_restaurant.replace(np.nan,'0')

    #콤마 없애기
    #data_restaurant['naver_visitor_review_qty'] = pd.to_numeric(data_restaurant['naver_visitor_review_qty']).astype('int')

    data_restaurant['naver_visitor_review_qty'] = pd.to_numeric(data_restaurant['naver_visitor_review_qty']).astype('int')
    data_restaurant['naver_blog_review_qty'] = pd.to_numeric(data_restaurant['naver_blog_review_qty']).astype('int')
    data_restaurant['naver_star_point'] = pd.to_numeric(data_restaurant['naver_star_point']).astype('int')

    #하기 각 * 0.005 의 강도를 조정한다.
    restaurant_score = (
           + np.repeat([data_restaurant['naver_visitor_review_qty'].values], len(data_restaurant['naver_visitor_review_qty']), axis=0) * 0.005
           + np.repeat([data_restaurant['naver_blog_review_qty'].values], len(data_restaurant['naver_blog_review_qty']), axis=0) * 0.005
           + np.repeat([data_restaurant['naver_star_point'].values], len(data_restaurant['naver_star_point']), axis=0) * 0.005
    )

    restaurant_sorted_ind = restaurant_score.argsort()[:, ::-1]

    return restaurant_sorted_ind, data_restaurant

#추천 결과 출력
def find_best_restaurant(df, sorted_ind, top_n=3):
    place_title = df
    place_index = place_title.index.values

    similar_indexes = sorted_ind[0, :(top_n)]
    similar_indexes = similar_indexes.reshape(-1)
    return df.iloc[similar_indexes]

def food(region, region_dong, cate):
    #데이터 로딩
    data_restaurant, data_trip = get_data_from_csv()

    #Data Check for Restaurant
    data_restaurant_total = data_restaurant

    #입력값 시(동) 이름 / 음식 종류 입력값으로.
    data_restaurant = data_restaurant[(data_restaurant['si']==region) | (data_restaurant['dong']==region_dong)]
    data_restaurant = data_restaurant[(data_restaurant['cate_1']==cate)|(data_restaurant['naver_store_type']==cate)]
    data_restaurant_score, data_restaurant = data_score_restaurant(data_restaurant)
    print('-----추천 장소 출력')
    print(data_restaurant)
    best_restaurant = find_best_restaurant(data_restaurant, data_restaurant_score, 5)
    print(best_restaurant)
    return best_restaurant.index[0], best_restaurant.index[1]

