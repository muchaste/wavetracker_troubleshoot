import os
import numpy as np
import matplotlib.pyplot as plt
from thunderlab.powerspectrum import decibel
import argparse
#from IPython import embed


def main(path):
    
    # frequency traces
    f0 = np.load(os.path.join(path,'fund_v.npy'),   allow_pickle=True)
    idx = np.load(os.path.join(path,'idx_v.npy'),   allow_pickle=True)
    ids = np.load(os.path.join(path,'ident_v.npy'), allow_pickle=True)
    t   = np.load(os.path.join(path,'times.npy'),   allow_pickle=True)

    #if np.all(np.isnan(ids)):
    #    ids[:] = 1
    #    print('all ids are nan')

    fig, ax = plt.subplots()
    for fish in np.unique(ids[~np.isnan(ids)]):
    #for fish in np.unique(ids):
        mask = ids == fish
        ax.plot(t[idx[mask]], f0[mask], '.', label=f'Fish {int(fish)}')

    ax.set_xlabel('Time [s]'); ax.set_ylabel('Frequency [Hz]')
    ax.legend() 
    plt.show()
    fig.savefig(os.path.join(path, 'eodtrace.png'))
    print(f"Plot saved to {os.path.join(path, 'eodtrace.png')}")
    

    # fine spec

    freqs   = np.load(os.path.join(path, 'fine_freqs.npy'), allow_pickle=True)
    times   = np.load(os.path.join(path, 'fine_times.npy'), allow_pickle=True)
    shape   = np.load(os.path.join(path, 'fine_spec_shape.npy'), allow_pickle=True)
    spec_mm = np.memmap(os.path.join(path, 'fine_spec.npy'), dtype='float', mode='r', shape=shape, order='F')

    # display first 20 min, 0–1.2 kHz
    fmask = (freqs >= 0) & (freqs <= 1200)
    tmask = (times >= 0) & (times <= 1200)
    S_db  = decibel(spec_mm[fmask][:, tmask])

    fig, ax = plt.subplots()
    pcm = ax.pcolormesh(times[tmask], freqs[fmask], S_db, cmap='viridis')
    ax.set_xlabel('Time [s]'); plt.ylabel('Frequency [Hz]')
    ax.set_title('Fine spectrogram (dB)')
    fig.colorbar(pcm, label='Power [dB]', ax=ax)
    fig.savefig(os.path.join(path, 'finespec.png'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot EPD trace from given dataset")
    parser.add_argument("--path", required=True, help="Path to dataset")
    args = parser.parse_args()
    
    main(args.path)


"""
# fine spec

freqs   = np.load(os.path.join(path, 'fine_freqs.npy'), allow_pickle=True)
times   = np.load(os.path.join(path, 'fine_times.npy'), allow_pickle=True)
shape   = np.load(os.path.join(path, 'fine_spec_shape.npy'), allow_pickle=True)
spec_mm = np.memmap(os.path.join(path, 'fine_spec.npy'), dtype='float', mode='r', shape=shape, order='F')

# display first 20 min, 0–1.2 kHz
fmask = (freqs >= 0) & (freqs <= 1200)
tmask = (times >= 0) & (times <= 1200)
S_db  = decibel(spec_mm[fmask][:, tmask])

plt.pcolormesh(times[tmask], freqs[fmask], S_db, cmap='viridis')
plt.xlabel('Time [s]'); plt.ylabel('Frequency [Hz]')
plt.title('Fine spectrogram (dB)')
plt.colorbar(label='Power [dB]')
plt.show()
"""
"""
freqs = np.load(os.path.join(path, 'sparse_freq.npy'), allow_pickle=True)
times = np.load(os.path.join(path, 'sparse_time.npy'), allow_pickle=True)
shape = np.shape(freqs)
spec_mm = np.memmap(os.path.join(path, 'sparse_spectra.npy'), dtype='float', shape=shape, mode='r', order='F')


embed()

fmask = (freqs >= 0) & (freqs <= 1200)
tmask = (times >= 0) & (times <= 1200)
S_db  = decibel(spec_mm[fmask][tmask])#[:, tmask])

plt.pcolormesh(times[tmask], freqs[fmask], S_db, cmap='viridis')
plt.xlabel('Time [s]'); plt.ylabel('Frequency [Hz]')
plt.title('Fine spectrogram (dB)')
plt.colorbar(label='Power [dB]')
plt.show()
"""
