
class EssentialIndex:
    """HashIndex provides fast lookup indexing for dictionary"""

    def __init__(self, field_key, index_type='hash', index_name=None):
        self.field_key = field_key
        self.index_name = index_name if index_name != None else index_type + field_key
        self.index = {}


    def find(self, data, value):
        results = []
        if value in self.index:
            for _id in self.index[value]:
                results.append(data[_id])
        return results

    def create_index(self, data):
        index = {}
        #start with a simple numeric indexing
        for item in data:
            if data[item][self.field_key] not in index:
                index[data[item][self.field_key]] = []

            index[data[item][self.field_key]].append(item)
        self.index = index
        return self.index

class OrderedIndex(EssentialIndex):

    def __init__(self, field_key, index_name=None):
        super().__init__(field_key, "ordered", index_name)

    def create_index(self, data, field):
        self.index = super().create_index(data, self.field_key)
        self.sorted_index = sorted(self.index)



