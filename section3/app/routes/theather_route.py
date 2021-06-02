from flask import Blueprint, request, redirect, url_for, Response, render_template
from app.services import theather_api

from app.models.theather_model import Theather
from app.models.movie_model import Movie
from app import db
from datetime import datetime

bp = Blueprint('theather', __name__)


@bp.route('/theather', methods=['POST'])
def add_theather():
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()
    
    reps = request.form.get('date',None) 
    if not reps : 
       return  redirect(url_for('main.theather_index', msg_code=4))

    theather_info = theather_api.get_theather_data(reps)

    for index in range(0, len(theather_info["boxOfficeResult"]["dailyBoxOfficeList"])) :
      new_theather = Theather(
          rank    = theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["rank"],
          movieCd = theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["movieCd"],
          movieNm = theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["movieNm"],
          openDt  = datetime.strptime(theather_info["boxOfficeResult"]["dailyBoxOfficeList"][index]["openDt"], "%Y-%m-%d").date(),     
      )
      db.session.add(new_theather)
      db.session.commit() 

    return redirect(url_for('main.theather_index', msg_code=0))


@bp.route('/theather/delte_all')
def delete_theather(date=None):
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()
  
    # theather =Theather.query.filter(Theather.date == date).first()

    # if date is None:
    #   return Response(status=400)
    
    # if not theather:
    #   return Response(status=404)
    
    # db.session.delete(theather)
    # db.session.commit()
    return redirect(url_for('main.theather_index', msg_code=3))
