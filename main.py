import os
try:
    import requests
    import requests.auth
    import robloxpy
except ModuleNotFoundError:
    import os
    os.system('python -m pip install robloxpy')

os.system('cls' if os.name == 'nt' else 'clear')

cookie = ''
itemID = ''

def GetCookie(customCookie):
    global cookie
    if customCookie == None:
        cookie = str(input('Your cookies:\n'))
    else:
        cookie = customCookie

def GetItemID(customItemID):
    global itemID
    if customItemID == None:
        item = open('./itemID.txt', 'r').read()
        if item == '':
            itemID = str(input('Your item ID:\n'))
        else:
            itemID = item
    else:
        itemID = customItemID

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
    print(f'Item ID: {itemID}')
    furl = requests.post(f'http://catalog.roblox.com/v1/favorites/users/{userID}/assets/{itemID}/favorite', headers={'X-CSRF-TOKEN': xcsrf, 'Referer': 'https://www.roblox.com'}, cookies={'.ROBLOSECURITY': cookie})
    print(f'URL Status Code: {furl.status_code}')
    print(f'URL Content: {str(furl._content).strip("}b'{")}')
    if int(furl.status_code) == 200 and str(furl._content) == "b'{}'":
        print('Success!')

def DoThing(customCookie, customItemID):
    GetCookie(customCookie)
    GetItemID(customItemID)
    isCookieValid = robloxpy.Utils.CheckCookie(cookie)
    if str(isCookieValid) == "Valid Cookie":
        print(isCookieValid)
        Fav()
    else:
        print(isCookieValid)

DoThing(None, None) # you can do whatever you want with it.
