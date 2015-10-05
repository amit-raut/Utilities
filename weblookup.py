#!/usr/bin/env python
import socket, xlwt, dns.resolver, os, logging, tld
from multiprocessing import Pool



def getMXRecord(url_record):
	result = dns.resolver.query(url_record, 'mx')
	output = []
	for d in result:
		output.append(str(d.exchange))
	return output

# Threading to find server status
def checkConnectionStatus(ip_addr):
	return (ip_addr, 'Up!' if os.system("ping -c 1 -W 0 " + ip_addr + ' | 2>&1') == 0 else 'Down!')

def printRecordsAndSaveToExcel(outputList, statusList):
	recordNum = 2
	# Printing the output to the console
	print '{0:13s} {1:18s} {2:37s} {3:18s} {4:8.8}\n'\
	.format('Hostname', 'IP Address', 'MX Record', 'MX IP Address', 'Status')

	# Saving to Excel Spreadsheet
	sheet1.write(0,0, 'Hostname')
	sheet1.write(0,1, 'IP Address')
	sheet1.write(0,2, 'MX Record')
	sheet1.write(0,3, 'MX IP Address')
	sheet1.write(0,4, 'Status')

	for record in outputList:
		print '{0:13s} {1:18s} {2:37s} {3:18s} {4:8.8}'\
			.format(record[0], record[1], record[2], record[3], \
				[status[1] for status in statusList if status[0] == record[3]][0])
		sheet1.write(recordNum,0, record[0])
		sheet1.write(recordNum,1, record[1])
		sheet1.write(recordNum,2, record[2])
		sheet1.write(recordNum,3, record[3])
		sheet1.write(recordNum,4, [status[1] for status in statusList if status[0] == record[3]][0])
		recordNum += 1


def main():
	with open('/Users/AR/Desktop/url_list.txt', 'r') as f:
		domainDetailsList = []
		unResolvedHostList = []
		domainNameList = []

		for line in f:
			if len(line) > 2:
				line1 = line[:-1] if line[-1] == '\n' else line
				url = line1 if line1.startswith('http') else 'http://' + line1
				try:
					domainNameList.append(tld.get_tld(url))
				except Exception, e:
					unResolvedHostList.append(url)
					logger.info('Invalid Domain Name --> ' + url + '\n')

		domainList = list(set(domainNameList))

	for domainName in domainList:		
		#Check to see if the domain name provided is resolvable or not
		try:
			domainDetailsList.append((domainName, socket.gethostbyname(domainName), \
		getMXRecord(domainName)))
		except Exception, e:
			unResolvedHostList.append(domainName)
			logger.info('Can Not Resolve --> ' + domainName + '\n' )

	outputList = []
	for record in domainDetailsList:
		for i in xrange(len(record[2])):
			outputList.append((record[0], record[1], record[2][i], socket.gethostbyname(record[2][i])))
	
	mypool = Pool(len(outputList) - 1)
	statusList = mypool.map(checkConnectionStatus, [ip[3] for ip in outputList])
	
	printRecordsAndSaveToExcel(outputList, statusList)

	 
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
	sheet1 = book.add_sheet("Web Lookup Worksheet")

	print '{:*^94}'.format(' Web Lookup! ')
	print 

	main()

	book.save('/Users/AR/Desktop/weblookup.xls')
	print '\nSpreadsheet saved!'	
	print 
	print '{:*^94}'.format(' EOP ')