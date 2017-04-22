import mwclient
import re
import time

site = mwclient.Site("zh.wikipedia.org")
reg = r"(\[\[\w+]]|\[\[\w+\|\w+]]|\[\[\w+\s\(\w+\)]]|\[\[\w+\s\(\w+\)\|\w+]])"
tagNeed = False

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
    match = re.findall(reg, text)

    for link in match:
        if link == "[[" + pageTitle + "]]":
            num1 = text.count(link)
            tagNeed = True
            continue
        elif "|" in link:
            par = link.split("|")
            if par[0][2:] == pageTitle:
                num2 = text.count("[["+pageTitle+"|")
                tagNeed = True
                continue

    if tagNeed:
        with open("selflinklist.txt","a") as log:
            log.write("#[["+pageTitle+"]]"+str(num1)+"个<nowiki>[[title]]<nowiki>，"+str(num2)+"个<nowiki>[[title|text]]</nowiki>\n")
        print(pageTitle + " tagged.")
        tagNeed = False
    else:
        print("No selflinks in " + pageTitle)
    time.sleep(1)
