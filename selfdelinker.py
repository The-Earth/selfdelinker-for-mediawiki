import mwclient
import re
import time

site = mwclient.Site("zh.wikipedia.org")

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
    oldtext = text
    match = re.findall(r"(\[\[.+]]|\[\[.+\|.+]])", text)

    for link in match:
        if link == "[["+pageTitle+ "]]":
            text = text.replace("[["+pageTitle+"]]",pageTitle)
        elif "|" in link:
            par = link.split("|")
            if par[0] == pageTitle:
                par[1] = par[1][0:-2]
                text = text.replace(link,par[1])

    if oldtext != text:
        page.save(text,"机器人：移除指向自身的链接",minor=True)
        print(pageTitle+" delinked.")
    else:
        print("No edit is needed in "+pageTitle)
    time.sleep(1)
