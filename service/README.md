# サービスの作成
公式ドキュメントが整備されていないが、事例から`win32serviceutil`のソースコードを辿るとやるべきことが載っている。

https://github.com/mhammond/pywin32/blob/630ffa3a372874784b9e6f8b68359179b9ec259b/win32/Lib/win32serviceutil.py#L957

## SvcDoRunの実装
サービスとして何を実施するかを記述する。このメソッドが終了するとサービスとしても終了するので、実行間隔を設定して無限ループにすること。

## SvcStopの実装
「サービスの状態」から停止を受け付けられるようにするには、このメソッドを実装する。
`SERVICE_STOP_PENDING`を通知することで、サービスが停止中であることを伝える必要がある。

```
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
```

## 一時停止と再会の実装
「サービスの状態」から一時停止と再会を受け付けられるようにするには、`SvcPause`と`SvcContinue`を実装する。
停止と同様、`PENDING`の通知で時間のかかる処理を待ってもらい、`PAUSED`や`RUNNING`で状態が変わったことを通知する。

```
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
```

## 実行環境の整備
PyWin32に含まれるDLLと実行形式を、システム環境変数の`PATH`から参照できる位置に置く。これをしておかないと、サービスが起動できない。

* pythoncomXX.dll
* pywintypesXX.dll
* pythonservice.exe

## サービスの登録・起動・停止・削除
`install`と`start`を実行すれば、「サービス」の一覧に名前が表示されるはず。

```
python <サービスを書いたスクリプト> install
python <サービスを書いたスクリプト> start
python <サービスを書いたスクリプト> stop
python <サービスを書いたスクリプト> remove
```

### 異常で停止できなくなった場合
タスクマネージャから`pythonservice.exe`を探し、強制終了する。

### 相対パスの基点
ログの位置などを相対パスで記述すると、実行元によって基点が変わるので注意が必要。

* コマンドラインで起動: コマンドラインを実行したディレクトリが基点となる
* サービスとして起動: `pythonservice.exe`の場所が基点となる