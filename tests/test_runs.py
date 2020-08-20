from click.testing import CliRunner
from kiwi.runs import list_run
import kiwi


def test_list_run():
    with kiwi.start_run(run_name='apple'):
        pass
    result = CliRunner().invoke(list_run, ["--experiment-id", "0"])
    assert 'apple' in result.output


def test_list_run_experiment_id_required():
    result = CliRunner().invoke(list_run, [])
    assert "Missing option '--experiment-id'" in result.output
