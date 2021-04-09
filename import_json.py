from pymongo import MongoClient
import json


class Import:
    def __init__(self):
        # Mongodb connection
        self.conn = MongoClient('mongodb://localhost:27017')

        # Mongodb database and repository
        db = self.conn.Twitter

        # Collections
        self.Barcelona = db.Barcelona  # Platforms

    def import_json_file(self):
        # df = pandas.read_json('Barcelona.json')
        # print(df)
        with open('barcelona.json', 'rb') as f:  # , encoding='cp1252'

            json_data = json.loads(
                f.read())
            # "loads()" converts from the Extended JSON syntax with "$oid" to an actual ObjectId instance.

        for i in json_data:
            # print(dict(i))
            self.Barcelona.insert_one(i)


if __name__ == "__main__":
    import_json = Import()
    import_json.import_json_file()
