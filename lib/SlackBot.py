from requests import request


class SlackBot:
    def __init__(self, web_hook_url):
        self._web_hook_url = web_hook_url

    def send(self, text: str):
        print(f'Sending to Slack: {text}')

        return request(
            method='POST',
            url=self._web_hook_url,
            headers={'content-type': 'application/json'},
            json={'text': text}
        )
