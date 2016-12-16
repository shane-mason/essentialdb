
class EssentialIndex:
    """HashIndex provides fast lookup indexing for dictionary"""

    def __init__(self):
        self.index = {}


    def find(self, data, value):
        results = []
        if value in self.index:
            for _id in self.index[value]:
                results.append(data[_id])
        return results

    def create_index(self, data, field):
        index = {}
        #start with a simple numeric indexing
        for item in data:
            if data[item][field] not in index:
                index[data[item][field]] = []

            index[data[item][field]].append(item)
        self.index = index
        return self.index
