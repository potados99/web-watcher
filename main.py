import json
import schedule
from time import sleep
from datetime import datetime
from argparse import ArgumentParser
from lib.Detector import Detector
from lib.SlackBot import SlackBot


def heartbeat():
    print(f'{datetime.now().strftime("%Y.%m.%d %H:%M:%S")} Good working :)')


def format_message(before_change: str, after_change: str) -> str:
    """
    App specific(Melon ticket) formatter.

    :param before_change:
    :param after_change:
    :return:
    """

    before = list(map(lambda x: (x['perfDay'], x['perfTimelist'][0]['seatGradelist'][0]['realSeatCntlk']),
                      json.loads(before_change)['data']['perfDaylist']))

    after = list(map(lambda x: (x['perfDay'], x['perfTimelist'][0]['seatGradelist'][0]['realSeatCntlk']),
                     json.loads(after_change)['data']['perfDaylist']))

    changes = []

    for i in range(len(before)):
        seats_before = before[i][1]
        seats_after = after[i][1]

        if seats_before != seats_after:
            changes.append(after[i])

    if len(changes) == 0:
        return 'realSeatCntlk 이외 변화 발생.'

    return '\n'.join(map(lambda x: f'{x[0]}일 공연 {x[1]}석 남음.', changes)) + '\n링크는 <https://m.ticket.melon.com/public/index.html#performance.index?prodId=206425|여기>.'


if __name__ == '__main__':
    parser = ArgumentParser(description='Watch for website changes')
    parser.add_argument('--target', required=True, dest='target', help='URL of the webpage to observe')
    parser.add_argument('--interval', required=True, dest='interval', help='Polling interval', type=float)
    parser.add_argument('--slack-webhook-url', required=True, dest='webhook_url',
                        help='Slack webhook URL where notification will be sent.')

    args = parser.parse_args()

    target = args.target
    interval = args.interval
    webhook_url = args.webhook_url

    slack_bot = SlackBot(webhook_url)
    detector = Detector(target, lambda prev, now: slack_bot.send(format_message(prev, now)))

    heartbeat()
    slack_bot.send('Watcher 기동!')

    schedule.every(1).hours.do(heartbeat)
    schedule.every(interval).seconds.do(detector.tick)

    while True:
        schedule.run_pending()
        sleep(0.01)
