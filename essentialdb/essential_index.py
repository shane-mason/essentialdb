from essentialdb import SimpleDocument

class EssentialIndex:
    """HashIndex provides fast lookup indexing for dictionary"""

    def __init__(self, field_key, index_type='hash', index_name=None):
        self.field_key = field_key
        self.index_name = index_name if index_name != None else index_type + field_key
        self.index = {}

    def find(self, data, value):
        results = SimpleDocument()
        if value in self.index:
            for _id in self.index[value]:
                results[_id] = data[_id]
        return results

    def create_index(self, data):
        index = {}
        #start with a simple numeric indexing
        for item in data:
            if self.field_key in data[item] and data[item][self.field_key] not in index:
                index[data[item][self.field_key]] = []

            index[data[item][self.field_key]].append(item)
        self.index = index
        return self.index

    def update_index(self, document):
        if self.field_key in document:
            if document[self.field_key] not in self.index:
                self.index[document[self.field_key]] = []
                self.index[document[self.field_key]].append(document['_id'])
            elif document['_id'] not in document[self.field_key]:
                self.index[document[self.field_key]].append(document['_id'])


    def remove_from_index(self, document):
        if self.field_key in document:
            if document[self.field_key] in self.index:
                self.index[document[self.field_key]].remove(document['_id'])

