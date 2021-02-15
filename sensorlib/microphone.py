import sounddevice as sd
import scipy.io.wavfile
import numpy as np
from scipy.io.wavfile import write
from helper.logger import ErrorHandler
from scipy import signal
import os


class Microphone:
    def __init__(self):
        self.fs = 0
        self.duration = 0
        self.error = ErrorHandler()

    def write_configuration_data(self, duration, fs):
        self.duration = int(duration)
        self.fs = int(fs)

    def get_fft_data(self):
        n_window = pow(2, 12)
        n_overlap = n_window / 2
        n_fft = n_window

        try:
            audiodata = sd.rec(self.duration * self.fs, samplerate=self.fs, channels=1, dtype='float64')
            sd.wait()
            data = audiodata.transpose()
            [F, pxx] = scipy.signal.welch(data,
                                          fs=self.fs,
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

            return {"status": True, "data": data}

        except Exception as e:
            print(e)
            self.error.log.exception(e)
            return False

    def write_wav_data(self, filepath):
        try:
            recording = sd.rec(self.duration * self.fs, samplerate=self.fs, channels=2)
            sd.wait()
            write(filepath, self.fs, recording)
            return True
        except Exception as e:
            print(e)
            self.error.log.exception(e)
            return False
