
import os
import hashlib
import librosa
import numpy as np
import matplotlib.pyplot as plt

def read(path,sr):
    return librosa.load(path,sr=sr)

def binaryMD5(path):
    if path is not None:
        if os.path.isfile(path):
            BLOCKSIZE = 65536
            hasher = hashlib.md5()
            with open(path,"rb") as media:
                buf = media.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = media.read(BLOCKSIZE)
            return hasher.hexdigest()
        else:
            return None
    else:
        return None


def stft(sig,n_fft,hop_length):
    return librosa.stft(sig,n_fft=n_fft,hop_length=hop_length)

def plot_power_spec(spec,ax):
    librosa.display.specshow(librosa.amplitude_to_db(spec,ref=np.max),ax=ax,y_axis='log', x_axis='time')
    plt.colorbar(cax=ax,format='%+2.0f dB')
    plt.tight_layout()