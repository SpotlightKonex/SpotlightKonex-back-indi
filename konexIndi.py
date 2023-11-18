import GiExpertControl as giLogin
import GiExpertControl as giJongmokTRShow

currentData = []
previousDayData = []

class konexIndi():

    def __init__(self):
        super().__init__()
        giLogin.RunIndiPython()
        giJongmokTRShow.RunIndiPython()
        self.rqidD = {}

        giJongmokTRShow.SetCallBack('ReceiveData', self.giJongmokTRShowReceiveData)

        print(giLogin.GetCommState())
        if giLogin.GetCommState() == 0: # 정상
            print("")        
        elif  giLogin.GetCommState() == 1: # 비정상
            login_return = giLogin.StartIndi('234110','test0365!','', 'C:\\SHINHAN-i\\indi\\GiExpertStarter.exe')
            if login_return == True:
                print("INDI 로그인 정보", "INDI 정상 호출")
            else:
                print("INDI 로그인 정보", "INDI 호출 실패")  

    # [VC] input: 표준코드

    def getKonexCurrentData(self, standardCode):
        
        print("get konex current data")
        TRName = "VC"

        ret = giJongmokTRShow.SetQueryName(TRName)          
        ret = giJongmokTRShow.SetSingleData(0, standardCode) # 표준코드
        rqid = giJongmokTRShow.RequestData()

        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TRName

    # [VB] input: 표준코드

    def getKonexPreviousDayData(self, standardCode):
        
        print("get konex previous day data")
        TRName = "VB"

        ret = giJongmokTRShow.SetQueryName(TRName)          
        ret = giJongmokTRShow.SetSingleData(0, standardCode) # 표준코드
        rqid = giJongmokTRShow.RequestData()

        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TRName

    def giJongmokTRShow_ReceiveData(self,giCtrl,rqid):
    
        print("in receive_Data:",rqid)
        print('recv rqid: {}->{}\n'.format(rqid, self.rqidD[rqid]))
        TRName = self.rqidD[rqid]
        print("TR_name : ",TRName)

        # [VC] output: 표준코드(0), 현재가(3), 전일대비율(6), 누적거래대금(8)

        if TRName == "VC":

            nCnt = giCtrl.GetSingleRowCount()
            print("받아온 데이터의 개수: ", nCnt)

            for i in range(nCnt):
                standardCode = str(giCtrl.GetSingleData(i, 0)) # 표준코드
                currentPrice = str(giCtrl.GetSingleData(i, 3)) # 현재가
                changeRate = str(giCtrl.GetSingleData(i, 6)) # 전일대비율
                volume = str(giCtrl.GetSingleData(i, 8)) # 누적거래대금

                currentData.append([standardCode, currentPrice, changeRate, volume])
        
        # [VC] output: 표준코드(0), 전일종가(11), 전일누적체결수량(16)

        if TRName == "VB":

            nCnt = giCtrl.GetSingleRowCount()
            print("받아온 데이터의 개수: ", nCnt)

            for i in range(nCnt):
                standardCode = str(giCtrl.GetSingleData(i, 0)) # 표준코드
                previousDayClosingPrice = str(giCtrl.GetSingleData(i, 11)) # 전일종가
                previousDayQuantity = str(giCtrl.GetSingleData(i, 16)) # 전일누적체결수량

                previousDayData.append([standardCode, previousDayClosingPrice, previousDayQuantity])


                
            




            