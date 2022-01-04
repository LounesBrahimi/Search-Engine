import urllib.request

with urllib.request.urlopen("https://gutenberg.org/files/56667/56667-h/56667-h.htm") as url:
    s = url.read()
    print(s)