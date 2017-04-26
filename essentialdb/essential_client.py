from essential_local import EssentialLocal

class EssentialClient():
    
    def __init__(self, host=None,  port=None):
        self.host = host
        self.port = port
        
    def get_database(self,  db_id=None,  filepath=None):
        return EssentialLocal(filepath=filepath)
