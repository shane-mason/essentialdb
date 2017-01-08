import unittest
import os
from essentialdb import PickleSerializer, JSONSerializer



class TestSerializers(unittest.TestCase):

    json_file_path = "test.json"
    pickle_file_path = "test.pickle"

    def __get_data(self):
        return dict({'f1': [1,2,3], 'f2': {'n1':'a', 'n2': 2}})

    def test_pickle(self):
        data = self.__get_data()
        PickleSerializer.dump(data, self.pickle_file_path)
        loaded = PickleSerializer.load(self.pickle_file_path)
        self.assertEqual(loaded['f2']['n1'], 'a')
        os.remove(self.pickle_file_path)


    def test_json(self):
        data = self.__get_data()
        JSONSerializer.dump(data, self.json_file_path)
        loaded = JSONSerializer.load(self.json_file_path)
        self.assertEqual(loaded['f2']['n1'], 'a')
        os.remove(self.json_file_path)
