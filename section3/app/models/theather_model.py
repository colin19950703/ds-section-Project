from app import db

class Theather(db.Model):
    __tablename__ = 'theather'
    # id          = db.Column(db.Integer(), primary_key= True)
    # rank        = db.Column(db.Integer(), nullable=False)
    # movieNm     = db.Column(db.String(128), nullable=False)
    # movieCd     = db.Column(db.Integer(), nullable=False)
    # openDt      = db.Column(db.DateTime)

    rank        = db.Column(db.Integer(), primary_key= True, nullable=False)
    movieNm     = db.Column(db.String(128), nullable=False)
    movieCd     = db.Column(db.Integer(), nullable=False)
    openDt      = db.Column(db.DateTime)

    rl    = db.relationship('Movie', backref='theather', cascade="all,delete")
    
    def __repr__(self):
        return f"theather {self.movieCd}"

#####openDt=     db.Column(db.DateTime)