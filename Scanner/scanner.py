import json
import requests
import pandas as pd

class Scanner:

    def __init__(self):
        self.urlbase = "https://api.binance.com/api/v3/"

    def GET(self, action: str, parametros:dict):
        try:
            response = requests.get(self.urlbase + action, params=parametros)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception('Error en la petición')
        except:
            print('Error')
            return {'error':''}

    async def Cambio(self):
        mercado = self.GET("ticker/24hr",{})
        mercados = pd.DataFrame(mercado)
        mercados = mercados[['symbol','lastPrice','priceChangePercent','volume','count']]
        mercados.columns = ['symbol', 'Precio', 'Cambio', 'Volumen','#Trades']
        mercados = mercados.astype({'Precio':'float','Cambio':'float','Volumen':'float'})
        mercados = mercados[mercados['symbol'].str.endswith("USDT")]
        mercados = mercados.sort_values(by='Cambio', ascending=False)
        mercados = mercados[mercados['Cambio']>3]

        print(mercados)

        merc_json = mercados.to_json(orient="split")
        merc_json = json.loads(merc_json)
        return json.dumps(merc_json)