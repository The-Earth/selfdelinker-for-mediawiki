import mwclient
import re
import time
import os

site = mwclient.Site("zh.wikipedia.org")
reg = re.compile(r'\[\[\s*:?(.*?)(\|[\s\S]*?)?]]')
logPage = site.Pages["User:Tiger-bot/SelfLinks"]

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
            log.write("#[[%s]]，%d个<nowiki>[[title]]</nowiki>，%d个<nowiki>[[title|text]]</nowiki>\n" % (pageTitle, num1, num2))
        print(pageTitle + " tagged.")
    else:
        print("No selflinks in " + pageTitle)

    with open("selflinklist.txt", "r") as file:
        upload = False
        li = file.readlines()
        if len(li) >= 10:
            upload = True

    if upload:
        with open("selflinklist.txt", "r") as file:
            txt = file.read()
        oldtext = logPage.text()
        newtext = oldtext + "\n----\n" + txt
        logPage.save(newtext, "机器人：上传自链接检测记录。", minor=True)
        print("Log saved in https://zh.wikipedia.org/wiki/User:Tiger-bot/SelfLinks")

        with open("selflinklist.txt", "w") as file:
            file.write("")
    time.sleep(1)
