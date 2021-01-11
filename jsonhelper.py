import json

def getpoints():
    with open('data.json', 'r') as f:
                filejson = f.read()
                list = []
                filejson = json.loads(filejson)
                print((len(filejson['bpi'].keys())))
                daycount = 0
                for value in filejson['bpi'].values():
                    list.append((daycount,value/1000))
                    daycount += 1
                print(list)
                return list
