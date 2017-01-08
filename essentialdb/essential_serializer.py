
import pickle
import json

class PickleSerializer:
    """
    Implements a basic (de)serializer based on pickle.
    """

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as fp:
            data = pickle.load(fp)
        return data

    @staticmethod
    def dump(data, file_path):
        with open(file_path, 'wb') as fp:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)


class JSONSerializer:
    """
    Implements a basic (de)serializer based on builtin json.
    """

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as fp:
            data = json.load(fp)
        return data

    @staticmethod
    def dump(data, file_path):
        with open(file_path, 'w') as fp:
            json.dump(data, fp, ensure_ascii=False)
