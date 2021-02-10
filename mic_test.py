import time
import sounddevice as sd
import scipy.io.wavfile
import datetime
from scipy import signal
import numpy as np
from scipy.io.wavfile import write
import os
from helper.filesize_helper import get_filesize
import shutil
from tinydb import TinyDB
from numpy import median

data_path = "/home/pi/beemo/db.json"
db = TinyDB(data_path)
db.truncate()


def get_fft_data():
    duration = 2
    n_window = pow(2, 12)
    fs = int(8000)
    n_overlap = n_window / 2
    n_fft = n_window

    try:
        audiodata = sd.rec(int(duration) * fs, samplerate=fs, channels=1, dtype='float64')
        sd.wait()
        data = audiodata.transpose()
        [F, pxx] = scipy.signal.welch(data,
                                      fs=fs,
                                      window='hanning',
                                      nperseg=n_window,
                                      noverlap=n_overlap,
                                      nfft=n_fft,
                                      detrend=False,
                                      return_onesided=True,
                                      scaling='density'
                                      )
        temp_data = np.array(pxx).astype(float)
        data = temp_data.tolist()

        db.insert({"test": str(data)})
        if median(data) == 0:
            print("data not okay")
        print(data)

    except Exception as e:
        print(e)
        return False


def get_wav_data(filename):
    duration = 200
    fs = 8000
    filesize = duration * 0.061
    minutes = duration / 60
    print(f"filesize at the end: {filesize}MB")
    print(f"recording {minutes} minutes...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, recording)
    return True



get_fft_data()
# filename = "test.wav"
#
# if get_wav_data(filename):
#     print(get_filesize(filename))


# 1 Sekunde = 0.061 MB fuer .wav Datei
# 0.046 fuer fft Datei


# total, used, free = shutil.disk_usage("/")
#
# print("Total: %d GiB" % (total // (2**30)))
# print("Used: %d GiB" % (used // (2**30)))
# print("Free: %d MB" % (free / 1024 / 1024))
