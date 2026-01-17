import requests

def getUserByName(username):
    ROBLOX_USER_API = "https://users.roblox.com/v1/usernames/users"
    requestPayload = {
        "usernames": [
            username
        ],

        "excludeBannedUsers": True # Whether to include banned users within the request, change this as you wish
    }

    responseData = requests.post(ROBLOX_USER_API, json=requestPayload)

    # Make sure the request succeeded
    assert responseData.status_code == 200

    return responseData.json()["data"][0]

def getUserByID(id):
    ROBLOX_USER_API = "https://users.roblox.com/v1/users"
    requestPayload = {
        "userIds": [
            id
        ],

        "excludeBannedUsers": True # Whether to include banned users within the request, change this as you wish
    }

    responseData = requests.post(ROBLOX_USER_API, json=requestPayload)

    # Make sure the request succeeded
    assert responseData.status_code == 200

    return responseData.json()["data"][0]
