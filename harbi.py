import requests
import hashlib, random
from urllib.parse import quote
from utils import XGorgon8402


def getxg(param, data):
    """Generate X-Gorgon and X-Khronos headers based on parameters."""
    return XGorgon8402.getxg(
        param, hashlib.md5(data.encode()).hexdigest() if data else None, None
    )


def get_profile(session_id, device_id, iid):

    try:

        data = None
        parm = f"device_id={device_id}&iid={iid}&id=kaa&version_code=34.0.0&language=en&app_name=lite&app_version=34.0.0&carrier_region=SA&tz_offset=10800&mcc_mnc=42001&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone&device_type=iPhone13,4"
        sig = getxg(parm, data)
        url = f"https://api16.tiktokv.com/aweme/v1/user/profile/self/?{parm}"  # lite/v1/comment/publication
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id}",
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; fewfwdw; Build/PI;tt-ok/3.12.13.1)",
            "X-Gorgon": sig["X-Gorgon"],
            "X-Khronos": sig["X-Khronos"],
        }
        response = requests.get(
            url,
            headers=headers,
            cookies={"sessionid": f"{session_id}"},
        )
        res = response.text
        # print(res)
        return response.json()["user"]["unique_id"]
    except Exception as e:
        return "None"


def check_is_changed(last_username, session_id, device_id, iid):
    """Check if the username has been changed in the TikTok profile."""
    if get_profile(session_id, device_id, iid) != last_username:
        return True
    return False


def change_username(session_id, device_id, iid, last_username, new_username):
    """Attempt to change a TikTok username."""
    data = f"unique_id={quote(new_username)}"
    parm = f"device_id={device_id}&iid={iid}&residence=SA&version_name=1.1.0&os_version=17.4.1&app_name=tiktok_snail&locale=en&ac=4G&sys_region=SA&version_code=1.1.0&channel=App%20Store&op_region=SA&os_api=18&device_brand=iphone&idfv={iid}-1ED5-4350-9318-77A1469C0B89&device_platform=iphone&device_type=iPhone13,4&carrier_region1=&tz_name=Asia/Riyadh&account_region=eg&build_number=11005&tz_offset=10800&app_language=en&carrier_region=&current_region=&aid=364225&mcc_mnc=&screen_width=1284&uoo=1&content_language=&language=en&cdid={iid}&openudid={iid}&app_version=1.1.0&scene_id=830"
    sig = getxg(parm, data)

    url = f"https://api16.tiktokv.com/aweme/v1/commit/user/?{parm}"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"sessionid={session_id}",
        "sdk-version": "2",
        "user-agent": "com.zhiliaoapp.musically/{device_id} (Linux; U; Android 5; en; {iid}; Build/PI;tt-ok/3.12.13.1)",
        "X-Gorgon": sig["X-Gorgon"],
        "X-Khronos": sig["X-Khronos"],
    }

    response = requests.post(url, data=data, headers=headers)
    result = response.text
    if "unique_id" in result and check_is_changed(
        last_username, session_id, device_id, iid
    ):

        return "Username change successful."
    else:
        return "Failed to change username: " + str(result)


def main():
    device_id = str(random.randint(777777788, 999999999999))
    iid = str(random.randint(777777788, 999999999999))
    session_id = input("Enter the sessionid : ")

    user = get_profile(session_id, device_id, iid)
    if user != "None":
        print(f"Your current TikTok username is: {user}")
        new_username = input("Enter the new username you wish to set: ")
        print(change_username(session_id, device_id, iid, user, new_username))
    else:
        print("not wrok sessionid")

if __name__ == "__main__":
    main()
