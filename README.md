# 文献管理スクリプト（.bib形式）
## 概要
- 文献管理ファイル(.bibファイル）作成Pythonスクリプト
- パッケージ[bibtexparser](https://bibtexparser.readthedocs.io/en/master/)をインストールする必要あり

## 実行方法
1. `read_bib.py`を実行  
    ```bash
    $ python read_bib.py
    ```

2. 編集先の.bibファイルのパスを聞かれるので入力する（ここでは`reference.bib`を編集するとする．ここで指定したファイルに文献情報が追記される）  
    ```
    Input reference .bib file path: reference.bib
    ```

3. 追記方法を聞かれる  
    ```
    Select mode
    [1] Read from .bib file
    [2] Input data manually
    [0] exit
    ```
    - 既存の.bibファイルの内容を追記する場合  
        - `1`を選択
        - .bibファイルのパスを聞かれるので入力する（ここでは`sample.bib`の内容を追記するとする）  
            ```
            Input .bib path: sample.bib
            ```
        - 入力した.bibファイルにkeyの抜け漏れがある場合は入力を求められるので，最低限入力必須な項目（`(Required)`となっている項目）は入力する（その他の項目は入力せずそのままEnterキーを押してもよい）  
            ```
            [ keywords ] (Required) : continuum theory of dislocations  # 入力必須項目は埋める
            [ memo ] (Required) : continuum theory of dislocations文献
            [ month ] :  # 必須でない項目は入力しなくてよい
            [ note ] :
            ```
    - コマンドライン上で直接入力する場合
        - `2`を選択
        - 各項目の入力を求めれられるので1つ1つ入力する

4. 文献情報を出力する.csvファイルのパスを聞かれるので入力する（ここでは`reference.csv`に文献情報の表を出力するとする）  
    ```
    Output .csv file path: reference.csv
    ```

## 備考
- 出力した文献情報（.bib or .csv）は[refviewer](https://kujirai.shinyapps.io/refviewer/)で確認できる
