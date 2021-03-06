

# Kiwi
Towards Fully Versioned Machine Learning. An opinionated fork from [MLflow](https://mlflow.org) for reproducible experiments.

![Python](https://img.shields.io/badge/python-v3.7-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
![Licence](https://img.shields.io/badge/licence-Apache--2.0-green)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)


## Key features
- [Data versioning »](#data-versioning)
- [Hyperparameter tuning and reporting »](#hyperparam)
- [Reproducible snapshots »](#snapshots)


## How to use

### Install
Since we are in alpha and in peer review, we have not published Kiwi. 
You can install Kiwi from our Github repository. 

```shell script
pip install git+git@github.com:iPieter/kiwi.git
```

### <a name="data-versioning"></a> Data versioning
You can register your datasets with Kiwi. 
We support Pytorch dataloaders and virtually all dataset arrays (as long as they are hashable and have implemented `len()`).
In addition, you can also register the file itself for more metadata (disk size + location).

The following code registers the training dataset:
```python
import kiwi
kiwi.register_training_dataset(
    dataloader=train_loader,
    dataset_location="/path/to/test.txt",
    experiment_id=current_experiment_id)
```

Normally, you register all three data splits (or use random splits).
```python
import kiwi
kiwi.register_training_dataset(...)
kiwi.register_dev_dataset(...)
kiwi.register_test_dataset(...)
```

### <a name="hyperparam"></a> Hyperparameter tuning and logging
We provide hyperparameter search with random search (`"random"`) and Bayesian optimization (`"tpe"`).
You can add this as a wrapper over your training/eval loop as follows:

1. You define the search space as follows: 

    ```python
    space = {
        'learning_rate': ("range", [1e-6, 1e-4]),
        'weight_decay': ("range", [0, 0.1]),
        'batch_size': ("choice", [8, 16, 32, 48])
    }
    ```

2. Define an objective function over the training + evaluation loop.
    You have to return an evaluation metric (in this case accuracy) that can be **minimized**. 
    So if the metric, like accuracy, is higher-is-better, then you need to invert it. 

    ```python
    def objective(args):
        # start a run
        with kiwi.start_run(experiment_id=current_experiment_id):
           ...
           return 1-metrics['eval_acc']
    ```
3. Start the experiment with the previously declared objective function:
    ```python
    kiwi.start_experiment(current_experiment_id, hp_space=space, objective=objective, max_evals=30, mode="tpe")
    ```

### <a name="snapshots"></a> Reproducible snapshots

### Full example
Here is a minimal example without a training loop. 
We also have fully working examples in `examples/`, check out the following: 

- Pytorch on MNIST: [`examples/pytorch` »](examples/pytorch)

```python
import kiwi

# ... load datasets

# register datasets

kiwi.register_training_dataset(
    dataloader=train_dataset,
    dataset_location=data_args.train_data + ".sentences",
    experiment_id=current_experiment_id)
kiwi.register_test_dataset(
    dataloader=test_dataset,
    dataset_location=data_args.test_data + ".sentences",
    experiment_id=current_experiment_id)
kiwi.register_dev_dataset(
    dataloader=dev_dataset,
    dataset_location=data_args.dev_data + ".sentences",
    experiment_id=current_experiment_id)

# Create an experiment
current_experiment_id: int = kiwi.create_experiment(
    datetime.datetime.now().__str__() + " - " + model_args.model_name_or_path)


# Create an objective function
def objective(args):
    
    # start a run
    with kiwi.start_run(experiment_id=current_experiment_id):
        # replace training args and log them
        for key in args:
            vars(training_args)[key] = args[key]
        for key, value in vars(training_args).items():
            kiwi.log_param(key, value)
        
        # Training loop ...
    
        kiwi.log_artifacts(training_args.output_dir)

        return 1-metrics['eval_acc'] # minimize 1-acc with TPE


# define search space
space = {
        'learning_rate': ("range", [1e-6, 1e-4]),
        'weight_decay': ("range", [0, 0.1]),
        'gradient_accumulation_steps': ("choice", [1, 2, 3, 4])
    }

kiwi.start_experiment(current_experiment_id, hp_space=space, objective=objective, max_evals=30, mode="tpe")
```


# Credits
- Kiwi bird by Georgiana Ionescu from the Noun Project
- Source code forked from [MLflow](https://mlflow.org)