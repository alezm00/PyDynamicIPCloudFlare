import requests,time,json

ZONE_ID = "YOUR_ZONE_ID_TOKEN"
BASE_LINK_ALL = "https://api.cloudflare.com/client/v4/zones/"
API_TOKEN = "YOUR_API_TOKEN"
RECORD_NAME = 'RECORDNAME'


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
    update()