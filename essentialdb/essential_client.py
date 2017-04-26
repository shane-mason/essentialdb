
class EssentialClient():
    
    def __init__(self,  host=None,  port=None):
        self.host = None
        self.port = None
        
    def get_database(self,  db_id):
        self.db_id = db_id
        
