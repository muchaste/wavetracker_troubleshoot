# Wavetracker

[![Published in Frontiers in Integrative Neuroscience](https://img.shields.io/badge/Published%20in-Frontiers%20in%20Integrative%20Neuroscience-blue?style=for-the-badge)](https://www.frontiersin.org/articles/10.3389/fnint.2022.965211/full)

**Wavetracker** is a Python toolkit for analysing multi-electrode recordings of *wave-type electric fish*.  
It automatically detects individual fish, follows their electric-organ discharges (EODs) through time, and provides downstream utilities for curation and visualisation.  

---

### Key Concepts

| Term | Meaning |
|------|---------|
| *Wave-type fish* | Species that emit a continuous, quasi-sinusoidal EOD. |
| *EOD frequency* | Fundamental frequency of the electric discharge; uniquely identifies a fish over short time scales. |

---

## Installation

> **Requirements**: Python 3.9 – 3.12, Git ≥ 2.20, and ideally a virtual-environment manager (`venv`, Conda, Poetry, …).

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
# clone the development branch
git clone -b dev https://github.com/weygoldt/wavetracker.git
cd wavetracker

# (recommended) create & activate venv
python -m venv wavetracker_env
source wavetracker_env/bin/activate

# editable install
pip install -e .
```
</details>

<details>
<summary><strong>Windows (venv or Conda)</strong></summary>

```powershell
git clone -b dev https://github.com/weygoldt/wavetracker.git
cd wavetracker

# ---- venv ----
python -m venv wavetracker_env
.\wavetracker_env\Scripts\Activate.ps1
pip install -e .

# ---- or Conda ----
conda create -n wavetracker python=3.11
conda activate wavetracker
pip install -e .
```
</details>

Verify:

```bash
python -c "import importlib.metadata; print(importlib.metadata.version('wavetracker'))"
```

---

## Data Organisation

Place recordings in date-stamped session folders:

```
dataset/
└── 2024-01-01_12-34/
    └── recordings/
        ├── 2024-01-01_12-34.wav
        ├── 2024-01-01_12-35.wav
        └── …
```

Wavetracker will recurse through `recordings/` and assemble a continuous stream from sequential `.wav` files.

---

## End-to-end Pipeline

Run the full tracker with one command:

```bash
wavetracker /path/to/dataset
```

The script executes three stages:

1. **Spectrogram construction** – Each channel is converted to a high-resolution time–frequency representation (STFT).  
2. **Harmonic-group detection** – Using the [`thunderfish`](https://github.com/bendalab/thunderfish) library, harmonic stacks that belong to individual fish are located in the spectrogram.  
3. **Identity tracking** – Fundamental frequencies are extracted and stitched through time; electrode-array amplitude “signatures” help maintain identity when frequencies cross.

Outputs (`*.npy`) are written to a single results folder:

| File | Description |
|------|-------------|
| `fund_v.npy` | Vector of fundamental frequencies. |
| `idx_v.npy`  | Time-index vector for each detection. |
| `ident_v.npy`| Identity label for every detection. |
| `times.npy`  | Absolute time axis corresponding to indices. |

---

## Post-processing Tools

| Tool | Purpose | Invocation |
|------|---------|------------|
| `cleanup`   | Remove obvious false positives / correct tracking glitches. | `cleanup  path/to/output` |
| `EODsorter` | GUI for manual inspection and fine correction of tracks.   | `EODsorter path/to/output` |

---

## Example Analysis

### Plot EOD frequency traces

```python
import numpy as np, matplotlib.pyplot as plt

f0 = np.load('fund_v.npy',   allow_pickle=True)
idx = np.load('idx_v.npy',   allow_pickle=True)
ids = np.load('ident_v.npy', allow_pickle=True)
t   = np.load('times.npy',   allow_pickle=True)

for fish in np.unique(ids[~np.isnan(ids)]):
    mask = ids == fish
    plt.plot(t[idx[mask]], f0[mask], '.', label=f'Fish {int(fish)}')

plt.xlabel('Time [s]'); plt.ylabel('Frequency [Hz]')
plt.legend(); plt.show()
```

### Visualise a fine spectrogram

```python
import numpy as np, matplotlib.pyplot as plt
from thunderlab.powerspectrum import decibel

freqs   = np.load('fine_freqs.npy',        allow_pickle=True)
times   = np.load('fine_times.npy',        allow_pickle=True)
shape   = np.load('fine_spec_shape.npy',   allow_pickle=True)
spec_mm = np.memmap('fine_spec.npy', dtype='float', mode='r', shape=shape, order='F')

# display first 20 min, 0–1.2 kHz
fmask = (freqs >= 0) & (freqs <= 1200)
tmask = (times >= 0) & (times <= 1200)
S_db  = decibel(spec_mm[fmask][:, tmask])

plt.pcolormesh(times[tmask], freqs[fmask], S_db, cmap='viridis')
plt.xlabel('Time [s]'); plt.ylabel('Frequency [Hz]')
plt.title('Fine spectrogram (dB)')
plt.colorbar(label='Power [dB]')
plt.show()
```

---


## Practical Tips

* **Memory** – Long, high-sample-rate files produce large spectrograms and memmaps; adjust window length and overlap if you run into RAM limits.  
* **Validation** – Automatic tracking is robust but not perfect; use `cleanup` and `EODsorter` for publication-quality datasets.  
* **Windows specifics** – If PowerShell blocks `Activate.ps1`, run  
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.

---

Questions or pull requests? Visit the [GitHub issues page](https://github.com/weygoldt/wavetracker).  

*Happy tracking!* 🐟⚡
