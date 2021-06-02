# import tweepy
import requests
import json

#API_KEY = '3c2998d12070779b4b322803d7c79986'
API_KEY = "f5eef3421c602c6cb7ea224104795888"
def get_theather_data(date):
    """
    get_theather_data 함수는 kofic 에서부터 가져온 데이터를 json 형태로
    리턴해야 합니다.

    파라미터:
        - date: 조회할 날짜를 담은 문자열(str) 입니다.

    리턴:
        - 파이썬 딕셔너리: 조회한 API JSON 데이터를 파이썬 딕셔너리 형태로
        리턴합니다.
    """
    API_URL= f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={API_KEY}&targetDt={date}"

    resp = requests.get(API_URL)
    theather_data = json.loads(resp.text)

    return theather_data

# def get_user(screen_name):
#     """
#     `get_user` 함수는 트위터의 `screen_name` 이 주어지면 tweepy 를 통해 해당
#     트위터 유저를 조회한 객체를 그대로 리턴합니다.
#     """
#     try : 
#         raw_user = api.get_user(screen_name)
#     except :
#         raw_user = None
#     return raw_user

# def get_tweets(screen_name):
#     """
#     `get_tweets` 함수는 트위터의 `screen_name` 이 주어지면 tweepy 를 통해 해당 트위터 유저의 트윗들을 조회한 리스트를 리턴합니다.
#      - 리턴되는 트윗에는 리트윗 (retweet) 을 포함하지 않습니다.
#      - 140 글자가 넘는 경우에도 다 가져올 수 있어야 합니다.
#      - 답변 트윗 (retweet) 들은 포함하지 않습니다.
#      - 한 페이지당 50 개의 트윗을 가져오도록 설정해야 합니다.

#     Hint:

#      - get_tweets 는 tweepy 의 user_timeline 함수를 사용합니다.
#      - 다음 파라미터들을 어떻게 사용하는지 찾아보세요.
#          - 'screeen_name'
#          - 'tweet_mode'
#          - 'include_rts'
#          - 'count'
#          - 'exclude_replies'
#     """

#     raw_tweets =  api.user_timeline(screen_name = screen_name, tweet_mode="extended", include_rts = False, count = 50, exclude_replies = True)
    
#     return raw_tweets

# a = weather_data(201309030600)
# ai =0
# ai +=1

