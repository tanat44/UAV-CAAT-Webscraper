import requests
from bs4 import BeautifulSoup
import time

class Bot:
    def __init__(self, username, password):
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {
            'temail2': username, 
            'tpass': password
        }
        self.session = requests.Session()
        response = None
        try:
            response = self.session.post('https://uav.caat.or.th/search_member.php', headers=headers, data=payload)
            soup = BeautifulSoup(response.text, 'html.parser')
            error = soup.find('input', {'type': 'hidden', 'name': 'wrong'})
            if error is not None:
                self.close()
                return
        except:
            self.session = None
            return
    
        self.cookie = response.cookies.get_dict()

    def runPipeline(self, outputFolder=""):
        if self.session is None:
            return False

        id, name, status = self.getLastApplicationId()
        if "Requested approval" not in status:
            return status

        time.sleep(1)
        html = self.getCertificate(id)

        import os
        outputPath = os.path.join(outputFolder, f'CATT_{name}.pdf')

        self.savePdf(html, outputPath)
        self.close()

        return status

    def getLastApplicationId(self):
        if self.session is None:
            return False
        response = self.session.get('https://uav.caat.or.th/report_all_uav.php')
        soup = BeautifulSoup(response.text, 'html.parser')
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
        return id, name, status

    def getCertificate(self, id):
        payload = id
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = self.session.post('https://uav.caat.or.th/print_allow.php', headers=headers, data=payload)
        html = response.text

        # add signature tag
        soup = BeautifulSoup(html, 'html.parser')
        soup.script.decompose()
        signSpan = soup.find('span', {'id': 'mySpan_sign'})
        signPhoto = soup.new_tag('img', src= "asset/sign_new.jpg", height="55px", width="190px")
        signSpan.insert(0, signPhoto)
        html = str(soup)
        return html

    def savePdf(self, html, filepath):
        import pdfkit 
        import os 

        dir_path = os.path.dirname(os.path.realpath(__file__))
        asset_path = os.path.join(dir_path,'asset')
        asset_path = 'file:///' + asset_path.replace('\\','/') + '/'
        html = html.replace('asset/', asset_path)
        html = html.replace('css/', asset_path)
        html = html.replace('images/', asset_path)
        options = {
            'page-size':'A4', 'dpi':400,
            "enable-local-file-access": None,
            'encoding': "UTF-8",
            'quiet': None,
        }
        pdfkit.from_string(html, filepath, options=options) 

    def close(self):
        self.session.get('https://uav.caat.or.th/logout.php')
        self.session.close()
        self.session = None


# # get signature
# pmeters = "secret=4607741b12d9a057034fc1e8dbf64005"
# headers = {
#     "Content-type": "application/x-www-form-urlencoded",
#     "Content-length": str(len(pmeters)),
#     "Connection": "close"
# }
# response = session.post('https://uav.caat.or.th/hide_picute2.php', headers=headers, data=pmeters)
# print(response.text)