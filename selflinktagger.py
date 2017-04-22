import mwclient
import re
import time

site = mwclient.Site("zh.wikipedia.org")
reg = re.compile(r'\[\[\s*:?(.*?)(\|[\s\S]*?)?]]')

while True:
    try:
        pwd = input("Password?")
        site.login("Tiger-bot", pwd)
        break
    except mwclient.errors.LoginError:
        print("Password Error. Try again.")

for pagegen in site.random(0, limit=20):
    pageTitle = pagegen["title"]
    page = site.pages[pageTitle]
    text = page.text()
    tagNeed,num1,num2 = False,0,0

    for link in reg.finditer(text):
        if link.group(1).strip() == pageTitle:
            if link.group(2) and link.group(2) != '|':
                num2 += 1
            else:
                num1 += 1
            tagNeed = True

    if tagNeed:
        with open("selflinklist.txt","a") as log:
            log.write("#[[%s]]，%d个<nowiki>[[title]]</nowiki>，%d个<nowiki>[[title|text]]</nowiki>\n" % (pageTitle， num1, num2))
        print(pageTitle + " tagged.")
    else:
        print("No selflinks in " + pageTitle)
    time.sleep(1)
