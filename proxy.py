from seleniumwire import webdriver
import time


# replace 'user:pass@ip:port' with your information
options = {
	'proxy': {
		'http': 'https://muratsalman0680:AC8kEw9V7c@198.105.102.148:50100',
		'https': 'https://muratsalman0680:AC8kEw9V7c@198.105.102.148:50100',
		'no_proxy': 'localhost,127.0.0.1'
	}
}

# replace 'your_absolute_path' with your chrome binary's aboslute path
driver = webdriver.Chrome(seleniumwire_options=options)

driver.get('http://whatismyipaddress.com')

time.sleep(1000)

driver.quit()