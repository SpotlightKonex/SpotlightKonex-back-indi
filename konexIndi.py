import GiExpertControl as giLogin
import GiExpertControl as giJongmokTRShow
import time
import schedule

standardCodeList = []
currentDataList = []
previousDayDataList = []

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

    # [knx_mst] input: None

    def getKonexStandardCode(self):

        print("get konex standard code")
        TRName = "knx_mst"

        ret = giJongmokTRShow.SetQueryName(TRName)          
        rqid = giJongmokTRShow.RequestData()

        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TRName

    # output

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

                currentDataList.append([standardCode, currentPrice, changeRate, volume])
        
        # [VB] output: 표준코드(0), 전일종가(11), 전일누적체결수량(16)

        if TRName == "VB":

            nCnt = giCtrl.GetSingleRowCount()
            print("받아온 데이터의 개수: ", nCnt)

            for i in range(nCnt):
                standardCode = str(giCtrl.GetSingleData(i, 0)) # 표준코드
                previousDayClosingPrice = str(giCtrl.GetSingleData(i, 11)) # 전일종가
                previousDayQuantity = str(giCtrl.GetSingleData(i, 16)) # 전일누적체결수량

                previousDayDataList.append([standardCode, previousDayClosingPrice, previousDayQuantity])

        # [knx_mst] ouput: 표준코드(0)

        if TRName == "knx_mst":

            nCnt = giCtrl.getMultiRowCount()
            print("받아온 데이터의 개수: ", nCnt)

            for i in range(nCnt):
                standardCode = str(giCtrl.GetSingleData(i, 0)) # 표준코드
                standardCodeList.append(standardCode)
            
            print("StandardCodeList: ", standardCodeList)

if __name__ == "__main__":
    
    konexIndi = konexIndi()

    print("종목코드를 추가합니다.") # 맨 처음 한번 실행시켜주기
    konexIndi.getKonexStandardCode
    print("종목코드 추가 완료")

    def getKonexCurrentDataList():
        for standardCode in standardCodeList:
            konexIndi.getKonexCurrentData(standardCode)
            time.sleep(1)

    def getKonexPreviousDayDataList():
        for standardCode in standardCodeList:
            konexIndi.getKonexPreviousDayData(standardCode)
            time.sleep(1)

    # 1시간마다 현재가, 전일대비율, 누적거래대금 업데이트
    schedule.every(1).hours.do(getKonexCurrentDataList)

    # 매일 오전 8시에 전일종가, 전일누적체결수량 업데이트
    schedule.every().day.at("08:00").do(getKonexPreviousDayDataList)

    # 한 달에 한 번 표준코드 업데이트
    schedule.every().month.at("00:00").do(konexIndi.getKonexStandardCode)

    while True:
        # 예약된 작업을 실행
        schedule.run_pending()
        time.sleep(1)
    

                
            




            