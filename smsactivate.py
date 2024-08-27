from credits import smsactivatetoken
import requests
import re
import time
import json

class smsactivate:
    def __init__(self):
        self.api_key = smsactivatetoken

    def checkavailable(self, country, operator):
        url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getNumbersStatus&country={country}&operator={operator}"
        response = requests.get(url)      
        if response.status_code == 200:
            data = response.json()
            print(data)  
        else:
            print("Error:", response.status_code)

    def get_balance(self):
        url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getBalance"
        response = requests.get(url)
        if response.status_code == 200:
            return (int(re.findall(r'ACCESS_BALANCE:(\d+)\.', response.text)[0])) 
        else:
            print("Error:", response.status_code)
            return None
    #balance = get_balance(api_key)

    def get_activation_number(self, service, country, forward=None, operator=None, ref=None, phone_exception=None, max_price=None, verification=None, use_cashback=None):
        url = f"https://sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getNumber&service={service}"               
        if forward:
            url += f"&forward={forward}"
        if operator:
            url += f"&operator={operator}"
        if ref:
            url += f"&ref={ref}"
        if country:
            url += f"&country={country}"
        if phone_exception:
            url += f"&phoneException={phone_exception}"
        if max_price:
            url += f"&maxPrice={max_price}"
        if verification:
            url += f"&verification={verification}"
        if use_cashback:
            url += f"&useCashBack={use_cashback}"

        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Error:", response.status_code)
            return None

    def get_active_activations(self):
            url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=getActiveActivations"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'activeActivations' in data:
                    active_activations = data['activeActivations']
                    # Создаем список словарей с информацией о каждой активации
                    activations_info = []
                    for activation in active_activations:
                        activation_info = {
                            'status': activation['activationStatus'],
                            'phone_number': activation['phoneNumber'],
                            'activation_id': activation['activationId']
                        }
                        activations_info.append(activation_info)
                    return activations_info
                else:
                    return {"error": "No active activations found"}
            else:
                return {"error": "Failed to fetch active activations"}
   
    def cancel_activation(self, activation_id):
        url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key={self.api_key}&action=setStatus&status=8&id={activation_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

#print(smsactivate().cancel_activation(str(smsactivate().get_active_activations()[0]['activation_id'])))
#print(smsactivate().get_activation_number(service = 'tg', country = '6', max_price='50'))         
#print(smsactivate().get_active_activations()[0]['phone_number'])
#print(smsactivate().get_active_activations()[0]['activation_id'])
#print(smsactivate().get_active_activations()[0]['status'])
