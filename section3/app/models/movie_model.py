from app import db

class Movie(db.Model):
    __tablename__ = 'movie'

    movieCd_id          =    db.Column(db.Integer(), primary_key= True)
    movieNm     =    db.Column(db.String(128), nullable=False)
    movieCd     =    db.Column(db.Integer(), db.ForeignKey('theather.movieCd'))
    date        =    db.Column(db.DateTime)
    audiCnt     =    db.Column(db.Integer(), nullable=False)

    
    
   
    def __repr__(self):
        return f"movie {self.movieCd}"
