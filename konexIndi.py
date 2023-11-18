import sys
import GiExpertControl as giJongmokTRShow
from indiUI import Ui_MainWindow

class konexIndi():

    def __init__(self):
        super().__init__()
        giJongmokTRShow.RunIndiPython()
        giJongmokTRShow.SetCallBack('ReceiveData', self.giJongmokTRShowReceiveData)
        self.rqidD = {}

    # konexCurrentData - 표준코드, 현재가, 전일대비율, 누적거래대금

    def getKonexCurrentData(self, standardCode):
        
        print("get konex details")
        TRName = "VC"

        ret = giJongmokTRShow.SetQueryName(TRName)          
        ret = giJongmokTRShow.SetSingleData(0, standardCode) # 표준코드
        rqid = giJongmokTRShow.RequestData()

        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TRName

    # konexPreviousDayData - 전일종가, 전일누적체결수량

    def getKonexPreviousDayData(self, standardCode):
        
        print("get konex details")
        TRName = "VC"

        ret = giJongmokTRShow.SetQueryName(TRName)          
        ret = giJongmokTRShow.SetSingleData(0, standardCode) # 표준코드
        rqid = giJongmokTRShow.RequestData()

        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TRName