# coding:utf-8
import hashlib
import json
from time import time
from hashlib import md5
from copy import deepcopy
from random import choice
import requests
import hashlib
import random
from urllib.parse import quote
import XGorgon8404

def get_profile(session_id, device_id, iid):
    """Retrieve the current TikTok username for a given session, device, and iid."""
    try:
        data = None
        parm = (
            f"device_id={device_id}&iid={iid}&id=kaa&version_code=34.0.0&language=en"
            "&app_name=lite&app_version=34.0.0&carrier_region=SA&tz_offset=10800&mcc_mnc=42001"
            "&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3"
            "&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone"
            "&device_type=iPhone13,4"
        )
        url = f"https://api16.tiktokv.com/aweme/v1/user/profile/self/?{parm}"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id}",
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; fewfwdw; Build/PI;tt-ok/3.12.13.1)",
  
        }
        response = requests.get(url, headers=headers, cookies={"sessionid": session_id})
        return response.json()["user"]["unique_id"]
    except Exception as e:
        return "None"


def check_is_changed(last_username, session_id, device_id, iid):
    """Check if the username has been changed in the TikTok profile."""
    return get_profile(session_id, device_id, iid) != last_username


def change_username(session_id, device_id, iid, last_username, new_username):
    """Attempt to change a TikTok username."""
    data = f"aid=364225&unique_id={new_username}"
    parm = f"aid=364225&residence=&device_id={device_id}&version_name=1.1.0&os_version=17.4.1&iid={iid}&app_name=tiktok_snail&locale=en&ac=4G&sys_region=SA&version_code=1.1.0&channel=App%20Store&op_region=SA&os_api=18&device_brand=iPad&idfv=16045E07-1ED5-4350-9318-77A1469C0B89&device_platform=iPad&device_type=iPad13,4&carrier_region1=&tz_name=Asia/Riyadh&account_region=sa&build_number=11005&tz_offset=10800&app_language=en&carrier_region=&current_region=&aid=364225&mcc_mnc=&screen_width=1284&uoo=1&content_language=&language=en&cdid=B75649A607DA449D8FF2ADE97E0BC3F1&openudid=7b053588b18d61b89c891592139b68d918b44933&app_version=1.1.0"
    
        
    sig = XGorgon8404.run(parm, md5(data.encode("utf-8")).hexdigest() if data else None,None)  
    url = f"https://api16.tiktokv.com/aweme/v1/commit/user/?{parm}"
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Whee 1.1.0 rv:11005 (iPad; iOS 17.4.1; en_SA@calendar=gregorian) Cronet",


        "Cookie": f"sessionid={session_id}",
    }
    headers.update(sig)
    response = requests.post(url, data=data, headers=headers)
    result = response.text
    if "unique_id" in result and check_is_changed(
        last_username, session_id, device_id, iid
    ):
        return "Username change successful."
    else:
        return "Failed to change username: " + str(result)


def main():
    """Main function to handle user interaction and username change."""
    device_id = str(random.randint(777777788, 999999999999))
    iid = str(random.randint(777777788, 999999999999))

    session_id = input("Enter the sessionid: ")

    user = get_profile(session_id, device_id, iid)
    if user != "None":
        print(f"Your current TikTok username is: {user}")
        new_username = input("Enter the new username you wish to set: ")
        print(change_username(session_id, device_id, iid, user, new_username))

    else:
        print("Invalid session ID or other error.")
    print("telegram @harbi")
    # telegram @harbi


if __name__ == "__main__":
    main()
