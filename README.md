# BarCodeDecoder (Minimal_BCDecoder)
BCDecoderのミニマル版。サイズを抑えるため、以下のものは含まれていません
- データセット（元データセット及び加工後のnpzファイル）
- トレーニングに用いたPythonスクリプト
- チェックポイントファイル
- データの調査に使用したPythonスクリプト
- そのほか、最終的に不使用となった各種Pythonスクリプト
- 訓練済みモデルのバリエーション（直近最高性能のモデルのみ収録）
- その他、不要なリソースファイル（アイコン素材など）

## BCDecoderとは
バーコードのデコードシステム。
ディープラーニングを用いた多クラス分類器を、バーコードのデコード処理に転用しました。
13桁のJANコードの仕様に準拠したバーコード画像を入力することで、適切なコードを返します。

## 使い方
1. `pip install -r requirements.txt`で必要なライブラリをインストール
  - (`BCD_Cli.py`実行時にエラーが出る場合は)[Visual C++ Redistributable Packages for Visual Studio 2013](https://www.microsoft.com/en-gb/download/details.aspx?id=40784)のインストール 
2. `BCD_Cli.py`を実行
3. Tempフォルダ内からバーコード画像を選択するか、自身で番号を入力
4. pyzbarを用いたデコード結果と、ディープラーニング版のデコード結果（内部的には推論結果）が表示されます