"""
The ``mlflow`` module provides a high-level "fluent" API for starting and managing MLflow runs.
For example:

.. code:: python

    import mlflow
    mlflow.start_run()
    mlflow.log_param("my", "param")
    mlflow.log_metric("score", 100)
    mlflow.end_run()

You can also use syntax like this:

.. code:: python

    with mlflow.start_run() as run:
        ...

which automatically terminates the run at the end of the block.

The fluent tracking API is not currently threadsafe. Any concurrent callers to the tracking API must
implement mutual exclusion manually.

For a lower level API, see the :py:mod:`mlflow.tracking` module.
"""
import sys

from kiwi.version import VERSION as __version__
from kiwi.utils.logging_utils import _configure_mlflow_loggers
import kiwi.tracking._model_registry.fluent
import kiwi.tracking.fluent

# Filter annoying Cython warnings that serve no good purpose, and so before
# importing other modules.
# See: https://github.com/numpy/numpy/pull/432/commits/170ed4e33d6196d7
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")  # noqa: E402
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")  # noqa: E402
# log a deprecated warning only once per function per module
warnings.filterwarnings("module", category=DeprecationWarning)

# pylint: disable=wrong-import-position
import kiwi.projects as projects  # noqa
import kiwi.tracking as tracking  # noqa

_configure_mlflow_loggers(root_module_name=__name__)

if sys.version_info.major == 2:
    warnings.warn("MLflow support for Python 2 is deprecated and will be dropped in a future "
                  "release. At that point, existing Python 2 workflows that use MLflow will "
                  "continue to work without modification, but Python 2 users will no longer "
                  "get access to the latest MLflow features and bugfixes. We recommend that "
                  "you upgrade to Python 3 - see https://docs.python.org/3/howto/pyporting.html "
                  "for a migration guide.", DeprecationWarning)

ActiveRun = kiwi.tracking.fluent.ActiveRun
log_param = kiwi.tracking.fluent.log_param
log_metric = kiwi.tracking.fluent.log_metric
set_tag = kiwi.tracking.fluent.set_tag
delete_tag = kiwi.tracking.fluent.delete_tag
log_artifacts = kiwi.tracking.fluent.log_artifacts
log_artifact = kiwi.tracking.fluent.log_artifact
active_run = kiwi.tracking.fluent.active_run
get_run = kiwi.tracking.fluent.get_run
start_run = kiwi.tracking.fluent.start_run
end_run = kiwi.tracking.fluent.end_run
register_training_dataset = kiwi.tracking.fluent.register_training_dataset
register_dev_dataset = kiwi.tracking.fluent.register_dev_dataset
register_test_dataset = kiwi.tracking.fluent.register_test_dataset
search_runs = kiwi.tracking.fluent.search_runs
get_artifact_uri = kiwi.tracking.fluent.get_artifact_uri
set_tracking_uri = tracking.set_tracking_uri
set_registry_uri = tracking.set_registry_uri
get_experiment = kiwi.tracking.fluent.get_experiment
get_experiment_by_name = kiwi.tracking.fluent.get_experiment_by_name
get_tracking_uri = tracking.get_tracking_uri
get_registry_uri = tracking.get_registry_uri
create_experiment = kiwi.tracking.fluent.create_experiment
set_experiment = kiwi.tracking.fluent.set_experiment
set_experiment_tag = kiwi.tracking.fluent.set_experiment_tag
start_experiment = kiwi.tracking.fluent.start_experiment
log_params = kiwi.tracking.fluent.log_params
log_metrics = kiwi.tracking.fluent.log_metrics
set_tags = kiwi.tracking.fluent.set_tags
delete_experiment = kiwi.tracking.fluent.delete_experiment
delete_run = kiwi.tracking.fluent.delete_run
register_model = kiwi.tracking._model_registry.fluent.register_model


run = projects.run

__all__ = ["ActiveRun", "log_param", "log_params", "log_metric", "log_metrics", "set_tag",
           "set_tags", "delete_tag", "log_artifacts", "log_artifact", "active_run", "start_run",
           "end_run", "search_runs", "get_artifact_uri", "get_tracking_uri", "set_tracking_uri",
           "get_experiment", "get_experiment_by_name", "create_experiment", "set_experiment",
           "delete_experiment", "get_run", "delete_run", "run", "register_model", "start_experiment",
           "get_registry_uri", "set_registry_uri"]
