from flask import Blueprint, request, redirect, url_for, Response, render_template
from app.services import theather_api

from app.models.theather_model import Theather
from app.models.movie_model import Movie
from app.utils import main_funcs
from app import db
from datetime import datetime
import datetime as dt
bp = Blueprint('predict', __name__)


@bp.route('/predict', methods=['POST'])
def add_movie():
    Movie.query.delete() ##Movie DB를 초기화
    db.session.commit()  

    movieCd = request.form.get('movieCd',None)  ##MovieCode를 form에서 얻어옴
    if not movieCd :                            ##MovieCode가 없으면 main화면으로 돌아감
        return redirect(url_for('main.index', msg_code=0))

    opendate = Theather.query.filter(Theather.movieCd== movieCd).with_entities(Theather.openDt).first() 
    movieName = Theather.query.filter(Theather.movieCd== movieCd).with_entities(Theather.movieNm).first()
    ##MovieCode가 일치하는 영화의 개봉일을 가져옴
    opendate = main_funcs.todatetime(opendate) #개봉일을 datetime으로 변환
    nowdate = datetime.now()                   #현재일을 datetime으로 얻어옴
    diffdate = int((nowdate - opendate).days)  #현재일과 개봉일의 차이를 구함.
    #doi = opendate #date of inquiry 첫 조회날짜를 개봉날짜로 설정
    stopflag = False

    while True : 
        if stopflag or (int((nowdate - opendate).days) == 0): break #flag가 False면 중지

        date_str = main_funcs.dttostr(opendate) #조회날짜를 문자열로 변환
        theather_info = theather_api.get_theather_data(date_str) #조회날짜의 개봉한 영화 정보를 불러옴 
        stopflag = True
        for index in range(0, len(theather_info["boxOfficeResult"]["dailyBoxOfficeList"])) :
            
            
            if movieCd == theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["movieCd"] :
                date = theather_info["boxOfficeResult"]["showRange"][0:8]
                date = dt.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]), 0, 0, 0).date()
                new_movie = Movie(movieCd = theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["movieCd"],
                                  movieNm = theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["movieNm"],
                                  date    = date,
                                  audiCnt = theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["audiCnt"])  
                
                print(theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["movieNm"],
                    theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["movieCd"],
                    date,
                    theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["audiCnt"])

                db.session.add(new_movie)
                db.session.commit()
                stopflag = False
        
        opendate += dt.timedelta(days=1)
    
    date = Movie.query.with_entities(Movie.date).all()
    audiCnt = Movie.query.with_entities(Movie.audiCnt).all()
    date_list = []
    audiCnt_list = []
    

    for a in date :
        date_list.append(a.date)
    for a in audiCnt :
        audiCnt_list.append(a[0])

    predict = main_funcs.predict_audiCnt(date_list,audiCnt_list)
    return redirect(url_for('main.predict_index', predict = predict, movieName=movieName[0])) 