# Kaidun (by HktOverload)

import json

SAVEFILE = 'SAVEFILE.json'

SAVEFILE_EMPTY_OBJ = {
    'scores': {},
}

SAVEFILE_EMPTY = json.dumps(SAVEFILE_EMPTY_OBJ)

def readSavefile():
    res = None
    try:
        with open(SAVEFILE, 'r') as f:
            res = json.loads(f.read())
        return res
    except:
        with open(SAVEFILE, 'w') as f:
            f.write(SAVEFILE_EMPTY)
        return SAVEFILE_EMPTY_OBJ

def writeSavefile(data):
    dataAsJSON = json.dumps(data)
    with open(SAVEFILE, 'w') as f:
        f.write(dataAsJSON)

def updateScore(timestamp, added):
    current = readSavefile()
    if timestamp not in current['scores']:
        current['scores'][timestamp] = added
    else:
        current['scores'][timestamp] += added
    writeSavefile(current)

