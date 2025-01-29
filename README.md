# Wavetracker

Algorithms used to analyze electrode-array recordings of wave-type
electric fish. This includes the detection of individual fish, the tracking of individuals over time,
and the post-processing to eliminate and correct tracking errors.

## `wavetracker`

Script to track signals of electric wavetype fish over time utilizing EOD
frequency (fundmalentals) and signal strength across electrodes (signatures) as
tracking features. 

Basic usage:
```sh
wavetracker /path/to/dataset
```

The pipeline includes:
1. converting the dataset into a spectrogram
2. detecting harmonic groups using the [`thunderfish`](https://github.com/bendalab/thunderfish) package
3. tracks fundamental frequencies of the harmonic groups corresponding to EODs of single fish

All data produces is stored in a single folder as `.npy` files.

## `cleanup`

Post-processing algorithms to discard false detections and fix tracking errors.

Basic usage:
```sh
cleanup /path/to/wavetracker/ouput/folder
```

## EODsorter

Graphical interface to manually check and fix tracking errors.

Basic usage:
```sh
EODsorter /path/to/wavetracker/ouput/folder
```

## Examples:

### Display tracked EOD frequency traces:**

```py
import matplotlib.pyplot as plt
import numpy as np

fund_v = np.load('fund_v.npy', allow_pickle=True) # fundamental frequencies
idx_v = np.load('idx_v.npy', allow_pickle=True) # indices on time arry
ident_v = np.load('ident_v.npy', allow_pickle=True) # fish identities
times = np.load('times.npy', allow_pickle=True) # time

ids  = np.unique(ident_v[~np.isnan(ident_v)]) # unique fish identities

fig, ax = plt.subplots()
for fish_id in ids:
  ax.plot(times[idx_v[ident_v == fish_id]], fund_v[ident_v == fish_id], marker='.')
ax.set_xlabel('time [s]')
ax.set_ylabel('frequency [Hz]')
plt.show()
```

### Load and display fine spectrogram
```py
import numpy as np
import matplotlib.pyplot as plt
from thunderlab.powerspectrum import decibel

# Load data
fine_freqs = np.load('fine_freqs.npy', allow_pickle=True)
fine_times = np.load('fine_times.npy', allow_pickle=True)
fine_spec_shape = np.load('fine_spec_shape.npy', allow_pickle=True)
fine_spec = np.memmap('fine_spec.npy', dtype='float', mode='r', 

# Set frequency and time limits
f0, f1 = 0, 1200 # frequency limitation
t0, t1 = 0, 60 * 20 # time limitation, 20 minutes

# Create mask for spectrogram matrix
f_mask = np.arange(len(fill_freqs))[(fill_freqs >= f0) & (fill_freqs <= f1)]
t_mask = np.arange(len(fill_times))[(fill_times >= t0) & (fill_times <= t1)]

# Plot decibel transform of spectrogram
fig, ax = plt.subplots()
ax.imshow(
  decibel(fill_spec[f_mask[0]:f_mask[-1], t_mask[0]:t_mask[-1]][::-1]), 
  extent=[t0, t1, f0, f1],
  aspect='auto', 
  cmap='viridis',
  interpolation='none'
)
plt.show()
```


# Wavetracker

A collection of algorithms for analyzing electrode-array recordings of
wave-type electric fish. These algorithms detect individual fish, track their
signals over time, and perform post-processing to eliminate and correct
tracking errors. 

**Terminology Note**:  
- *Wave-type electric fish* produce continuous, quasi-sinusoidal electric organ discharges (EODs).  
- *EOD frequency* refers to the fundamental frequency of the fish’s electric organ discharge.

---

## `wavetracker`

`wavetracker` is a command-line script that tracks signals of wave-type electric fish over time by utilizing two primary features:
1. **EOD frequency (fundamentals)**  
2. **Signal strength across multiple electrodes (signatures)**

### Basic Usage
```bash
wavetracker /path/to/dataset
```

### Pipeline Overview
1. **Convert raw data to a spectrogram**.  
   The raw recordings are transformed into a time–frequency representation.  
2. **Detect harmonic groups** using the [`thunderfish`](https://github.com/bendalab/thunderfish) package.  
   This step locates harmonic structures in the spectrogram that are indicative of individual fish signals.  
3. **Track EODs** by following the fundamental frequencies of each harmonic group, assigning identities to single fish over time.

All output data from this process is stored in a single folder as `.npy` files.

---

## `cleanup`

`cleanup` is a command-line script for post-processing and refining the results produced by `wavetracker`. It discards false detections and corrects obvious tracking errors.

### Basic Usage
```bash
cleanup /path/to/wavetracker/output/folder
```

---

## EODsorter

`EODsorter` is a graphical interface for manually inspecting and correcting any remaining tracking errors. It allows for fine-grained, human supervision to ensure the tracked signals are accurate.

### Basic Usage
```bash
EODsorter /path/to/wavetracker/output/folder
```

---

## Examples

Below are two brief examples demonstrating how to use the output produced by the `wavetracker` pipeline.

### 1. Display Tracked EOD Frequency Traces

```python
import matplotlib.pyplot as plt
import numpy as np

# Load tracking results
fund_v = np.load('fund_v.npy', allow_pickle=True)   # fundamental frequencies
idx_v = np.load('idx_v.npy', allow_pickle=True)     # indices in time array
ident_v = np.load('ident_v.npy', allow_pickle=True) # fish identities
times = np.load('times.npy', allow_pickle=True)     # corresponding time points

# Extract unique fish IDs (filter out NaNs)
ids = np.unique(ident_v[~np.isnan(ident_v)])

fig, ax = plt.subplots()
for fish_id in ids:
    # Plot EOD frequency over time for each fish
    ax.plot(times[idx_v[ident_v == fish_id]], 
            fund_v[ident_v == fish_id], 
            marker='.', 
            label=f'Fish {int(fish_id)}')

ax.set_xlabel('Time [s]')
ax.set_ylabel('Frequency [Hz]')
ax.legend()
plt.show()
```

**What this does**:  
- Loads the fundamental frequencies (`fund_v`), the time indices (`idx_v`), and each sample’s fish identity (`ident_v`).  
- Finds all unique fish IDs and plots the tracked frequency (y-axis) against time (x-axis) for each fish.

---

### 2. Load and Display a Fine Spectrogram

```python
import numpy as np
import matplotlib.pyplot as plt
from thunderlab.powerspectrum import decibel

# Load data
fine_freqs = np.load('fine_freqs.npy', allow_pickle=True)
fine_times = np.load('fine_times.npy', allow_pickle=True)
fine_spec_shape = np.load('fine_spec_shape.npy', allow_pickle=True)
fine_spec = np.memmap('fine_spec.npy', dtype='float', mode='r', shape=fine_spec_shape)

# Set frequency and time limits for visualization
f0, f1 = 0, 1200   # frequency range [Hz]
t0, t1 = 0, 60 * 20  # time range [s] (20 minutes)

# Create frequency and time masks to slice the spectrogram
f_mask = np.where((fine_freqs >= f0) & (fine_freqs <= f1))[0]
t_mask = np.where((fine_times >= t0) & (fine_times <= t1))[0]

# Prepare the subset of the spectrogram for plotting
spec_subset = fine_spec[f_mask[0]:f_mask[-1]+1, t_mask[0]:t_mask[-1]+1]

# Plot the decibel-transformed spectrogram
fig, ax = plt.subplots()
im = ax.imshow(
    decibel(spec_subset[::-1]),  # flip vertically for conventional freq axis
    extent=[t0, t1, f0, f1],
    aspect='auto',
    cmap='viridis',
    interpolation='none'
)

ax.set_xlabel('Time [s]')
ax.set_ylabel('Frequency [Hz]')
ax.set_title('Fine Spectrogram (dB)')
plt.colorbar(im, ax=ax, label='Power [dB]')
plt.show()
```

**What this does**:  
- Loads a higher-resolution spectrogram (`fine_spec`) along with its corresponding frequency and time axes.  
- Applies a decibel transform using `thunderlab.powerspectrum.decibel` for clearer visualization of power magnitudes.  
- Restricts the display to a specific frequency (`[f0, f1]`) and time range (`[t0, t1]`).  
- Uses `imshow` to display the spectrogram in a two-dimensional color-coded grid.

---

## Additional Notes

1. **Input Format**:  

  The `wavetracker` script expects your data to be organized into
  date/time-stamped folders, each containing one or more recordings in `.wav`
  format (or another supported audio format). An example directory structure is
  shown below:

  ```bash
  dataset/
  ├── 2024-01-01_12-34/
  │   └── recordings/
  │       ├── 2024-01-01_12-34.wav
  │       ├── 2024-01-01_12-35.wav
  │       ├── 2024-01-01_12-36.wav
  │       └── ...
  └── ...
  ```

  - **`dataset/`**  
    Top-level folder where each recording session is stored in a subfolder.
    
  - **`2024-01-01_12-34/`**  
    Example subfolder named by date and time. This helps identify individual recording sessions.
    
  - **`recordings/`**  
    Subfolder containing the actual audio files for a session. Each file typically represents a segment of continuous recording.  

    Make sure each subfolder follows this structure so that `wavetracker` can correctly locate and process your recordings.


2. **Memory Considerations**:  

   If your recordings are large, be aware that generating spectrograms and memmap files can be memory-intensive. Adjust parameters (e.g., window size, overlap) to optimize performance.

3. **Manual Inspection**:  

   Automated tracking can still yield false detections or missed events, which is why the `cleanup` and especially the `EODsorter` steps are important for achieving high-quality results.

---

**Questions or Issues?**  

If you run into problems, feel free to open an issue on [GitHub](https://github.com/weygoldt/wavetracker). Pull requests and contributions are welcome!

---

*Happy tracking!*
