#!/usr/bin/env python
import socket, xlwt, dns.resolver, os


def getMXRecord(url_record):
	result = dns.resolver.query(url_record, 'mx')
	output = []
	for d in result:
		output.append(str(d.exchange))
	return output

with open('/Users/AR/Desktop/url_list.txt', 'r') as f:

	book = xlwt.Workbook(encoding="utf-8")
	sheet1 = book.add_sheet("Sheet 1")

	sheet1.write(0,0, 'Hostname')
	sheet1.write(0,1, 'IP Address')
	sheet1.write(0,2, 'MX Record')
	sheet1.write(0,3, 'MX IP Address')
	hostIPList = []
	url = ''

	for line in f:
		if line[-1] == '\n':
			url = line[:-1]
		else:
			url = line
		hostIPList.append((url, socket.gethostbyname(url), \
		getMXRecord(url)))

	print '{0:13s}     {1:18s}     {2:30s}     {3:18s}    {4:8.8}\n'\
	.format('Hostname', 'IP Address', 'MX Record', 'MX IP Address', 'Status')
	rowcount = 1
	for record in hostIPList:
		for i in xrange(len(record[2])):
			print '{0:13s}     {1:18.15s}     {2:30s}     {3:18s}    {4:8.8}'\
			.format(record[0], record[1], record[2][i], socket.gethostbyname(record[2][i]), 
				'Up!' if os.system("ping -c 2 " + record[2][i] + ' | 2>&1') == 0 else 'Down!')

			sheet1.write(rowcount, 0, record[0])
			sheet1.write(rowcount, 1, record[1])
			sheet1.write(rowcount, 2, record[2][i])
			sheet1.write(rowcount, 3, socket.gethostbyname(record[2][i]))
			sheet1.write(rowcount, 4, 'Up!' if os.system("ping -c 2 " + record[2][i] + ' | 2>&1') == 0 else 'Down!')
			rowcount += 1

	book.save('/Users/AR/Desktop/IPlookups.xls')
	print '\nSpreadsheet saved!'
		