from flask import Blueprint, render_template, request, url_for

from werkzeug.utils import redirect

#main은 별칭, __name__은 파일 이름이 인수로 전달, URL앞에 기본으로 붙일 접두어
#만약 url_prefix가 /main이라면 hello_pybo 호출하는 url은 localhost:5000/main/

#2-05
#url_for 함수는 라우팅 함수명으로 URL을 역으로 찾는 함수
#question._list에 해당하는 URL로 리다이렉트 하도록함


bp=Blueprint('main',__name__,url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/region')
def region_info():
    return render_template('region/region_info.html')