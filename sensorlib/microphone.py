import sounddevice as sd
import scipy.io.wavfile
import numpy as np
from scipy.io.wavfile import write
from helper.logger import ErrorHandler
from scipy import signal
from configuration.local_config import LocalConfig


class Microphone:
    def __init__(self):
        self.fs = 0
        self.duration = 0
        self.error = ErrorHandler()
        self.config = LocalConfig()

    def get_fft_data(self):

        try:
            self.config.get_config_data()
            audiodata = sd.rec(int(self.config.audio["duration"]) * int(self.config.audio["fs"]),
                               samplerate=int(self.config.audio["fs"]), channels=1, dtype='float64')
            sd.wait()
            data = audiodata.transpose()
            f, pxx = scipy.signal.welch(data,
                                        fs=int(self.config.audio["fs"]),
                                        window='hanning',
                                        nperseg=int(self.config.audio["nperseg"]),
                                        noverlap=int(self.config.audio["noverlap"]),
                                        nfft=int(self.config.audio["nfft"]),
                                        detrend=False,
                                        return_onesided=True,
                                        scaling='density',
                                        )

            temp_data = np.array(pxx).astype(float)
            data = temp_data.tolist()

            return {"status": True, "data": data}

        except Exception as e:
            print(e)
            self.error.log.exception(e)
            return {"status": False, "data": 0}

    def write_wav_data(self, filepath):
        try:
            self.config.get_config_data()
            recording = sd.rec(int(self.config.audio["duration"]) * int(self.config.audio["fs"]),
                               samplerate=int(self.config.audio["fs"]),
                               channels=2)
            sd.wait()
            write(filepath, int(self.config.audio["fs"]), recording)
            return True
        except Exception as e:
            self.error.log.exception(e)
            return False
