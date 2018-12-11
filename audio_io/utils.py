
import os
import hashlib
import librosa
import librosa.display
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
    return librosa.stft(sig,n_fft,hop_length)

def spectrogram(sig,n_fft,hop_length):
    return np.abs(stft(sig,n_fft,hop_length))

def plot_power_spec(spec,ax):
    return librosa.display.specshow(librosa.amplitude_to_db(spec,ref=np.max),ax=ax,y_axis='linear',x_axis='time')
