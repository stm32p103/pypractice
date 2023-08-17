import win32service
import win32serviceutil
import time
import logging

class PythonServiceExample( win32serviceutil.ServiceFramework ):
    # サービス名
    _svc_name_ = "PythonServiceExample"
    # 表示名
    _svc_display_name_ = "【例】サービス"
    # 説明
    _svc_description_='サービスの説明'

    # SvcDoRunのメインループを抜ける条件
    running = True

    def __init__( self, args ):
        win32serviceutil.ServiceFramework.__init__( self, args )

    # サービスの停止
    def SvcStop(self):
        # サービスが停止中であることを伝える
        # ステータスは以下参照
        # https://learn.microsoft.com/en-us/windows/win32/api/winsvc/nf-winsvc-controlservice#remarks
        self.ReportServiceStatus( win32service.SERVICE_STOP_PENDING )

        # 停止処理
        logging.info( 'STOPPING...' )

        # SvcDoRunのメインループを抜ける条件を設定
        self.running = False

    # 一時停止が必要な場合実装する
    # SvcContinueと合わせて実装しない場合、「サービスの状態」で「一時停止」ボタンが無効化される
    def SvcPause(self):
        # サービスが一時停止中であることを通知
        self.ReportServiceStatus( win32service.SERVICE_PAUSE_PENDING )
        logging.info( 'PAUSING' )
        
        # 一時停止処理(ダミー)
        time.sleep(3)

        # サービスが一時停止したことを通知
        self.ReportServiceStatus( win32service.SERVICE_PAUSED )
        logging.info( 'PAUSED' )
        
    # 一時停止が必要な場合実装する
    # SvcPauseと合わせて実装しない場合、「サービスの状態」で「再開」ボタンが無効化される
    def SvcContinue(self):
        # サービスが再開中であることを通知
        self.ReportServiceStatus( win32service.SERVICE_CONTINUE_PENDING )
        logging.info( 'CONTINUING' )

        # 再開処理(ダミー)
        time.sleep(3)

        # サービスが再開したことを通知
        self.ReportServiceStatus( win32service.SERVICE_RUNNING )
        logging.info( 'RUNNING' )

    # サービスの本体
    # このメソッドを呼び出す前に、親クラスでSERVICE_RUNNINGが通知され、サービスが実行中になる
    def SvcDoRun(self):
        # 開始時処理(例: ログファイルの準備)
        # pythonservice.exe基点の相対パスになる事に注意
        logging.basicConfig(
            filename=r'log.txt',
            level=logging.DEBUG,
            format="%(asctime)s:LINE[%(lineno)s] %(levelname)s %(message)s"
        )

        # メインループ
        while self.running:
            logging.info( time.asctime() )
            time.sleep( 5 )

        # メインループを抜けてこのメソッドが終了すると、親クラスでSERVICE_STOPPEDが通知され、サービスが停止する
        logging.info( 'EXIT MAIN LOOP' )
            
if __name__=='__main__':
    # コマンドラインからサービスの操作を行う
    win32serviceutil.HandleCommandLine( PythonServiceExample )

    # コマンド例
    # サービスの登録
    # python service_example install
    # サービスの削除
    # python service_example remove

    # サービスの開始
    # python service_example start
    # サービスの停止
    # python service_example stop

    # 強制終了する場合は、タスクマネージャから pythonservice.exe を探して停止する