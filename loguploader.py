import mwclient

site = mwclient.Site("zh.wikipedia.org")
page = site.Pages["User:Tiger-bot/SelfLinks"]

while True:
    try:
        pwd = input("Password?")
        site.login("Tiger-bot", pwd)
        break
    except mwclient.errors.LoginError:
        print("Password Error. Try again.")

with open("selflinklist.txt","w") as file:
    txt = file.read()

oldtext = page.text()
newtext = oldtext+"\n\n"+txt
page.save(newtext,"机器人：上传自链接检测记录。",minor=True)

print("Log saved in https://zh.wikipedia.org/wiki/User:Tiger-bot/SelfLinks")