from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

# db, migrate 객체는 create 함수 밖에서 생성
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)  # name 변수에는 모듈명이 담김
    # config 파일 작성 항목 읽기
    app.config.from_object(config)

    # ORM   -> 밖에 있는 객체 앱에 등록
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, survey_views,auth_views,myinfo_views, recommend_views, board_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(survey_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(myinfo_views.bp)
    app.register_blueprint(recommend_views.bp)
    app.register_blueprint(board_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app