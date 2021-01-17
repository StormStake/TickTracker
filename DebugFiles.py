
url = 'https://finnhub.io/api/v1/crypto/candle'

        urlparams = {
            'symbol':str(ticker),
            'resolution':self.resolution,
            'from':f'{1610854579-86400}',
            'to':f'{1610854579}',
            'token': 'bvtss4748v6pijnevmqg'
        }

def urlgener(url, params):



urlgener(url, params)