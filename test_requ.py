import requests
import re

def findOccurences(league, want, have):
	r = requests.get("http://currency.poe.trade/search", params={'league': league, 'online':'x', 'want':want, 'have':have})
	string = r.text.encode('ascii', 'ignore').decode('utf-8')
	tab = []
	triggered_char = 'displayoffer-middle'
	for i in re.finditer(triggered_char, s):
		inter = s[i.start()+21:i.start()+45]
		liste = (inter[:inter.find(' ')],inter[inter.find(' ', int(len(inter) / 2)):inter.find('<')])
		l1 = inter[:inter.find(' ')]
		inter = inter[inter.find(' ')+1:]
		inter = inter[inter.find(' ')+1:]
		l2 = inter[:inter.find('<')]
		tab.append('{} <= {}'.format(l1, l2))
	return tab