# UAV-CAAT-Webscraper
Automatic crawler (bot) script for extracting drone license certificate from https://uav.caat.or.th/

- List of username and password is provided in csv format.
- Bot uses respective user credential for logging in and fetch the status of latest application
- If it sees successful application (status is set to "Request Approved" on the website), it opens the certificate in html.
- Certificate is rendered and save to pdf using respective applicant'a name.
- A log file together with approval status is created in csv format (log.csv)

Usage / Legality is not guarantee in any cases.

## Technique
- Written in Python.
- "requests" library for keep cookie session, GET, POST
- "beautifulsoup" library for inspecting HTML tag / attributes, injecting some styling as neccessary
- Some of the static files, such as .css/.ttf/images are downloaded and modified to serve the purpose
- "pdfkit" library for rendering and save pdf
- "wkhtmltopdf.exe" is packaged with the distribution. No separate installation is required.

## Notes on development
- Create binaries and automatic copy asset folder
    > pyinstaller main.spec