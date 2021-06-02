from flask import Blueprint, render_template, request
from app.utils import main_funcs

from app.models.theather_model import Theather
from app.models.movie_model import Movie
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    print("index")
    return render_template('index.html')

@bp.route('/theather')
def theather_index():
    """
    movie_list 에 유저들을 담아 템플렛 파일에 넘겨주세요
    """
    msg_code = request.args.get('msg_code', None)
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    movie_list = Theather.query.with_entities(Theather.rank, 
                                              Theather.movieNm,
                                              Theather.movieCd, 
                                              Theather.openDt )  
    
    if alert_msg == 4:
        return render_template('theather.html', alert_msg=alert_msg)

    return render_template('theather.html', alert_msg=alert_msg, movie_list = movie_list)



@bp.route('/predict')
def predict_index():
    
    movies=Theather.query.all()

    predict = request.args.get('predict', None)

    if predict:
        movieName = request.args.get('movieName', None)
        return render_template('predict_audi.html', movies=movies, predict=predict, movieName=movieName)
    #     # POST 일 경우에 필요한 코드를 작성해 주세요

    #     movieCd = request.form.get('movieCd') 
    #     #compare_text=request.form.get('compare_text')

    #     movies = Theather.query.filter(Theather.movieCd == movieCd).first()
    #     Movies = [movies]
    #     print("Movies :",Movies[0].movieNm)
    #     # Users=[user1,user2]

    #     # # utils main_funcs > predict_text 추출하여 predict_text 데이터 확보
    #     # predict_text = main_funcs.predict_text(Users, compare_text)

    #     # # compare_text, predict_text 구했으므로 각 해당하는 변수에 넣어주기 for문 X
    #     # prediction['result']=predict_text
    #     # prediction['compare_text']=compare_text
        
    #     return render_template('compare_user.html', movies=Movies, prediction=prediction),200

    return render_template('predict_audi.html', movies=movies)
