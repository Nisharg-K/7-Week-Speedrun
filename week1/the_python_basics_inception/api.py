#This is a simple CLI Based Weather App, made for the purpose of learning API concepts in Python. 
#Learning week 1, Topic 3.


import requests

base_url = "https://wttr.in/"
location = "Vadodara"



print("Welcome to the weather CLI!")
print("We must feed you how you can see the weather is outside the window of Aditi Vadodara Office!")


response = requests.get(base_url + location, verify=False)

if response.status_code == 200:
    print(f"You can see the weather outside the Aditi Vadodara Office is: {response.text}")

else:
    print("Sorry, we couldn't fetch the weather information at the moment. Please try again later.")

    exit(0)

print("now its time to check weather of other cities")



while True:
    city = input("Enter the name of the city you want to check the weather for ")

    response = requests.get(base_url + city, verify=False)
    if response.status_code == 200:
        print(f"The weather in {city} is: {response.text}")
    else:
        print("Sorry, we couldn't fetch the weather information for that city. Please try again later.")
