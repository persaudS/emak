#this is what it should look like for getting the data from glucometer_adaptor
'''from glucometerutil import glucometer as gl

def dump():
    data = gl.getdump()
    return data

def get_last():
    try:
        data = dump()
        data = data.split('"')
    except:
        return "N/A"
    if(data != ""):
        return data[13]
    return ""

def device_connected():
    try:
        data = dump()
    except:
        return False
    return True

if __name__ == "__main__":
  print(dump())
  print(get_last())
  print(device_connected())

'''