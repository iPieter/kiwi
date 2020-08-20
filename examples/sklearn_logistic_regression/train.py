import numpy as np
from sklearn.linear_model import LogisticRegression

import kiwi
import kiwi.sklearn

if __name__ == "__main__":
    X = np.array([-2, -1, 0, 1, 2, 1]).reshape(-1, 1)
    y = np.array([0, 0, 1, 1, 1, 0])
    lr = LogisticRegression()
    lr.fit(X, y)
    score = lr.score(X, y)
    print("Score: %s" % score)
    kiwi.log_metric("score", score)
    kiwi.sklearn.log_model(lr, "model")
    print("Model saved in run %s" % kiwi.active_run().info.run_uuid)
