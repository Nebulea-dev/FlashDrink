import requests

class FD_API:
    BACKEND_URL = "http://141.145.208.206:5000/"

    @staticmethod
    def get_id_of_tag(tag_id):
        user_JSON = requests.get(FD_API.BACKEND_URL + "getUserOfTag?tag_id=" + tag_id)
        if user_JSON.status_code == 200:
            return user_JSON.json()['user_id']
        else:
            return None

    @staticmethod
    def get_balance(user_id):
        balance_JSON = requests.get(FD_API.BACKEND_URL + "getBalance?user_id=" + str(user_id))
        if balance_JSON.status_code == 200:
            return balance_JSON.json()['balance']
        else:
            return None

    @staticmethod
    def set_balance(tag_id, amount):
        balance_JSON = requests.post(FD_API.BACKEND_URL + "setBalance", json={'tag_id': tag_id, 'amount': amount})
        if balance_JSON.status_code == 200:
            return
        else:
            print("Error in set_balance request: " + str(balance_JSON.status_code))



