from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g

from werkzeug.utils import redirect

from mytrip import db
from mytrip.models import Survey, User, SurveyResult, Board
from mytrip.forms import BoardForm


bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/board')
def board_list():
    board_list=Board.query.order_by(Board.create_date.desc())
    return render_template('board/board_list.html',board_list=board_list)

@bp.route('/board/detail/<int:board_id>/')
def detail(board_id):
    board=Board.query.get_or_404(board_id)
    return render_template('board/board_detail.html',board=board)

@bp.route('/board/create/', methods=('GET', 'POST'))
def create():
    form = BoardForm()
    if request.method == 'POST' and form.validate_on_submit():
        board = Board(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('board.board_list'))
    return render_template('board/board_form.html', form=form)