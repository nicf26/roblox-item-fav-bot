import os
try:
    import requests
    import requests.auth
    import robloxpy
except ModuleNotFoundError:
    os.system('python -m pip install requests')
    os.system('python -m pip install robloxpy')

os.system('cls' if os.name == 'nt' else 'clear')

cookie = ''
itemsID = {}

def GetCookie(customCookie):
    global cookie
    if customCookie == None:
        cookie = str(input('Your cookies:\n'))
    else:
        cookie = customCookie

def GetItemID(customItemsID):
    global itemsID
    if customItemsID == None:
        items = open('./itemsID.txt', 'r').readlines()

        if len(items) == 0 or (len(items) >= 1 and items[0].strip('\n') == 'item-id1...'):
            useritems = str(input('Your items ID (EXAMPLE: 1234567890 0987654321 3216549870):\n'))
            if str.find(useritems, ' '):
                itemsID = useritems.split(' ')
            print(itemsID)
        else:
            itemsID = items
    else:
        if str.find(customItemsID, ' '):
            itemsID = customItemsID.split(' ')

def GetXcsrf():
    #https://auth.roblox.com/v2/logout
    lurl = requests.post('http://auth.roblox.com/v2/logout', headers={'Referer': 'https://www.roblox.com'}, cookies={'.ROBLOSECURITY': cookie})
    return lurl.headers['x-csrf-token']

def GetUserID():
    #https://users.roblox.com/v1/users/authenticated
    aurl = requests.get('http://users.roblox.com/v1/users/authenticated', headers={'Referer': 'https://www.roblox.com'}, cookies={'.ROBLOSECURITY': cookie})
    userID = str(aurl._content).strip("}b'{").split(',')[0].strip('"id":')
    return userID

def Fav():
    #https://catalog.roblox.com/v1/favorites/users/{id}/assets/{item}/favorite
    userID = GetUserID()
    print(f'User ID: {userID}')
    xcsrf = GetXcsrf()
    print(f'X-CSRF-TOKEN: {xcsrf}')
    
    success = 0
    for i in range(len(itemsID)):
        furl = requests.post(f'http://catalog.roblox.com/v1/favorites/users/{userID}/assets/{itemsID[i].strip('\n')}/favorite', headers={'X-CSRF-TOKEN': xcsrf, 'Referer': 'https://www.roblox.com'}, cookies={'.ROBLOSECURITY': cookie})
        if int(furl.status_code) == 200 and str(furl._content) == "b'{}'":
            success += 1
    print(f'{success}/{len(itemsID)} Success!')

def DoThing(customCookie, customItemID):
    GetCookie(customCookie)
    GetItemID(customItemID)
    isCookieValid = robloxpy.Utils.CheckCookie(cookie)
    if str(isCookieValid) == "Valid Cookie":
        print(isCookieValid)
        Fav()
    else:
        print(isCookieValid)

if __name__ == "__main__":
    DoThing(None, None) # you can do whatever you want with it.