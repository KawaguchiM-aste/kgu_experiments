# Laboratory for Health Science and Technology

## テキスト
- [Text_Student.pdf](./Text_Student.pdf)
- パスワードは授業で開示

<a id="toc"></a>
## テーマごとの目次
- [音声信号処理](#sound_signal_processing)
- [心電図](#ecg)
- [表面筋電図](#emg)
- [脳波](#eeg)
- [近赤外線分光計測](#niro2ch)
- [姿勢計測: 床反力計](#pos_forceplate)
- [補足: Bitalino (r)evolutionによる生体信号計測](#appendix_bitalino)

<a id="sound_signal_processing"></a>
## 音声信号処理
- 概要
  - 音声信号を生成し，スマートフォンで録音する
  - 録音したデータを解析する．解析結果をレポートにまとめる
  - 音声信号の生成から解析までの過程をMATLABで行う
- 音声信号の生成用MATLABコード
  - いずれもmp3ファイルを出力する
  - [gen_sinsound.m](./m/gen_sinsound.m): 純音$x(t)=A\sin(\omega t)$を生成
  - [gen_rectsound.m](./m/gen_rectsound.m): 矩形波を生成
  - [gen_unsound.m](./m/gen_unsound.m): 「うなり」の生成
  - [gen_amsound.m](./m/gen_amsound.m): 振幅変調
- 音声信号の解析用MATLABコード
  - MATLAB Mobileで録音し，そのデータがMATLABのWorkspaceに配置されているという前提
  - [ana_audio.m](./m/ana_audio.m): Signal Processing Toolboxのpwelchコマンドを使用し，パワースペクトル密度の推定とその描画を行う
- [テーマごとの目次に戻る](#toc)

<a id="ecg"></a>
## 心電図
- 概要
  - [Bitalino (r)evolutionとOpenSignals](#appendix_bitalino)を用いて1ch心電図計測を行う．
  - データは[exportOpenSignals.py](#appendix_bitalino_exportOpenSignals)を用いてまずExcel bookファイルに変換する
  - Excel bookファイルを読み込みRR間隔列の基本的な解析を行う
  - 前処理の基線除去に[BioSPPy](https://biosppy.readthedocs.io/en/stable/)を用いている．
- データ解析用Pythonコード
  - [anaPSD.py](./py/anaPSD.py): パワースペクトル密度の推定と可視化を行うモジュール．下記anaECG.pyで使用．
  - [anaECG.py](./py/anaECG.py): RR間隔列の基本的な解析を行う
  - 実行方法:
    - 作業ディレクトリに以下のファイルをおく．
      - データファイル(.txt)
      - expportOpenSignals.py
      - anaPSD.py
      - anaECG.py
    - [exportOpenSignals.py](#appendix_bitalino_exportOpenSignals)を実行する．[こちら](#appendix_bitalino_exportOpenSignals)の例のようにデータファイルの名前がopensignals_hoge.txtであったとすると，opensignals_hoge_ECG.xlsxが出力される．
    - anaECG.pyを実行する．実行方法は以下の通り．
    ```
    python anaECG.py opensignals_hoge_ECG
    ```
      - (anaECG.pyを実行する際の引数を見ると，exportOpenSignals.pyを実行するときとは異なり，ファイル名に拡張子「.xlsx」を含めなくても実行される．それはなぜか，コードを読んで確認しておいてほしい)
- [テーマごとの目次に戻る](#toc)

<a id="emg"></a>
## 表面筋電図
- 概要
  - [Bitalino (r)evolutionとOpenSignals](#appendix_bitalino)を用いて表面筋電図計測を行う．
  - データは[exportOpenSignals.py](#appendix_bitalino_exportOpenSignals)を用いてまずExcel bookファイルに変換する
  - Excel bookファイルを読み込み包絡線の描画とRMS(Root Mean Square: 二乗平均平方根)の算出を行う
  - 前処理に[BioSPPy](https://biosppy.readthedocs.io/en/stable/)を用いている．
- データ解析用Pythonコード
  - [anaEMG.py](./py/anaEMG.py): 包絡線の描画を行い，選択された区間でRMSを算出する．
  - [anaEMGant.py](./py/anaEMGant.py): 複数のチャンネルでの計測データを読み込み，包絡線の描画を行う．
  - 実行方法:
    - 作業ディレクトリに以下のファイルをおく．
      - データファイル(.txt)
      - expportOpenSignals.py
      - anaEMG.py
      - anaEMGant.py
    - [exportOpenSignals.py](#appendix_bitalino_exportOpenSignals)を実行する．[こちら](#appendix_bitalino_exportOpenSignals)の例のようにデータファイルの名前がopensignals_hoge.txtであったとすると，opensignals_hoge_EMG.xlsxが出力される．複数チャンネルで計測した場合，opensignals_hoge_EMG.xlsx，opensignals_hoge_EMG1.xlsx，opensignals_hoge_EMG2.xlsx・・・のようにチャンネル数だけExcel bookファイルが出力される．
    - RMSを算出したい場合はanaEMG.pyを実行する．実行方法は以下のように1つのExcel bookファイル名を指定する．
    ```
    python anaEMG.py opensignals_hoge_EMG
    ```
      - 実行すると時間波形を描くウィンドウが表示されるので，これを **閉じずに** 筋発揮をしている区間(開始と終了時刻)を見つける
      - プロンプト画面で
      ```
      t_onset: 
      ```
      と表示される．ここに開始時刻を入力してEnterボタンを押す．
      - 続いてプロンプト画面で
      ```
      t_end: 
      ```
      と表示される．ここに終了時刻を入力してEnterボタンを押す．
      - その後にプロンプト画面で
      ```
      Press [Y], then RMS will be calculated. : 
      ```
      と表示される．ので半角でYと入力してEnterボタンを押すと，処理がはじまり，やがてプログラムが終了する．
    - 主動筋・拮抗筋の関係を見たい場合にはanaEMGant.pyを実行する．実行方法は以下のように複数のExcel bookファイル名を指定する(以下は2チャンネルでの測定の例)．
    ```
    python anaEMGant.py opensignals_hoge_EMG opensignals_hoge_EMG1
    ```
- [テーマごとの目次に戻る](#toc)

<a id="eeg"></a>
## 脳波
- 概要
  - [Bitalino (r)evolutionとOpenSignals](#appendix_bitalino)を用いて簡易的な脳波計測を行う．
  - データは[exportOpenSignals.py](#appendix_bitalino_exportOpenSignals)を用いてまずExcel bookファイルに変換する
  - Excel bookファイルを読み込み基本的な解析を行う
  - 前処理の基線除去に[BioSPPy](https://biosppy.readthedocs.io/en/stable/)を用いている．
- データ解析用Pythonコード
  - [anaPSD.py](./py/anaPSD.py): パワースペクトル密度の推定と可視化を行うモジュール．下記anaEEG.pyで使用．
  - [funcFilter.py](./py/funcFilter.py): バターワースフィルター処理を行うモジュール．下記anaEEG.pyで使用．
  - [anaEEG.py](./py/anaEEG.py): パワースペクトル密度の推定を行い，$\alpha$波と$\beta$波のパワーを求める
  - 実行方法:
    - 作業ディレクトリに以下のファイルをおく．
      - データファイル(.txt)
      - expportOpenSignals.py
      - anaPSD.py
      - funcFilter.py
      - anaEEG.py
    - [exportOpenSignals.py](#appendix_bitalino_exportOpenSignals)を実行する．[こちら](#appendix_bitalino_exportOpenSignals)の例のようにデータファイルの名前がopensignals_hoge.txtであったとすると，opensignals_hoge_EEG.xlsxが出力される．複数チャンネルで計測した場合，opensignals_hoge_EEG.xlsx，opensignals_hoge_EEG1.xlsx，opensignals_hoge_EEG2.xlsx・・・のようにチャンネル数だけExcel bookファイルが出力される．
    - anaEEG.pyを実行する．
      - 1chでの測定で，その箇所がFpzであった場合，実行方法は以下の通り．
      ```
      python anaEEG.py opensignals_hoge_EEG Fpz
      ```
      - 2chでの測定で，Bitalinoのチャンネル番号が小さい方から順にFpz, Ozであった場合の実行方法は以下の通り．
      ```
      python anaEEG.py opensignals_hoge_EEG Fpz opensignals_hoge_EEG1 Oz
      ```
      - 3ch以上の場合も同様に，Excelファイル名とその測定箇所をセットで並べていく
        - 実行すると時間波形を描くウィンドウが表示されるので，これを **閉じずに** 目視で定常的と思われる区間(開始と終了時刻．5秒程度)を見つける
      - 実行すると，プロンプト画面で
      ```
      t_start: 
      ```
      と表示される．ここに開始時刻を入力してEnterボタンを押す．
      - 続いてプロンプト画面で
      ```
      t_end: 
      ```
      と表示される．ここに終了時刻を入力してEnterボタンを押す．処理がはじまり，やがてプログラムが終了する．
- [テーマごとの目次に戻る](#toc)

<a id="niro2ch"></a>
## 近赤外線分光法
- 概要
  - NIRO-200NX(Hamamatsu Photonics)を用いて酸素化ヘモグロビン濃度等を計測する
- Pythonコード
  - [anaNIRO2ch.py](./py/anaNIRO2ch.py): NIRO-200NXで2chでの測定データ(拡張子は.nx2)を読み込み，時間波形を描画する
    - 本サイトに掲載されたコードは虫食い状態なので，テキスト「近赤外線分光法(1)」を参照して完成させる
    - nx2ファイル: 14行目以降はcsv形式．
    - 実行方法
      - 作業ディレクトリに以下のファイルをおく
        - データファイル: 例として，niro_sample.nx2とする
        - anaNIRO2ch.py
      - コマンドプロンプト，あるいはAnacondaプロンプト，Macの場合はターミナルを起動して，作業ディレクトリにcdする
      - anaNIRO2ch.pyを実行する．コマンドは以下の通り:
      ```
      python anaNIRO2ch.py niro_sample
      ```
- [テーマごとの目次に戻る](#toc)

<a id="pos_forceplate"></a>
## 床反力計を用いた姿勢計測
- 概要
  - 床反力計Accugait(AMTI)とg-Forceソフトウェア(フォーアシスト)を用いて静止立位姿勢計測を行い，リサンプルし，総軌跡長と矩形面積を算出する
- Pythonコード
  - [anaFP.py](./py/anaFP.py): g-Forceソフトウェアが出力するcsvファイルを読み込み，総軌跡長と矩形面積を算出する
    - 本サイトに掲載されたコードは虫食い状態なので，テキスト「姿勢計測(1)」を参照して完成させる
    - csvファイル: csv形式のデータは10行目からになっている
    - 実行方法
      - 作業ディレクトリに以下のファイルをおく
        - データファイル: 例として，FP_sample.csvとする
        - anaFP.py
      - コマンドプロンプト，あるいはAnacondaプロンプト，Macの場合はターミナルを起動して，作業ディレクトリにcdする
      - anaFP.pyを実行する．コマンドは以下の通り(「10.0」はリサンプルのサンプリング周波数[Hz]である):
      ```
      python anaFP.py FP_sample 10.0
      ```
- [テーマごとの目次に戻る](#toc)

<a id="appendix_bitalino"></a>
## 補足: Bitalino (r)evolutionとOpenSignalsによる生体信号計測

- 本科目では，[この動画(YouTube)](https://www.youtube.com/watch?v=Y25ijv5EEKM)のようにOpenSignalsソフトウェアで計測し，Pythonコードで解析(可視化)を行う
- OpenSignals [[Downloadはこちら](https://support.pluxbiosignals.com/knowledge-base/introducing-opensignals-revolution/)]のインストール方法，ペアリングについては省略する．
- いずれの実験においても，以下のことを確認すること
  - チャンネルの設定: どのチャンネル(A1, A2,...)にどの種類のセンサを接続したか．
  - サンプリング周波数(Sampling Rate[Hz]): EEG, EMG, ECGを計測する場合は1000Hzを選択
  - データの保存場所(Save Location)
  - 保存形式: "txt"にチェックをつける
- <a id="appendix_bitalino_exportOpenSignals">[exportOpenSignals.py](./py/exportOpenSignals.py)は，OpenSignalsで計測したtxt形式のデータを，整形されたExcel Book(.xlsx)に変換する</a>
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
    - その後の処理は，テーマによる．[心電図](#ecg)，[表面筋電図](#emg)，[脳波](#eeg)など．
- [テーマごとの目次に戻る](#toc)
