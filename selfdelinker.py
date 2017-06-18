import mwclient
import re
import time
from getpass import getpass

site = mwclient.Site("zh.wikipedia.org")
reg = re.compile(r'\[\[\s*:?(.*?)(\|[\s\S]*?)?]]')

while True:
    try:
        pwd = getpass("Password?")
        site.login("Tiger-bot", pwd)
        break
    except mwclient.errors.LoginError:
        print("Password Error. Try again.")

for page in site.allpages(namespace = "0",filterredir='nonredirects'):
    if not page.can("edit"):
        continue
    
    pageTitle = page.name
    text = page.text()
    oldtext = text

    for link in reg.finditer(text):
        if link.group(1).strip() == pageTitle:
            if link.group(2) and link.group(2) != '|':
                showText = link.group(2)
            else:
                showText = pageTitle
            text = text.replace(link.group(0), showText)

    if oldtext != text:
        page.save(text, "机器人：移除指向自身的链接", minor=True)
        print(pageTitle + " delinked.")
    else:
        print("No edit is needed in " + pageTitle)
    time.sleep(1)
