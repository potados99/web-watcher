import os
import time
import uuid
import hmac
import hashlib
import datetime
import requests


def unique_id():
    return str(uuid.uuid1().hex)


def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()


def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(api_key, api_secret):
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    signature = get_signature(api_secret, data)

    return {
      'Authorization': f'HMAC-SHA256 ApiKey={api_key}, Date={date}, salt={salt}, signature={signature}',
      'Content-Type': 'application/json; charset=utf-8'
    }


def send_sms(receiver: str, content: str):
    """
    LMS를 보냅니다! coolsms 서비스를 이용합니다.

    :param receiver: 받는 사람. 숫자만 포함합니다.
    :param content: 내용.
    :return:
    """
    api_key = os.environ['SMS_API_KEY']
    api_secret = os.environ['SMS_API_SECRET']

    payload = {
        'message': {
            'to': receiver,
            'from': '01029222661',
            'text': content
        }
    }

    response = requests.post(
        url='https://api.coolsms.co.kr/messages/v4/send',
        headers=get_headers(api_key, api_secret),
        json=payload
    )

    succeeded = "정상" in response.text

    if not succeeded:
        raise Exception(response.text)

    print('뿅 문자 전송 완료')
