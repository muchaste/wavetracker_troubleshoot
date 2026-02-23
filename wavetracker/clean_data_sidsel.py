#!/usr/bin/env python3

import sys
import os

def main():
    # === INITIAL CHECKS TO ENSURE SCRIPT RUNS FLAWLESSLY ===

    # Check whether list of arguments given after calling the script is below 2
    if len(sys.argv) < 2:
        print("Usage: cleandatastructure /path/to/dataset")
        sys.exit(1)

    # Define dataset_path variable to the second argument given to the terminal
    dataset_path = sys.argv[1]

    # Check whether this dataset_path exists
    if not os.path.exists(dataset_path):

        # Print an error if it doesn't exist
        print(f"Error: path {dataset_path} does not exist")

        # In case it doesn't exist, exit run
        sys.exit(1)

    # === PROCEED WITH DETECTING & REMOVING EMPTY FILES ===

    print(f"Processing dataset in {dataset_path}")


    # Find empty files
    files = os.listdir(dataset_path)
    print(f"Number of files before deletion {len(files)}")

    for i, file in enumerate(files):
        full_path = os.path.join(dataset_path, file)

        # Process only .wav files
        if os.path.isfile(full_path) and file.endswith(".wav"):
            size = os.path.getsize(full_path)

            if size == 0:
                # Delete .wav file
                os.remove(full_path)

                # Build corresponding .dat file
                base_name = file[:-4]
                dat_file = f"{base_name}-blinks.dat"
                dat_path = os.path.join(dataset_path, dat_file)


                if os.path.exists(dat_path):
                    os.remove(dat_path)

    files_after = os.listdir(dataset_path)
    print(f"\nNumber of files after deletion {len(files_after)}")




if __name__ == "__main__":
    main()
