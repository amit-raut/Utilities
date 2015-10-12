#!/usr/bin/env python

import socket, xlwt, dns.resolver, os, logging, tld, json
from multiprocessing import Process, Pool, Lock, Value
from ctypes import c_int
from datetime import datetime as dt


unResolvedHostList = []
recordNum = 1


def getMXRecord(url_record):
	result = dns.resolver.query(url_record, 'mx')
	output = []
	for d in result:
		output.append(str(d.exchange))
	return output

	
def printandSave(record):
	global unResolvedHostList
	global recordNum
	outList = []
	try:
		mxRecordList = [(entry, socket.gethostbyname(entry)) for entry in getMXRecord(record)]
		for i in xrange(len(mxRecordList)):
			outList.append((record, socket.gethostbyname(record), mxRecordList[i][0], mxRecordList[i][1]))
		
		for entry in outList:
			print '{0:20s} {1:18s} {2:37s} {3:18s}'\
				.format(entry[0], entry[1], entry[2], entry[3])

			sheet1.write(recordNum,0, entry[0])
			sheet1.write(recordNum,1, entry[1])
			sheet1.write(recordNum,2, entry[2])
			sheet1.write(recordNum,3, entry[3])
			recordNum += 1

		book.save('/Users/AR/Desktop/weblookup_' + str(dt.now().date()) +'.xls')
	except Exception, e:
		unResolvedHostList.append(record)


def main():
	global unResolvedHostList
	with open('/Users/AR/Desktop/url_list.txt', 'r') as f:
		domainDetailsList = []
		domainNameList = []

		for line in f:
			if len(line) > 2:
				line1 = line[:-1] if line[-1] == '\n' else line
				url = line1 if line1.startswith('http') else 'http://' + line1
				try:
					domainNameList.append(tld.get_tld(url))
				except Exception, e:
					unResolvedHostList.append(url)

		domainList = list(set(domainNameList))

	for domain in domainList:
		printandSave(domain)

	if len(unResolvedHostList):
		print 
		sheet2 = book.add_sheet('Error Host Worksheet')
		sheet2.write(0,0, 'Host with Invalid Domain Names')
		sheet2.write(0,1, 'Host with No MX Records')
		rowCount = row2Count = 2
		for host in list(set(unResolvedHostList)):
			if host.startswith('http'):
				sheet2.write(rowCount,0, host)
				rowCount += 1
			else:
				sheet2.write(row2Count,1, host)
				row2Count += 1


if __name__ == '__main__':
	# Define Logging parameters
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)


	book = xlwt.Workbook(encoding="utf-8")
	sheet1 = book.add_sheet("Web Lookup")

	print '{:*^94}\n'.format(' Web Lookup! ') 

	# Printing the output to the console
	print '\n{0:20s} {1:18s} {2:37s} {3:18s}\n'\
	.format('Hostname', 'IP Address', 'MX Record', 'MX IP Address')

	# Saving Headers to Excel Spreadsheet
	sheet1.write(0,0, 'Hostname')
	sheet1.write(0,1, 'IP Address')
	sheet1.write(0,2, 'MX Record')
	sheet1.write(0,3, 'MX IP Address')

	main()	

	print '\nSpreadsheet saved! ' + str(recordNum - 1) + ' added to Spreadsheet.'	
	print '{:*^94}\n'.format(' EOP ')