import urllib.request
try:
    response = urllib.request.urlopen('http://localhost:7290/Home/Builder')
    html = response.read().decode('utf-8')
    print("Page fetched successfully. Length:", len(html))
except Exception as e:
    print("Failed to fetch:", e)
