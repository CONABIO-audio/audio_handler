from abc import abstractmethod, ABCMeta
import utils

class Media(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_media_info(self):
        pass

    @abstractmethod
    def read_media(self):
        pass

class Audio(Media):
    __metaclass__ = ABCMeta

    def __init__(self,path,sr=None,timeexp=1):
        self.read_sr = sr
        self.timeexp = timeexp
        self.path = path
        self.read_media()

    def read_media(self):
        self.signal, self.sr = utils.read(self.path,sr=self.read_sr)
        self.md5 = utils.binaryMD5(self.path)

        shape = list(self.signal.shape)

        if len(shape) > 1:
            self.nchannels = shape[0]
            self.length = shape[1]
        else:
            self.nchannels = 1
            self.length = shape[0]

        self.shape = shape
        self.duration = (float(self.length)/float(self.sr))/self.timeexp
        self.filesize = utils.media_size(self.path)


    def get_media_info(self):
        info = {}
        info["path"] = self.path
        info["filesize"] = self.filesize
        info["md5"] = self.md5
        info["timeexp"] = self.timeexp
        info["samplerate"] = self.sr
        info["length"] = self.length
        info["nchannels"] = self.nchannels
        info["duration"] = self.duration

        return info

    def get_spec(self,channel=0,n_fft=1024,hop_length=512):
        if channel > self.nchannels -1:
            return None

        sig = self.signal
        if self.nchannels > 1:
            sig = sig[[channel],:]

        return utils.spectrogram(sig,n_fft=n_fft,hop_length=hop_length)

    def plot(self,ax,channel=0,n_fft=1024,hop_length=512):
        spec = self.get_spec(channel=channel,n_fft=n_fft,hop_length=hop_length)
        return utils.plot_power_spec(spec,ax)



