import json
from backend.constants import DATA_FILE, TAGS_FILE
from . import util


class Brain:

    def __init__(self):
        self.data = util.readjson(DATA_FILE)
        self.tags = util.readjson(TAGS_FILE)

    def add(self, data):
        key = data['key']
        val = data['val']
        tags = data['tags'] if 'tags' in data else ''
        tags = (tag.strip() for tag in tags.lower().split(','))
        tags = sorted(set(t for t in tags if len(t)))
        matches = [item for item in self.data if item['key'] == key]
        if matches:
            matches[0]['val'] = val
            matches[0]['tags'] = tags
        else:
            self.data.append({
                'key': key,
                'val': val,
                'tags': tags,
            })
        self.data.sort(key=lambda x: x['key'])

        # tags
        stored_tags = {tag['tag'] for tag in self.tags}
        for tag in set(tags) - stored_tags:
            self.tags.append({
                'tag': tag,
                'description': ''
            })
        self.store()

    def store(self):
        util.writejson(self.data, DATA_FILE)
        util.writejson(self.tags, TAGS_FILE)

    def get(self, params):
        return json.dumps({
            'items': self.data,
            'tags': self.tags
        })

    def exists(self, params):
        print('EXISTS method')
        key = params['key']
        keys = (item['key'] for item in self.data)
        if key in keys:  # TODO: use binary search
            return json.dumps(True)
        return json.dumps(False)

    def getitem(self, params):
        index = params['index']
        index = int(index)
        item = self.data[index]
        return json.dumps(item)

    def delete(self, params):
        index = params['index']
        index = int(index)
        self.data = self.data[:index] + self.data[index+1:]
        self.store()
