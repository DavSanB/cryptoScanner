import json
import requests
import pandas as pd

class Scanner:

    def __init__(self):
        self.urlbase = "https://api.binance.com/api/v3/"
        self.weight = True

    def GET(self, action: str, parametros:dict):
        try:
            response = requests.get(self.urlbase + action, params=parametros)
            if response.status_code == 200:
                return response
            else:
                raise Exception('Error en la petición')
        except:
            print('Error')
            return {'error':''}

    async def Cambio(self, config):

        mercado = self.GET("ticker/24hr",{})

        if(int(mercado.headers['x-mbx-used-weight']) < 1000):
            self.weight = True

            mercados = pd.DataFrame(mercado.json())
            mercados = mercados[['symbol','lastPrice','priceChangePercent','volume','count']]
            mercados.columns = ['symbol', 'Precio', 'Cambio', 'Volumen','#Trades']
            mercados = mercados.astype({'Precio':'float','Cambio':'float','Volumen':'float'})
            mercados = mercados[mercados['symbol'].str.endswith("USDT")]

            mercados = mercados.sort_values(by=config['orden'], ascending=False)
            mercados = mercados.head(config['monedas'])

            merc_json = mercados.to_json(orient="split")
            merc_json = json.loads(merc_json)
            return json.dumps(merc_json)
        else:
            self.weight = False
            return {}