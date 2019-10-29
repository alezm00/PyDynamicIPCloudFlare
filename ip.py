import requests,time,json,config



def GetIP():
    r = requests.get(r'http://jsonip.com')
    return r.json()['ip']

def update():
    a = requests.get((BASE_LINK_ALL + ZONE_ID + '/dns_records'),headers={
        'Authorization': API_TOKEN,
        'Content-Type': "application/json"
    })
    a = a.json()['result']
    found = False
    for i in a:
        if i['name'] == RECORD_NAME:
            a = i
            found = True
    if not found:
        print('NO...')
        print('Creating...')
        b = requests.post((BASE_LINK_ALL + ZONE_ID + '/dns_records'),headers={
            'Authorization': API_TOKEN,
            'Content-Type': "application/json"
        },json={
            "type":"A",
            "name": RECORD_NAME,
            "content": GetIP()
        })
        if b.json()['success']:
            print()
    else:
        if a['content'] == GetIP():
            print('No update needed')
        else:
            print('updating...')
            b = requests.put((BASE_LINK_ALL + ZONE_ID + '/dns_records/' + (a['id'])),headers={
                'Authorization': API_TOKEN,
                'Content-Type': "application/json"
            },json={
                "type":"A",
                "name": a['name'],
                "content": GetIP()
            })
            if b.json()['success']:
                print('IP aggiornato')



if __name__ == "__main__":
    if (not hasattr(config,'ZONE_ID') and
        not hasattr(config,'BASE_LINK_ALL') and
        not hasattr(config,'API_TOKEN') and
        not hasattr(BASE_LINK_ALL,'RECORD_NAME')):

            print("config error",'\n')
            print("Must be defined like in the file config.py.example",'\n')
    else:
        ZONE_ID = config.ZONE_ID
        BASE_LINK_ALL = config.BASE_LINK_ALL
        API_TOKEN = config.API_TOKEN
        RECORD_NAME = config.RECORD_NAME
        update()
        k=input("Script completed press Enter to exit") 