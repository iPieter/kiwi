"""
Small script used to generate mock data to test the UI.
"""

import argparse
import kiwi
import itertools
import random
import string
from random import random as rand

from kiwi.tracking import MlflowClient


def log_metrics(metrics):
    for k, values in metrics.items():
        for v in values:
            kiwi.log_metric(k, v)


def log_params(parameters):
    for k, v in parameters.items():
        kiwi.log_param(k, v)


def rand_str(max_len=40):
    return "".join(random.sample(string.ascii_letters, random.randint(1, max_len)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--large", help="If true, will also generate larger datasets for testing UI performance.",
        action="store_true")
    args = parser.parse_args()
    client = MlflowClient()
    # Simple run
    for l1, alpha in itertools.product([0, 0.25, 0.5, 0.75, 1], [0, 0.5, 1]):
        with kiwi.start_run(run_name='ipython'):
            parameters = {
                'l1': str(l1),
                'alpha': str(alpha),
            }
            metrics = {
                'MAE': [rand()],
                'R2': [rand()],
                'RMSE': [rand()],
            }
            log_params(parameters)
            log_metrics(metrics)

    # Runs with multiple values for a single metric so that we can QA the time-series metric
    # plot
    for i in range(3):
        with kiwi.start_run():
            for j in range(10):
                sign = random.choice([-1, 1])
                kiwi.log_metric("myReallyLongTimeSeriesMetricName-abcdefghijklmnopqrstuvwxyz",
                                random.random() * sign)
                kiwi.log_metric("Another Timeseries Metric", rand() * sign)
                kiwi.log_metric("Yet Another Timeseries Metric", rand() * sign)
            if i == 0:
                kiwi.log_metric("Special Timeseries Metric", rand() * sign)
            kiwi.log_metric("Bar chart metric", rand())

    # Big parameter values
    with kiwi.start_run(run_name='ipython'):
        parameters = {
            'this is a pretty long parameter name': 'NA10921-test_file_2018-08-10.txt',
        }
        metrics = {
            'grower': [i ** 1.2 for i in range(10)]
        }
        log_params(parameters)
        log_metrics(metrics)

    # Nested runs.
    with kiwi.start_run(run_name='multirun.py'):
        l1 = 0.5
        alpha = 0.5
        parameters = {
            'l1': str(l1),
            'alpha': str(alpha),
        }
        metrics = {
            'MAE': [rand()],
            'R2': [rand()],
            'RMSE': [rand()],
        }
        log_params(parameters)
        log_metrics(metrics)

        with kiwi.start_run(run_name='child_params.py', nested=True):
            parameters = {
                'lot': str(rand()),
                'of': str(rand()),
                'parameters': str(rand()),
                'in': str(rand()),
                'this': str(rand()),
                'experiement': str(rand()),
                'run': str(rand()),
                'because': str(rand()),
                'we': str(rand()),
                'need': str(rand()),
                'to': str(rand()),
                'check': str(rand()),
                'how': str(rand()),
                'it': str(rand()),
                'handles': str(rand()),
            }
            log_params(parameters)
            kiwi.log_metric('test_metric', 1)

        with kiwi.start_run(run_name='child_metrics.py', nested=True):
            metrics = {
                'lot': [rand()],
                'of': [rand()],
                'parameters': [rand()],
                'in': [rand()],
                'this': [rand()],
                'experiement': [rand()],
                'run': [rand()],
                'because': [rand()],
                'we': [rand()],
                'need': [rand()],
                'to': [rand()],
                'check': [rand()],
                'how': [rand()],
                'it': [rand()],
                'handles': [rand()],
            }
            log_metrics(metrics)

        with kiwi.start_run(run_name='sort_child.py', nested=True):
            kiwi.log_metric('test_metric', 1)
            kiwi.log_param('test_param', 1)

        with kiwi.start_run(run_name='sort_child.py', nested=True):
            kiwi.log_metric('test_metric', 2)
            kiwi.log_param('test_param', 2)

    # Grandchildren
    with kiwi.start_run(run_name='parent'):
        with kiwi.start_run(run_name='child', nested=True):
            with kiwi.start_run(run_name='grandchild', nested=True):
                pass

    # Loop
    loop_1_run_id = None
    loop_2_run_id = None
    with kiwi.start_run(run_name='loop-1') as run_1:
        with kiwi.start_run(run_name='loop-2', nested=True) as run_2:
            loop_1_run_id = run_1.info.run_id
            loop_2_run_id = run_2.info.run_id
    client.set_tag(loop_1_run_id, 'mlflow.parentRunId', loop_2_run_id)

    # Lot's of children
    with kiwi.start_run(run_name='parent-with-lots-of-children'):
        for i in range(100):
            with kiwi.start_run(run_name='child-{}'.format(i), nested=True):
                pass
    kiwi.set_experiment("my-empty-experiment")
    kiwi.set_experiment("runs-but-no-metrics-params")
    for i in range(100):
        with kiwi.start_run(run_name="empty-run-{}".format(i)):
            pass
    if args.large:
        kiwi.set_experiment("med-size-experiment")
        # Experiment with a mix of nested runs & non-nested runs
        for i in range(3):
            with kiwi.start_run(run_name='parent-with-children-{}'.format(i)):
                params = {rand_str(): rand_str() for _ in range(5)}
                metrics = {rand_str(): [rand()] for _ in range(5)}
                log_params(params)
                log_metrics(metrics)
                for j in range(10):
                    with kiwi.start_run(run_name='child-{}'.format(j), nested=True):
                        params = {rand_str(): rand_str() for _ in range(30)}
                        metrics = {rand_str(): [rand()] for idx in range(30)}
                        log_params(params)
                        log_metrics(metrics)
            for j in range(10):
                with kiwi.start_run(run_name='unnested-{}-{}'.format(i, j)):
                    params = {rand_str(): rand_str() for _ in range(5)}
                    metrics = {rand_str(): [rand()] for _ in range(5)}
        kiwi.set_experiment("hitting-metric-param-limits")
        for i in range(50):
            with kiwi.start_run(run_name="big-run-{}".format(i)):
                params = {str(j) + "a" * 250: "b" * 1000 for j in range(100)}
                metrics = {str(j) + "a" * 250: [rand()] for j in range(100)}
                log_metrics(metrics)
                log_params(params)
