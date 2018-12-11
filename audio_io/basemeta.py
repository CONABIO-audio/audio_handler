from abc import abstractmethod, ABCMeta
import json
from baseaudio import audio

class Metadata(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def build_metadata(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def as_dict(self):
        pass


class audioMetadata(Metadata):
    __metaclass__ = ABCMeta

    def __init__(self,audio,raw_metadata,struct_path):
        self.media_info = audio.get_media_info()
        self.raw_metadata = raw_metadata

        with open(struct_path) as fin:
            self.meta_struct = json.load(fin)
            
        self.build_metadata()

    def build_metadata(self):
        self.metadata = self.validate()

        if self.metadata is not None:
            self.metadata["media_info"] = self.media_info
        else:
            raise ValueError("Bad inputs. Validation failed.")

    def validate(self):
        val_obj = {}
        validated = True
        actual_fields = self.meta_struct.keys()
        raw_fields = self.raw_metadata.keys()

        for field in actual_fields:
            required = actual_fields["required"]
            data_type = actual_fields["data_type"]
            out_val = None

            if field not in raw_metadata:
                if required:
                    validated = False
                    print("Field "+field+" is required but absent.")
                    break
            else:
                out_val = raw_metadata[field]

                if out_val is None:
                    if required:
                        validated = False
                        print("Field "+field+" is required but None.")
                        break
                elif not type(out_val).__name__ == data_type:
                    validated = False
                    print("Data type for "+field+" does not match required type: "+type(out_val).__name__+" VS "+data_type+".")
                    break

            val_obj[field] = out_val

        if validated:
            return val_obj
        else:
            return None

    def as_dict(self):
        return self.metadata




