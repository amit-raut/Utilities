#!/usr/bin/env python

import subprocess as sp, time


def getHostnameAndIPaddr(url_addr):
	command = 'nslookup ' + url_addr + ' | grep ' + url_addr[:-1]
	with open('/Users/AR/Desktop/output.txt', 'a') as f: #This is the path for the output file
		ps = sp.Popen(command, stderr=sp.PIPE, stdout=f, shell=True)
		ps.communicate()[0]

		# ps.terminate()

def main():
	with open('/Users/AR/Desktop/url_list.txt', 'r') as f: #Use the correct absolute path for the url_list file
		for line in f:
			getHostnameAndIPaddr(line)

if __name__ == '__main__':
	main()



