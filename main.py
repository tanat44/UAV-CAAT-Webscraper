from bot import Bot
import csv
import time
import os 
import datetime

filename = 'test data/in.csv'

# prepare output folder
dirPath = os.path.dirname(os.path.realpath(filename))
timeString = datetime.datetime.now().strftime('%y%m%d-%H%M')
newDirPath = os.path.join(dirPath, timeString)
if not os.path.exists(newDirPath):
    os.makedirs(newDirPath)

# get username, password
applicants = []
with open(filename, newline='', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if len(row) != 2: 
            continue
        applicants.append({
            'username': row[0],
            'password': row[1]
        })

# execute bot
for i in applicants:
    print(f"Run {i['username']}")
    mybot = Bot(i['username'], i['password'])
    i['status'] = mybot.runPipeline(outputFolder = newDirPath)
    print(f"-{i['status']}")
    time.sleep(5)

# save output
print("Saving log file")
outputLogPath = os.path.join(newDirPath, 'log.csv')
with open(outputLogPath, 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in applicants:
        spamwriter.writerow([i['username'], i['password'], i['status']])

print('Bye!')