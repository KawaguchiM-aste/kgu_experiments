# Laboratory for Health Science and Technology

## テキスト
- [Text_Student.pdf](./Text_Student.pdf)
- パスワードは授業で開示

## テーマごとの目次
- 音声信号処理
- 心電図
- 表面筋電図
- 脳波
- 近赤外線分光計測
- 姿勢計測: 床反力計
- [補足: Bitalino (r)evolutionによる生体信号計測](#appendix_bitalino)

<a id="appendix_bitalino"></a>
## Bitalino (r)evolution
- 本科目では，[この動画(YouTube)](https://www.youtube.com/watch?v=Y25ijv5EEKM)のようにOpenSignalsソフトウェアで計測し，Pythonコードで解析(可視化)を行う
- OpenSignalsのインストール方法，ペアリングについては省略する．
- いずれの実験においても，以下のことを確認すること
  - チャンネルの設定: どのチャンネル(A1, A2,...)にどの種類のセンサを接続したか．
  - サンプリング周波数(Sampling Rate[Hz]): EEG, EMG, ECGを計測する場合は1000を選択
  - データの保存場所(Save Location)
  - 保存形式: "txt"にチェックをつける
- [exportOpenSignals.py](./py/exportOpenSignals.py)は，OpenSignalsで計測したtxt形式のデータを，整形されたExcel Book(.xlsx)に変換する
  - 1列目は時刻，2列目はセンサー瞬時値となっている
  - 同時に複数のチャンネルで計測した場合，そのチャンネル数だけファイルが出力される．
  - 使用方法:
    - 作業ディレクトリにexportOpenSignals.pyとデータファイルをおく．
      - 作業ディレクトリの例として，ここではホームディレクトリの直下にjikkenという名前のディレクトリ(フォルダ)を作ったものとする
      - 例としてデータファイルの名前はopensignals_hoge.txtであったとする．
    - コマンドプロンプト，またはAnacondaプロンプト，Macの場合はターミナルを起動して，以下のコマンドを1行ずつ入力して，Enterを押す．
    ```
    cd jikken
    python exportOpenSignals.py opensignals_hoge.txt
    ```
    - 時間波形を描くウィンドウが表示されるので，閉じる．
    - しばらく待つと.xlsxファイルが出力される．

