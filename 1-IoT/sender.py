import json
import random
from datetime import datetime
from azure.servicebus import ServiceBusService

def rd(mu, sigma):
    return abs(round(random.normalvariate(mu, sigma), 2))


def main():
    sbs = ServiceBusService(service_namespace='holEvents',
                            shared_access_key_name='RootManageSharedAccessKey',
                            shared_access_key_value='ugV/8wxg/Z0ZoTWBZWRUP5j2cgaEDiJC26ZLuoshotY=')
    turn = 0
    while turn >= 0:
        t = rd(19.6, 67.6)
        ap = rd(1002.6, 101.1)
        rh = rd(54, 13.6)
        v = rd(83.5, 99.1)
        pe = rd(445.6, 61.1)

        now = datetime.now().strftime("%M")

        if turn == 0:
            time = now
        else:
            if now != time:

                data = {"T":str(t), "V":str(v), "AP":str(ap), "RH":str(rh), "PE":str(pe)}

                body = str.encode(json.dumps(data))
                print(body)
                sbs.send_event('datatostream', body)

                time = now

        turn += 1

if __name__ == '__main__':
    main()