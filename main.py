from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.scard import *
from smartcard.util import *
import time
import requests
from dbHandler import Connection
from config import settings

db = Connection(settings['database'])


class printobserver(CardObserver):
    def update(self, observable, (addedcards, removedcards)):
        for card in addedcards:
            if addedcards:
                hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
                assert hresult == SCARD_S_SUCCESS
                hresult, readers = SCardListReaders(hcontext, [])
                assert len(readers) > 0
                reader = readers[0]
                hresult, hcard, dwActiveProtocol = SCardConnect(hcontext, reader, SCARD_SHARE_SHARED,
                                                                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
                hresult, response = SCardTransmit(hcard, dwActiveProtocol, [0xFF, 0xCA, 0x00, 0x00, 0x00])
                uid = toHexString(response, format=0)
                uid = uid.replace(" ", "")[:-4]
                url = 'https://whatsupdoc.epitech.eu/card/' + uid
                data = requests.get(url=url).json()
                email = data['login']
                print email
                status = db.manageUser(uid, email)
                print status


print("place card on reader")
while 1:
    cardmonitor = CardMonitor()
    cardobserver = printobserver()
    cardmonitor.addObserver(cardobserver)
    cardmonitor.deleteObserver(cardobserver)
    time.sleep(1)
