# SVN
PythonにはSVNを操作するライブラリ`pysvn`があるので使ってみる。

`pip`では0.1.0と古い物しか入手できないので、[SourceForge](https://sourceforge.net/projects/pysvn/)からビルド済のものをダウンロードする。Pythonのバージョンが合っていないとインストールできないので、組み合わせに注意すること。

# pysvnの使用例
## SparseCheckout
GitでいうSparseCheckoutは、SVNだと段階を分けて行う。これを`pysvn`で実現しようとすると以下のようになる。

```
import pysvn
client = pysvn.Client( r'svnclient' )  # SVNクライアント関係のファイルの置き場

# 作業コピーを作成
client.checkout( r'<RepositoryURL>', r'<WCRoot>', depth = pysvn.depth.empty )

# ファイルまで辿る
client.update( r'<WorkingCopyRoot>/path/', depth = pysvn.depth.empty )
client.update( r'<WorkingCopyRoot>/path/to/', depth = pysvn.depth.empty )
client.update( r'<WorkingCopyRoot>/path/to/file.txt', depth = pysvn.depth.files )
```

### SparseCheckoutした作業コピーのcommit/update
一度SparseCheckoutしたら、以降は編集したものはコミットでき、リポジトリの変更はupdateで取得できる。

```
# まとめてコミット
client.checkin( r'<WCRoot>', '<CommitMessage>' )

# まとめて更新
client.update( r'<WCRoot>' )
```
