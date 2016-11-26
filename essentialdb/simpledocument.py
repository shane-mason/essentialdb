class SimpleDocument(dict):
    """
    Implements a dictionary object that can be addressed by dot notation to get at nested members.
    """
    def __getitem__(self, name):
        if isinstance(name, str) and "." in name:
            path = name.split(".")
            current = self
            for item in path:
                current = current[item]
            return current
        else:
            return super(SimpleDocument, self).__getitem__(name)
