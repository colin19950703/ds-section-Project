import re
import datetime as dt
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA


from app.models.movie_model import Movie

def msg_processor(msg_code):
    '''
    msg_processor returns a msg object with 'msg', 'type'
    where 'msg' corresponds to the message user sees
    and 'type' is the color of the alert element

    codes:
        - 0 : Successfully added to database
        - 1 : User does not exist
        - 2 : Unable to retrieve tweets
        - 3 : Successfully deleted user
    '''

    msg_code = int(msg_code)

    msg_list = [
        (
            '해당 날짜의 영화 정보를 성공적으로 불러왔습니다.',
            'success'
        ),
        (
            'User does not exist',
            'warning'
        ),
        (
            '예측 완료!',
            'warning'
        ),
        (
            '영화 정보를 성공적으로 삭제했습니다.',
            'success'
        ),
        (
            '날짜를 다시 입력하세요',
            'warning'
        )
    ]

    return {
        'msg':msg_list[msg_code][0],
        'type':msg_list[msg_code][1]
    }

def todatetime(datetime) :
    
    datetime = str(datetime) #sqlalchemy타입 데이터를 string으로 변경
    numbers = re.findall("\d+", datetime) #숫자만 추출해서 리스트에 저장. 
                                          #ex) (datetime.datetime(2021, 5, 19, 0, 0),)  => ['2021', '5', '19', '0', '0']

    date = dt.datetime(int(numbers[0]), int(numbers[1]), int(numbers[2]), int(numbers[3]), int(numbers[4]), 0) 

    return date

def dttostr(datetime) :
    
    datetime = str(datetime) #sqlalchemy타입 데이터를 string으로 변경
    numbers = re.findall("\d+",datetime)
    y = numbers[0]
    m = numbers[1]
    d = numbers[2]

    datetime = y+m+d

    return datetime

def predict_audiCnt(date, audiCnt):

    data = { 'date' : date, 'count' : audiCnt}
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df.date, format='%Y-%m-%d')
    df = df.set_index('date')

    order = (2, 1, 2)
    model = ARIMA(df, order, freq='D')
    fit = model.fit()

    preidctdate = str(date[-1])
    preidctdate = preidctdate[:11]
    preds = fit.predict(preidctdate, typ='levels')
    preds = preds.tolist()
    preds = round(preds[0])
    
    if preds < min(audiCnt) :
        return round(min(audiCnt)*0.8)
    else :
        return round(preds) 
