from pathlib import Path
from wavetracker.wavetracker import wavetracker


VERBOSITY = 3
RENEW = True
NOSAVE = False
CONFIG = None
RUN_ONLY_ON_LOGGERS = ["A", "C"]


def main():
    # Root of dataset
    # data = Path("/home/efish/sidsel/raw/")
    data = Path("/home/weygoldt/mount/raw/")

    # Get recording days
    datasets = sorted(data.iterdir())

    # Remove files and only keep directories
    filtered_datasets = []
    for path in datasets:
        if path.is_dir():
            filtered_datasets.append(path)

    # Go through recording days
    for path in filtered_datasets:
        # Go through individual loggers for each day
        logger_dirs = sorted(path.glob("recordings*"))
        for logger in logger_dirs:
            upper_chars = list(filter(str.isupper, logger.name))

            assert (
                len(upper_chars) == 1
            ), f"Expected one upper char in logger name, got {upper_chars}"

            if upper_chars[0] not in RUN_ONLY_ON_LOGGERS:
                print(
                    f"Skipping {logger.name} because it is not in RUN_ONLY_ON_LOGGERS: {RUN_ONLY_ON_LOGGERS}"
                )
                continue

            print(
                f"Found {logger.name} in RUN_ONLY_ON_LOGGERS: {RUN_ONLY_ON_LOGGERS}, running wavetracker..."
            )
            print(f"Processing {logger.name} for dataset {path.name}")
            wavetracker(
                path=logger,
                renew=RENEW,
                nosave=NOSAVE,
                verbose=VERBOSITY,
            )
    exit()


if __name__ == "__main__":
    main()

