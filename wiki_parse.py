import json
d = json.load(open('wiki_it.json'))
pages = d['query']['pages']
for p in pages.values():
    text = p.get('extract','NO EXTRACT')
    print(text[:4500])
