from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

QUERY_INTERVAL = 4
MAX_TRIES = 5

print("Welcome!")
print("This tool lets you know when a user came online and went offline from WhatsApp!")
print("")

phone_number = input("Enter the phone number you want to create logs for: ")

success = False
tries = 0

while (success != True and tries < MAX_TRIES):
	try:
		tries += 1
		driver = webdriver.Chrome()
		driver.get("https://web.whatsapp.com")
		success = True
	except ConnectionResetError:
		pass

if (tries == MAX_TRIES):
	print("Unable to open browser! Exiting...")
	exit(1)

print("Please log in to the web WhatsApp in the browser!")

while(True):
	try:
		first_element_after_login = driver.find_element_by_id("side")
		break
	except Exception:
		pass

search_box = driver.find_element_by_class_name("_2MSJr")
search_box.send_keys(phone_number)
search_box.send_keys(Keys.RETURN)

old_flag = None

def format_last_seen_string(s):
    word_list = s.split()
    final = [word_list[0].capitalize()]
    exceptions = ["at", "AM", "PM"]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

while(True):
	flag = True
	online_element = None
	time.sleep(QUERY_INTERVAL)
	
	try:
		online_element = driver.find_element_by_class_name("O90ur")
		if (online_element.get_attribute('innerHTML') != 'online'):
			raise Exception
	except Exception:
		flag = False

	if (flag != old_flag):
		if(flag):
			print("The user came online at",datetime.now().strftime('%H:%M:%S'))
		else:
			if (online_element is not None):
				print(format_last_seen_string(online_element.get_attribute('innerHTML')))
			else:
				print("The user went offline at",datetime.now().strftime('%H:%M:%S'))
		old_flag = flag