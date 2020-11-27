# [Common Objects in Context (COCO)][COCO]
[COCO][] は、大規模な Object Detection, Segmentation, Captioning のための Dataset です。
画像とともに、アノテーション情報を含んでいます。

以下のタスクの学習に利用できます。
* Image Classification
* Object Detection
* Semantic Segmentation
* Instance Segmentation
* Caption Generation
* Pose Estimation

## Download
COCOのデータ・セットには以下のようなものがあります。
以下は、基本的に Object Detection 用のデータ・セットですが、
他に、Segmentation 用のアノテーション情報もあります。
* [トレーニング用画像](http://images.cocodataset.org/zips/train2017.zip)
* [評価用画像](http://images.cocodataset.org/zips/val2017.zip)
  - [トレーニング・評価用アノテーション](http://images.cocodataset.org/annotations/annotations_trainval2017.zip)
* [テスト用画像](http://images.cocodataset.org/zips/test2017.zip)
  - [テスト用情報](http://images.cocodataset.org/annotations/image_info_test2017.zip)

## COCO Format
`annotations_trainval2017.zip`ファイルを展開して、
`instances_{train,val}2017.json`を見ると(trainはファイルサイズが大きすぎて見ていない)、
以下のようにアノテーション情報が並んでいます。

フォーマットについては、 [ここ](http://cocodataset.org/#format-data) にあります。
COCO Format は、以下の５つのパートで構成されています。

1. info
2. licenses
3. images
4. annotations
5. categories

このうち、**info**, **licenses** はデータセットに固有の情報であり、
画像ファイル、アノテーション情報やその数に無関係です。

**images** は、画像ファイル１つ１つに対する情報を持ちます。
１つのオブジェクトは、画像ファイル１つの画像ファイルヘッダに含まれる情報を持ちます。
**annotations** は、一般物体検知であれば物体１つ１つに対する情報を持ちます。
１つのオブジェクトは、物体１つのアノテーション情報を持ちます。
**categories** は、一般物体検知であれば物体が属するカテゴリ１つ１つに対する情報を持ちます。
１つのオブジェクトは、カテゴリ１つの名前・識別子情報を持ちます。

次節から１つ１つのパートを説明します。

### "info": object
"info"オブジェクトには、データセットの情報(object)を記載します。

[COCO][]では以下の情報が記載されています

* "description": "COCO 2017 Dataset",
* "url": "http://cocodataset.org",
* "version": "1.0",
* "year": 2017,
* "contributor": "COCO Consortium",
* "date_created": "2017/09/01"

[Open Images Dataset V6 + Extensions]であれば以下の情報を記載します。

* "description": "Open Images Dataset V6 + Extensions",
* "url": "https://storage.googleapis.com/openimages/web/index.html",
* "version": "V6",
* "year": 2020,
* "contributor": "Google" 
* "date_created": "2020/02/26"

### "licenses": array
"licenses"オブジェクトには、"images"のライセンス情報をリストで記載します。
一意にライセンス情報を識別できるライセンスの識別子("id")を付与します。
この"id"は、"images"のobjectから"license"で参照されます。

[COCO][]では以下のような情報が複数記載されています

* "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
* "id": 1,
* "name": "Attribution-NonCommercial-ShareAlike License"

[Open Images Dataset V6 + Extensions]であれば以下のライセンス１つを記載します。

* "url": "https://creativecommons.org/licenses/by/4.0/",
* "id": 1,
* "name": "Attribution 4.0 International (CC BY 4.0)"

### "images": array
"images"オブジェクトには、画像ファイルの情報をリストで記載します。

[COCO][]では以下のような画像ファイルの情報が複数記載されています

* "license": 4,
    - ライセンス情報
* "file_name": "000000397133.jpg",
* "coco_url": "http://images.cocodataset.org/val2017/000000397133.jpg",
* "height": 427,
    - 高さ pixel
* "width": 640,
    - 幅   pixel
* "date_captured": "2013-11-14 17:02:52",
    - 画像キャプチャ時刻
* "flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
* "id": 397133
    - 画像ファイルの識別子
    
[Open Images Dataset V6 + Extensions]であれば以下のように画像ファイルの情報を記載します。
フリーで落ちている画像を拾ってきているわけではないので、urlの項目は持ちません。
その他の項目は、JPEGヘッダ情報に含まれています。

* "license": 1,
    - ライセンス情報は`CC BY 4.0`の１つだけ。
* "file_name": "e321a98048a49548.jpg",
* "coco_url": **なし**
* "height": 427,
    - 高さ pixel
* "width": 640,
    - 幅   pixel
* "date_captured": "2013-11-14 17:02:52",
    - 画像キャプチャ時刻(JPEGヘッダのProperties:date:modify)
* "flickr_url": **なし**
* "id": 0xe321a98048a49548
    - 画像ファイルの識別子(ファイル名:16進数)
    
### "annotations": array 
"annotations"オブジェクトには、アノテーション情報をリストで記載します。

[COCO][]では以下のような画像ファイルのアノテーション情報が複数記載されています

* "segmentation": array
    - 一次元配列?
* "area": 702.1057499999998,
    - 面積?
* "iscrowd": 0
    - その BoundingBox が含むオブジェクトが単一の場合は`0`, 複数の場合は`1` ? 
    - 今回はすべて単一のはずなので 0 とする
* "image_id": 289343
    - 画像ファイルのID
* "bbox": [ 473.07, 395.93, 38.65, 28.67 ]
    - バウンディングボックス `x, y, width, height` のpixel値として並んでいる
    - 注意点は x, y は左上の x_min, y_min であること。中心点ではないことに注意。
* "category_id": 18
    - カテゴリーの識別子
* "id": 1773
    - アノテーションの識別子
    
[Open Images Dataset V6 + Extensions]であれば以下のようにアノテーション情報を記載します。

* "segmentation": 今回は`object detection`タスクなので省略します。 **なし**
* "area": **なし**
* "iscrowd": **なし**
* "image_id": 0xe321a98048a49548
* "bbox": [ 473.07, 395.93, 38.65, 28.67 ]
    - バウンディングボックス `x, y, width, height` のpixel値として並んでいる
    - 注意点は x, y は左上の x_min, y_min であること。中心点ではない。
    - [Open Images Dataset V6 + Extensions][]では、pixel値に対する比率なので注意すること。
* "category_id": 18
    - カテゴリーの識別子(後述)
* "id": 1773
    - 一意に識別できるアノテーションの識別子
    
### "categories": array (物体のカテゴリ種類)
* "supercategory": "vehicle",
    - カテゴリの親分類
* "id": 2,
    - カテゴリの識別子
    - "annotations"から参照されます。
* "name": "bicycle"
    - カテゴリの名前
    - 同じ `supercategory` に複数の名前が存在することもある
    - e.g. `vehicle` に対して `car`, `motorcycle`, `airplane`, etc.

 - -
# COCO API via python

[こちら][Deep Learing - MS COCO データセットの概要]によると、
`cython`, `pycocotools` をインストールすると、[MS-COCO API][COCO API] を使用できるとのこと。

[MS-COCO API][COCO API] は、[COCO][]データ・セットのアノテーション情報を取得できるライブラリ。

アノテーション情報は json ファイルなので、json モジュールで読み込んで取得することもできるけど、
アノテーション情報を含む json ファイルは巨大なため、読み込みに時間がかかります。
ですが、`pycocotools`は`cython`で高速化されているため、処理が早いそうです。

以下のようにインストールできます。
`cython` は `--upgrade` を付けないとインストールできませんでした。

```bash
$ pip install --upgrade cython
$ pip install pycocotools
```

- - -
[COCO]: http://cocodataset.org/#home
[Deep Learing - MS COCO データセットの概要]: http://pynote.hatenablog.com/entry/mscoco
[MPRG ARCdataset]: http://mprg.jp/research/arc_dataset_2017_j
[COCO API]: https://github.com/cocodataset/cocoapi
[Open Images Dataset V6 + Extensions]: https://storage.googleapis.com/openimages/web/index.html
