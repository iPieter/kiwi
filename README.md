

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

Here is a minimal example without a training loop
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

### <a name="snapshots"></a> Reproducible snapshots

# Credits
- Kiwi bird by Georgiana Ionescu from the Noun Project
- Source code forked from [MLflow](https://mlflow.org)