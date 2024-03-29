import pathlib

from sneks.engine.config.instantiation import config as sneks_config
from sneks.engine.engine import runner
from sneks.engine.validator import main as validator

import scripts.config as script_config
import submission

prefix = str(pathlib.Path(submission.__file__).resolve().parent)


def validate():
    validator.main(test_path=prefix)


def run():
    sneks_config.registrar_submission_sneks = 4
    sneks_config.runs = 1000000000000000
    sneks_config.turn_limit = 1000000000000
    sneks_config.registrar_prefix = prefix
    sneks_config.graphics.step_delay = script_config.STEP_DELAY_MILLISECONDS
    sneks_config.graphics.step_keypress_wait = (
        script_config.STEP_DELAY_WAIT_FOR_KEYPRESS
    )
    sneks_config.graphics.end_delay = script_config.END_DELAY_MILLISECONDS
    sneks_config.graphics.end_keypress_wait = script_config.END_DELAY_WAIT_FOR_KEYPRESS

    import cProfile
    import pstats
    pr = cProfile.Profile()
    pr.enable()

    runner.main()

    pr.disable()
    stats = pstats.Stats(pr)
    print(stats.sort_stats("tottime").print_stats(20))
