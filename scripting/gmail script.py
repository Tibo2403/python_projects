import webbrowser
import time
import win32com.client

shell = win32com.client.Dispatch("WScript.Shell")
url="www.gmail.com"
email_to="*****@*****.com"
subject="Hello World!"
msg="Like a Swiss watch."
webbrowser.open("url")
time.sleep(9)
shell.SendKeys("c", 0)
time.sleep(1)
shell.SendKeys("email_to", 0)
time.sleep(1)
shell.SendKeys("{TAB}", 0)
time.sleep(1)
shell.SendKeys("{TAB}", 0)
time.sleep(1)
shell.SendKeys("subject", 0)
time.sleep(1)
shell.SendKeys("{TAB}", 0)
time.sleep(1)
shell.SendKeys("msg", 0)
time.sleep(1)
shell.SendKeys("{TAB}", 0)
time.sleep(1)
shell.SendKeys("{ENTER}", 0)