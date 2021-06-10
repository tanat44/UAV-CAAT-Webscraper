# open file
f = open("list.html", "r", encoding="utf-8")
html = f.read()
f.close()

# add signature tag
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
firstRow = soup.tbody.find('tr')
cols = firstRow.findAll('td')
href = cols[6].a['href'].split(';')
href = href[0]
href = href.replace('(','')
href = href.replace(')','')
href = href.split(',')
id = {
    'rap_id_drone': href[1],
    'register_id': href[2]
}
name = cols[2].div.string.splitlines()
name = ''.join(name)
status = cols[5].div.decode_contents().splitlines()
status = ''.join(status)
print(id, name, status)
# soup.script.decompose()
# signSpan = soup.find('span', {'id': 'mySpan_sign'})
# signPhoto = soup.new_tag('div', style= "background-image: url(\'asset/sign_new.jpg\');height:55px;width:190px;")
# signSpan.insert(0, signPhoto)

# # save file
# f = open("out2.html", "w", encoding="utf-8")
# f.write(str(soup))