ファイル説明
テストデータは[csv]形式

1, plotplot.py：動的なチャートを表示（test_rssi.txtに追記されたデータを動的に読み込む）
2, plotplot2.py：移動軌跡を動的に表示(test_latlon.txtに追記されたデータを動的に読み込む)

3, test_lanlot_rssi.py: csvを読み込んで一行ずつtest_tssi.txtとtest_latlon.txtに追記していく。
スニファを使用した時のようにテストデータを流す為に作成した。

使用方法
3のプログラムを起動して、1,2のプログラムを起動すると流れてきたデータが逐次グラフに反映される様子が見られる。
