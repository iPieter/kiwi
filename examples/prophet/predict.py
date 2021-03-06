import sys

import pandas as pd
from fbprophet import Prophet

import kiwi.pyfunc


model_uri = sys.argv[1]
model = kiwi.pyfunc.load_model(sys.argv[1])
print("Loaded model from URI: {}".format(model_uri))

data = {'periods':[5]}
df = pd.DataFrame(data)
out = model.predict(model_input=df)
print(out)
