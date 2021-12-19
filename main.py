import argparse
import schedule
from time import sleep
from datetime import datetime
from lib.Detector import Detector
from lib.messaging import send_sms


def heartbeat():
    print(f'{datetime.now().strftime("%Y.%m.%d %H:%M:%S")} Good working :)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Watch for website changes')
    parser.add_argument('--target', required=True, dest='target', help='URL of the webpage to observe')
    parser.add_argument('--interval', required=True, dest='interval', help='Polling interval', type=float)
    parser.add_argument('--recipient', required=True, dest='recipient',
                        help='SMS phone number to receive notifications')

    args = parser.parse_args()

    target = args.target
    interval = args.interval
    recipient = args.recipient

    detector = Detector(target, lambda: send_sms(recipient, '변화 감지됨.'))

    heartbeat()

    schedule.every(1).hours.do(heartbeat)
    schedule.every(interval).seconds.do(detector.tick)

    while True:
        schedule.run_pending()
        sleep(0.01)
