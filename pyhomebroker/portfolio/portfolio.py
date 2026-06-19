from ..common import user_agent
import requests as rq
import pandas as pd

class Portfolio:

    _ASSET_TYPE_MAP = {
        '0': 'Acciones',
        '1': 'Titulos Publicos',
        '3': 'Obligaciones Negociables',
        '4': 'Moneda',
        '7': 'Cedears',
        '11': 'Efectivo',
    }
    _CURRENCY_MAP = {0: 'ARS', 1: 'USD'}

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
        result = response.json().get('Result')

        if not result:
            return pd.DataFrame()

        record = result if isinstance(result, dict) else (result[0] if result else None)
        if not record:
            return pd.DataFrame()

        positions = []
        for subtotal in record.get('Activos', []):
            asset_type = self._ASSET_TYPE_MAP.get(str(subtotal.get('TIPO', '')), str(subtotal.get('TIPO', '')))
            for item in subtotal.get('Subtotal', []):
                symbol = item.get('TICK') or item.get('NERE') or item.get('AMPL', '')
                if not symbol:
                    continue
                positions.append({
                    'symbol': str(symbol),
                    'description': item.get('AMPL', ''),
                    'quantity': float(item.get('CANT') or 0),
                    'price': float(item.get('PCIO') or 0),
                    'ammount': float(item.get('IMPO') or 0),
                    'currency': self._CURRENCY_MAP.get(item.get('MONE', 0), 'ARS'),
                    'asset_type': asset_type,
                    'clearing_code': item.get('ESPE', ''),
                })

        if not positions:
            return pd.DataFrame()

        return pd.DataFrame(positions).set_index('symbol')
