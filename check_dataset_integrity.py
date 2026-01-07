from pathlib import Path
from datetime import datetime
from IPython import embed
from thunderlab.dataloader import DataLoader

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
            wavfiles = sorted(logger.glob("*.wav"))

            first_file = wavfiles[0].stem.split("-")[-1]
            last_file = wavfiles[-1].stem.split("-")[-1]

            first_datetime = datetime.strptime(first_file, '%Y%m%dT%H%M%S')
            last_datetime = datetime.strptime(last_file, '%Y%m%dT%H%M%S')

            dt = last_datetime - first_datetime

            wavfiles = [str(x) for x in wavfiles]

            n_wavefiles = len(wavfiles)
            dset = DataLoader(wavfiles)
            n_loaded = len(dset.file_paths)



            print(f"Recording took {dt}, total files: {n_wavefiles}, loaded files: {n_loaded}")




            
    


if __name__ == "__main__":
    main()