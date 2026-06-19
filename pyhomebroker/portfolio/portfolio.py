from ..common import user_agent
import requests as rq

class Portfolio:

    def __init__(self, auth, proxy_url=None):
        self.__auth = auth
        self.__proxies = proxy_url

    def get_portfolio(self, account_id):
        url = '{}/Consultas/GetConsulta'.format(self.__auth.broker['page'])

        payload = {
            'comitente': str(account_id),
            'consolida': '0',
            'proceso': '22',
            'tipo': None
        }

        headers = {
            'User-Agent': user_agent,
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json; charset=UTF-8'
        }

        response = rq.post(url, json=payload, headers=headers, cookies=self.__auth.cookies, proxies=self.__proxies)
        response.raise_for_status()
        response = response.json()

        return response['Result']
