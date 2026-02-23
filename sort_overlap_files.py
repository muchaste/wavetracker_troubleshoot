from pathlib import Path
from IPython import embed
import subprocess
import shutil


def main():
    # Get paths to the datafiles we want to compare
    data_A = Path("/home/efish/sidsel/raw/2025-07-28_00-00/recordingsA")
    reference_data_A = Path("/home/efish/sidsel/raw/2025-07-23_00-00/recordingsA")

    data_B = Path("/home/efish/sidsel/raw/2025-07-28_00-00/recordingsB")
    reference_data_B = Path("/home/efish/sidsel/raw/2025-07-23_00-00/recordingsB")

    # Sort the datafiles
    keep_files_A, overlap_files_A = sort_files(data_A, reference_data_A)
    keep_files_B, overlap_files_B = sort_files(data_B, reference_data_B)

    # move the overlapping files into a designated direction
    move_files(overlap_files_A, Path("/home/efish/sidsel/raw/2025-07-28_00-00/recordingsA/overlap_files"))
    move_files(overlap_files_B, Path("/home/efish/sidsel/raw/2025-07-28_00-00/recordingsB/overlap_files"))


def sort_files(data, reference_data):
    """
    gets the .wav files of a given dataset and sorts it in comparison to a reference dataset
    Purpose: if 2 datasets merged into one and some data overwrote and some didnt and you want to remove the doubled, not overwritten data
    """
    # Get .wav files of the datasets
    data_files = sorted(data.glob("*.wav"))
    reference_files = sorted(reference_data.glob("*.wav"))

    # Get filenames of the .wav files
    reference_filenames = {f.name for f in reference_files} # Set for faster lookup

    overlap_files = []
    keep_files = []
    
    # Iterate through the files in data and compare them
    for i in range(len(data_files) - 1):
        file1 = data_files[i]
        file2 = data_files[i + 1]

        # get config name for comparison
        stem1 = config_filename(file1)
        stem2 = config_filename(file2)
        
        # Check if the file has been already sorted
        if file1.name not in keep_files and file1.name not in overlap_files:
            # If config name the same, check is one in reference and put it accordingly in lists
            if stem1 == stem2:
                if file1.name in reference_filenames:
                    overlap_files.append(file1.name)
                    keep_files.append(file2.name)
                elif file2.name in reference_filenames:
                    overlap_files.append(file2.name)
                    keep_files.append(file1.name)
                else: print("error")
            else: keep_files.append(file1.name)
        #embed()
        
    return keep_files, overlap_files

def config_filename(filepath):
    """
    Cuts the lat two digits before .wav
    Example: bigtankA-20190101T000012.wav -> bigtankA-20190101T0000
    """
    stem = filepath.stem  
    return stem[:-2]      # cut last 2 digits

def move_files(files, destination_direction):
    """
    moves files into the specified direction
    """

    destination_direction.mkdir(exist_ok=True)
    for file in files:
        subprocess.run([
            "mv",
            str(destination_direction.parent / file),
            str(destination_direction),
        ])        
                

if __name__ == "__main__":
    main()