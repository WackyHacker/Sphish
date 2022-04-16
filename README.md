# Sphish

```python3
#!/usr/bin/python3

from pwn import *
from sys import exit
from subprocess import getoutput
from os import system
from colored import fg, attr
from time import sleep
from argparse import ArgumentParser
from requests import post

burp = {'http': 'http://127.0.0.1:8080'}

parser = ArgumentParser()

parser.add_argument('-c', '--check', help='check and install dependencies', action='store_true')
parser.add_argument('-n', '--ngrok', help='Install and configure ngrok')
parser.add_argument('-s', '--sms', help='config sms API, set ID argument',)

args = parser.parse_args()

def def_handler(sig,frame):
	print('\nSaliendo...\n')
	exit(0)
signal.signal(signal.SIGINT, def_handler)

class Sphish():
	def __init__(self, ngrok, user, id):
		self.__ngrok = ngrok
		self.__user = user
		self.__id = id

	def banner(self):
			print(f"""%s
			███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
			██╔════╝██╔══██╗██║  ██║██║██╔════╝██║  ██║
			███████╗██████╔╝███████║██║███████╗███████║
			╚════██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║
			███████║██║     ██║  ██║██║███████║██║  ██║
			╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
								Created by %sWackyH4cker""" % (fg('cyan'), fg('red')))

	def dependencies(self):
		self.banner()
		with log.progress('Executed as') as p1:
			if self.__user == 'root':
				dependencies = ['php', 'wget']

				for i in dependencies:
					p1.success(self.__user)
					p2 = log.progress(i)
					if getoutput(f'command -v {i}'):
						sleep(1.5)
						p2.success('%s✔%s' % (fg('green'), attr('reset')))
					else:
						p2.failure('%s✘%s' % (fg('red'), attr('reset')))
						system(f'apt-get install {i} -y > /dev/null 2>&1')
			else:
				p1.failure(self.__user+', use %sroot%s.' % (fg('green'), attr('reset')))
				exit(1)
	def ngrok_download(self):
		self.dependencies()
		with log.progress(self.__ngrok) as p1:
			try:
				system('wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -O ngrok.tgz > /dev/null 2>&1')
				p1.success('%s✔%s' % (fg('green'), attr('reset')))
				system(f'tar -xf {self.__ngrok}.tgz')
				with log.progress('authtoken') as p2:
					system(f'./{self.__ngrok} config add-authtoken {args.ngrok} > /dev/null 2>&1')
					if getoutput(f'echo {args.ngrok} | wc -c') == '50':
						sleep(1.5)
						p2.success('%s✔%s' % (fg('green'), attr('reset')))
						system(f'rm -rf {self.__ngrok}.tgz')
					else:
						p2.failure('%s✘%s' % (fg('red'), attr('reset')))
			except ValueError:
				p1.failure('✘')
				exit(1)
	def send_sms(self, addressee, spoof_number, message):

		url = "https://us.sms.api.sinch.com/xms/v1/" + self.__id + "/batches"

		json_data = {
			"from": spoof_number,
 			"to": [
   				addressee.rstrip()
  			],
  			"body": message
		}

		headers = {
  			"Content-Type": "application/json",
  			"Authorization": f"Bearer {args.sms}"
		}

		r = post(url, json=json_data, headers=headers)

		if r.status_code != 201:
			print('Error sending message')

	def config_sms(self):
		self.dependencies()
		option = input('\n¿You want to use a dictionary of numbers? (y/n): ')
		
		if option == 'n':
			number = input('Addressee (Ex: 34632424224): ')
			self.send_sms(number)
		else:
			wordlist = input('Wordlit path: ')
			with open("nums.txt", "r") as wordlist:
				spoof_number = input('\n'+fg('white')+'\nFrom (Ex: Facebook.com): ')
				message = input('Menssage: ')
				for number in wordlist:
					self.send_sms(number, spoof_number, message)

sphish = Sphish('ngrok', getoutput('whoami'), '3dbdd80ac56447449f9ed7c500c4248b') # <- Enter your Service Plan ID

def main():
	if args.check:
		sphish.dependencies()
	elif args.ngrok:
		sphish.ngrok_download()
	elif args.sms:
		sphish.config_sms(	)
		
		sphish.config_sms()
if __name__ == '__main__':
	main()
  
```
