import pdfkit 

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
asset_path = os.path.join(dir_path,'asset')
asset_path = 'file:///' + asset_path.replace('\\','/') + '/'
print(asset_path)

f = open("out.html", "r", encoding="utf-8")
html = f.read()
html = html.replace('css/', asset_path)
html = html.replace('images/', asset_path)
html = html.replace('admin/images/', asset_path)

options = {
  'page-size':'A4', 'dpi':400,
  "enable-local-file-access": None,
  'encoding': "UTF-8",
}

pdfkit.from_string(html, 'out.pdf', options=options) 