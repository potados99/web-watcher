# web-watcher

웹사이트 내용의 변화를 감지해 Slack으로 알려주는 스크립트입니다.

## 사용법

```bash
python3.7 main.py --target '{관찰할 url}' --interval {관찰 주기} --slack-webhook-url '{슬랙봇 웹훅 url}'
```