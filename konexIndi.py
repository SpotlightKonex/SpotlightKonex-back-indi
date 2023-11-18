import sys
import GiExpertControl as giJongmokTRShow
from indiUI import Ui_MainWindow

class konexIndi():

    def __init__(self):
        super().__init__()
        giJongmokTRShow.RunIndiPython()
        giJongmokTRShow.SetCallBack('ReceiveData', self.giJongmokTRShow_ReceiveData)
        self.rqidD = {}

    # konexDetails - 전일대비율, 누적거래량, 기업고유번호, 종목코드, 전일종가

    def getKonexDetails(self, standardCode):
        
        print("get konex details")
        TRName = "VC"

        ret = giJongmokTRShow.SetQueryName(TRName)          
        ret = giJongmokTRShow.SetSingleData(0, standardCode) # 표준코드
        rqid = giJongmokTRShow.RequestData()

        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TRName