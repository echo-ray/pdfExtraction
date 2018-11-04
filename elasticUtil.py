from elasticsearch import Elasticsearch



class elasticUtil():
    def __init__(self):
        self.hosts = '127.0.0.1'
        self.es = Elasticsearch(self.hosts, http_compress=True)

    def create(self, title, text):
        pass

    def search(self, title, text):
        pass