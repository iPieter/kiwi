from kiwi.pyfunc import scoring_server
from kiwi import pyfunc
app = scoring_server.init(pyfunc.load_pyfunc("/opt/ml/model/"))
