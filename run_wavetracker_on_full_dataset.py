from pathlib import Path
from wavetracker.wavetracker import wavetracker


VERBOSITY = 3
RENEW = True
NOSAVE = False
CONFIG = None


def main():
    # Root of dataset
    data = Path("/home/efish/sidsel/raw/")
    
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

            print(f"Processing {logger.name} for dataset {path.name}")
            wavetracker(
                path = logger,
                renew= RENEW,
                nosave = NOSAVE,
                verbose = VERBOSITY,
            )

    


if __name__ == "__main__":
    main()