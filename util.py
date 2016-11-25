def startsWith(text, prefix):
    return text[:len(prefix)] == prefix

def isLink(text):
    cant_start_with = ('http:', 'https:')
    return any([startsWith(text, prefix) for prefix in cant_start_with])

if __name__ == "__main__":
    print isLink("http://android.stackexchange.com/questions/41097/android-remote-desktop-thru-wifi-only")
    print isLink("hey there")
