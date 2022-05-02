def open_website(text):
    regex = re.search ('mở (.+)', text)
    if regex:
        domain = regex.group(1)
        url = 'https://www.24h.com.vn/du-bao-thoi-tiet-c568.html'
        webbrowser.open(url)
        speak("Trang web của bạn đã được mở lên!")
        return True
    else:
        return False