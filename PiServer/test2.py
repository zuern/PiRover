import networkSend
def test():
    return 1
rec = networkSend.FileReciever(8000, test)
rec.start()
print("T")
rec.kill()
