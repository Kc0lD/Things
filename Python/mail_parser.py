import requests as req
from bs4 import BeautifulSoup as bs

url = "http://dev.sneakycorp.htb/team.php"
html = req.get(url).text 
soup = bs(html,'html.parser')

for tr in soup.find_all("tr"):
	print(tr.contents[7].text)
