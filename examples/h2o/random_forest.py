import h2o
from h2o.estimators.random_forest import H2ORandomForestEstimator

import kiwi
import kiwi.h2o

h2o.init()

wine = h2o.import_file(path="wine-quality.csv")
r = wine['quality'].runif()
train = wine[r < 0.7]
test = wine[0.3 <= r]


def train_random_forest(ntrees):
    with kiwi.start_run():
        rf = H2ORandomForestEstimator(ntrees=ntrees)
        train_cols = [n for n in wine.col_names if n != "quality"]
        rf.train(train_cols, "quality", training_frame=train, validation_frame=test)

        kiwi.log_param("ntrees", ntrees)

        kiwi.log_metric("rmse", rf.rmse())
        kiwi.log_metric("r2", rf.r2())
        kiwi.log_metric("mae", rf.mae())

        kiwi.h2o.log_model(rf, "model")


if __name__ == "__main__":
    for ntrees in [10, 20, 50, 100, 200]:
        train_random_forest(ntrees)
