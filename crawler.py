import requests
import time
import hashlib
import random
import string
import pandas as pd

BASE_URL_API = "https://codeforces.com/api/"
API_KEY = "100038e9771660380b8e293d519822a86bff614c"
SECRET = "d90e45f9735b040e6a13261d96c72ed661841e10"

# Returns random string from ascii and digits 
def randomStr(length):
  return ''.join(random.choice(string.ascii_uppercase + string.digits)
                  for _ in range(length))

def callAPI(method, params):

  params['apiKey'] = API_KEY
  time_int = int(time.time()) # Get time in unix int format
  params['time'] = time_int 

  params = dict(sorted(params.items(), key=lambda kv:(kv[0], str(kv[1]))))

  rand_str = randomStr(6)
  hash_prefix = f"{rand_str}/{method}?"
  hash_params = '&'.join(f'{k}={str(v)}' for k,v in params.items())
  hash_suffix = f'#{SECRET}'
  hash = hashlib.sha512(f'{hash_prefix}{hash_params}{hash_suffix}'.encode()).hexdigest()
  
  url = f"{BASE_URL_API}{method}?{hash_params}&apiSig={rand_str}{hash}"
  r = requests.get(url)
  return r.json()

def getProblemsByHandler(handler, count=None):
    params = params={'handle':handler, 
                     'from':'1'}
    if count is not None:
      params['count'] = count
    return callAPI('user.status', params)['result']

def aggregateProblems(handler):
  problems = getProblemsByHandler(handler)

  df = pd.json_normalize(problems)
  if len(problems)>0:
    return df.loc[df['verdict']=='OK', ['problem.name','problem.index', 'problem.contestId']].groupby(['problem.contestId','problem.index','problem.name']).count().reset_index().astype({'problem.contestId': 'int32'}).values.tolist()
  else:
    return []
