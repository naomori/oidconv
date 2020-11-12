# やりたいこと

画像の中のナンバープレートを検知して、境界ボックス情報を取得したいです。
なぜなら、ナンバープレートは個人情報なので、取扱いに気をつける必要があるからです。

* ナンバープレートの検知には機械学習を使います。
* 機械学習のネットワークモデルの訓練には、オープンなデータセットを使います。
* 機械学習の推論は[Amazon Rekognition Custom Labels][]を使います。

# Open Images Dataset v6 to Ground Truth

オープンで有名なデータセットとしては、[COCO][], [Open Images Dataset][]があります。 
また、[Google Dataset Search][]で検索することもできます。

自前でデータセットを作成することもできますが、それには膨大な時間と手間がかかります。
最終的に推論精度を向上させるために、自前のデータセットを作成する場合もあると思いますが、
まずは、オープンなデータセットを利用して、どのようなデータを使えば
ニューラルネットワークモデルの精度が上がるのかを試してみることにします。

そこで、[VoTTで作成したデータをCustom Labelsで利用可能なAmazon SageMaker Ground Truth形式に変換してみました][]を参考に、
[Open Images Dataset][]からナンバープレートの画像とアノテーション情報を抜き出して、 
[Amazon SageMaker Ground Truth][]のデータセットを作成します。
出力形式は、[Amazon SageMaker 出力データ][]の"境界ボックスジョブの出力"に記載があります。

[Amazon SageMaker Ground Truth][]のデータセットは、
[Amazon Rekognition Custom Labels][]でも利用可能なため、
AWSで機械学習を考えている状況では、とても役に立ちそうです。

## 画像とアノテーション情報をダウンロードします
[Open Images Dataset][]からダウンロードします。
ダウンロードするファイルは、Amazon S3 上にあるファイルです。
かなり多いので何回かに分けて、夜中にでもダウンロードしておきます。

* Images: Download from CVDF
    - s3://open-images-dataset/tar/train_0.tar.gz  (46G)
    - s3://open-images-dataset/tar/train_1.tar.gz  (34G)
    - s3://open-images-dataset/tar/train_2.tar.gz  (33G)
    - s3://open-images-dataset/tar/train_3.tar.gz  (32G)
    - s3://open-images-dataset/tar/train_4.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_5.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_6.tar.gz  (32G)
    - s3://open-images-dataset/tar/train_7.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_8.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_9.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_a.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_b.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_c.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_d.tar.gz  (31G)
    - s3://open-images-dataset/tar/train_e.tar.gz  (28G)
    - s3://open-images-dataset/tar/train_f.tar.gz  (28G)
    - s3://open-images-dataset/tar/validation.tar.gz  (12G)
    - s3://open-images-dataset/tar/test.tar.gz  (36G)
* Boxes: {Train, Validation, Test}
* Image labels: {Train, Validation, Test}
* Image IDs: {Train, Validation, Test}
* Metadata: Class Names

## 検知するもの

Metadata の Class Names からダウンロードした
`class-descriptions-boxable.csv`を見て、車関連のラベルのうち、
検知したいものをいくつか選んでおきます。
なぜなら、[Amazon Rekognition Custom Labels][]で物体検知をするためには、
1つのラベルだけというのは駄目で複数のラベルが必要だからです。

検知したいものは、`Metadata`の`Class Names`のファイルで選んでおきます。
```bash
/m/01jfm_,Vehicle registration plate
/m/04_sv,Motorcycle
/m/0k4j,Car
/m/07yv9,Vehicle
/m/015qff,Traffic light
/m/01mqdt,Traffic sign
/m/0199g,Bicycle
/m/01bqk0,Bicycle wheel
/m/01bjv,Bus
/m/07r04,Truck
/m/012n7d,Ambulance
/m/02pv19,Stop sign
/m/0h9mv,Tire
/m/0pg52,Taxi
```

## アノテーション情報の第一次選別

こちらの
[Open Image Dataset V5を使ってみる](https://blog.imind.jp/entry/2019/06/18/210510)
がとても参考になります。

訓練用のアノテーション情報`oidv6-train-annotations-bbox.csv`を
そのまま開こうとするとファイルが大き過ぎて、PCのメモリ不足で開けなかったりします。
ですので、まずは、検知したい物体が含まれる行のみを選んで、新しいファイルに保存します。

対象のファイルから、検知したい物体が含まれる行のみを選んで、
ファイル拡張子の直前に"_pickup"を付加した新しいファイルに保存します。

必要なファイルは、物体ごとの境界ボックス情報が記載されている
Boxes: {Train, Validation, Test}の以下のファイルです。
* oidv6-train-annotations-bbox.csv
* validation-annotations-bbox.csv
* test-annotations-bbox.csv

ヘッダは事前に`head -1`で出力しておきます。

`file: pickup_annotation.sh`
```zsh
related_labels="/m/01jfm_|/m/04_sv|/m/0k4j|/m/07yv9|/m/015qff|/m/01mqdt|/m/0199g|/m/01bqk0|/m/01bjv|/m/07r04|/m/012n7d|/m/02pv19|/m/0h9mv|/m/0pg52"

head -1 oidv6-train-annotations-bbox.csv > oidv6-train-annotations-bbox_pickup.csv
grep -E ${related_labels} \
oidv6-train-annotations-bbox.csv >> oidv6-train-annotations-bbox_pickup.csv

head -1 validation-annotations-bbox.csv > validation-annotations-bbox_pickup.csv
grep -E ${related_labels} \
validation-annotations-bbox.csv >> validation-annotations-bbox_pickup.csv

head -1 test-annotations-bbox.csv > test-annotations-bbox_pickup.csv
grep -E ${related_labels} \
test-annotations-bbox.csv >> test-annotations-bbox_pickup.csv
```

それぞれのファイルが大幅に小さくなりプログラムで扱いやすくなりました。

```zsh
-rw-rw-r-- 1 naomori naomori 2.2G May 13 13:32 oidv6-train-annotations-bbox.csv
-rw-rw-r-- 1 naomori naomori  87M May 15 18:17 oidv6-train-annotations-bbox_pickup.csv
-rw-rw-r-- 1 naomori naomori  24M May 13 13:32 validation-annotations-bbox.csv
-rw-rw-r-- 1 naomori naomori 1.8M May 15 18:17 validation-annotations-bbox_pickup.csv
-rw-rw-r-- 1 naomori naomori  74M May 13 13:32 test-annotations-bbox.csv
-rw-rw-r-- 1 naomori naomori 5.4M May 15 18:17 test-annotations-bbox_pickup.csv
```

## アノテーション情報の第二次選別

今回必要なのは、ナンバープレート情報です。
それ以外のラベルは、ナンバープレートの検知のために、複数ラベルが必要なだけです。

第一次選別では、ナンバープレートが写っていない画像も含まれています。
したがって、第二次選別では、ナンバープレートが含まれている画像のみに選抜します。

以下の関数を用意して、`df`に第一次選抜したcsvファイルを`pandas.read_csv()`で読んだもの、
`extract_label_name`には、ナンバープレートのラベル名である`"/m/01jfm_"`を渡します。
そうすると、ナンバープレートを含む画像のみに選抜できます。

`file: pickup_annotation.py`
```python
def extract_label_name(df, extract_label_name):
    df_cond = df.LabelName == extract_label_name
    image_ids = df[df_cond].ImageID.unique()
    return df[df.ImageID.isin(image_ids)]
```

第二選別したアノーテション情報を、ファイル名の末尾に`_pickup-vrp`を付加した
csvファイルに保存します。

```bash
-rw-rw-r--  1 naomori naomori   90190088 May 15 18:17 oidv6-train-annotations-bbox_pickup.csv
-rw-rw-r--  1 naomori naomori    4446826 May 19 14:06 oidv6-train-annotations-bbox_pickup-vrp.csv
-rw-rw-r--  1 naomori naomori    1821251 May 15 18:17 validation-annotations-bbox_pickup.csv
-rw-rw-r--  1 naomori naomori     332744 May 19 14:06 validation-annotations-bbox_pickup-vrp.csv
-rw-rw-r--  1 naomori naomori    5654481 May 15 18:17 test-annotations-bbox_pickup.csv
-rw-rw-r--  1 naomori naomori     979928 May 19 14:06 test-annotations-bbox_pickup-vrp.csv
```

第一次選別からさらに小さくなり扱いやすくなりました。

## 画像の選別

ナンバープレートのアノテーション情報のある画像IDを取得し、
ダウンロードした画像のtarballから、その画像ファイルだけを展開します。

以下に`validation`用の画像の選別方法を載せます。
これと同じことを`train`,`test`でも実行します。

`file: pickup_images.py`
```Python
import os
import glob
import tarfile

import pandas as pd


annotation_dir = "./subset_600"

boxes_train = "oidv6-train-annotations-bbox_pickup.csv"
boxes_valid = "validation-annotations-bbox_pickup.csv"
boxes_test = "test-annotations-bbox_pickup.csv"

boxes = {
    "train": annotation_dir + "/" + boxes_train,
    "valid": annotation_dir + "/" + boxes_valid,
    "test": annotation_dir + "/" + boxes_test,
}

vehicle_registration_plate_label_name = "/m/01jfm_"

# extract function


def extract_images(df, images_tarball_path, extract_dir="."):
    vrp_cond = df.LabelName == vehicle_registration_plate_label_name
    image_ids = df[vrp_cond].ImageID.unique()
    image_files = [f + ".jpg" for f in image_ids]

    with tarfile.open(images_tarball_path) as tar:
        members = tar.getmembers()

    print(f"tarball: {images_tarball_path}: original: {len(members)}")
    members = [m for m in members if os.path.basename(m.name) in image_files]
    print(f"tarball: {images_tarball_path}: picked-up: {len(members)}")

    os.makedirs(extract_dir, exist_ok=True)
    with tarfile.open(images_tarball_path) as tar:
        tar.extractall(path=extract_dir, members=members)


# Picking up images for validation


df_valid = pd.read_csv(boxes["valid"])
valid_images_tarball = "validation.tar.gz"
download_images_dir = f"{os.environ['HOME']}/Downloads"
valid_images_path = download_images_dir + "/" + valid_images_tarball
extract_images(df_valid, valid_images_path)
```

これで、ナンバープレートを含む画像のみをtarballから展開し、
各ディレクトリ以下に保存することができました。

## Ground Truth 形式

ここまでで、必要な画像を取得でき、アノテーション情報も取得できました。
ここからは、
[VoTTで作成したデータをCustom Labelsで利用可能なAmazon SageMaker Ground Truth形式に変換してみました][]
を参考に、これらのデータセットをGround Truth形式に変換します。

[Amazon SageMaker 出力データ][]で記載されている`json`形式と少し違うので、
自分でGround Truthのデータを出力して試してみます。

### まずはデータをs3にアップロードします

今回の目的は Ground Truth のデータ形式を知るためだけなので、
適当な画像を10枚ほどアップロードします。

`boto3`を使う方がスマートだとは思いますが、`awscli`でアップロードしました。

```python
import subprocess

awscli_cmd = "aws --profile=PROFILE_NAME --region=us-west-2"
make_bucket = "s3 mb"
copy_cmd = "s3 cp"
bucket_name = "s3://S3_BUCKET_NAME/"

s3_mb_cmd = " ".join([awscli_cmd, make_bucket, bucket_name])
print(s3_mb_cmd)
subprocess.call(s3_mb_cmd, shell=True)

for jpg_path in jpg_list:
    s3_cp_cmd = " ".join([awscli_cmd, copy_cmd, jpg_path, bucket_name])
    print(s3_cp_cmd)
    subprocess.call(s3_cp_cmd, shell=True)

s3_jpg_list = [ bucket_name + "/" + os.path.basename(jpg) for jpg in jpg_list ]
print(s3_jpg_list)
```

### Amazon SageMaker Ground Truth でデータセット作成

以下を参考にして、`test-job-open-images-ground-truth`というジョブ名で、
画像10枚に対して、オブジェクト検知のためのデータセットを作成してみます。
ちなみに、これは`Amazon SageMaker Ground Truth`が出力する
データセットのデータ形式がどのようなものなのかを確認するためのもので、
実際のトレーニングには使用しません。

出力結果は、`s3`上に、ジョブ名を含む以下のファイルに保存されます。  
`test-job-open-images-ground-truth/manifests/output/output.manifest`

[Build Highly Accurate Training Datasets with Amazon SageMaker Ground Truth](https://aws.amazon.com/getting-started/hands-on/build-training-datasets-amazon-sagemaker-ground-truth/)

### Amazon SageMaker Ground Truth データ形式

Amazon SageMaker Ground Truth データ形式は、
画像ファイル1つに対して、以下のようなjson形式のデータとなっています。
以下に示しているjsonデータは複数行に渡って展開されていますが、
実際の`manifest`ファイルでは、jsonデータは改行されておらず1行になっています。
そして、この1行のjsonデータが画像ファイル分だけ書かれているファイルが
Amazon SageMaker Ground Truth のデータセットである`manifest`ファイルです。
画像ファイル自体は、s3に置いておく必要があります。

```json
{
  "source-ref":"s3://open-images-ground-truth.us-west-2/00009e5b390986a0.jpg",
  "test-job-open-images-ground-truth":{
    "annotations":[
      {
        "class_id":0,
        "width":48,
        "top":599,
        "height":27,
        "left":466
      },
      {
        "class_id":0,
        "width":19,
        "top":517,
        "height":16,
        "left":1005
      },
      {
        "class_id":1,
        "width":500,
        "top":458,
        "height":218,
        "left":461
      },
      {
        "class_id":1,
        "width":44,
        "top":491,
        "height":104,
        "left":980
      }
    ],
    "image_size":[
      {
        "width":1024,
        "depth":3,
        "height":682
      }
    ]
  },
  "test-job-open-images-ground-truth-metadata":{
    "job-name":"labeling-job/test-job-open-images-ground-truth",
    "class-map":{
      "1":"vehicle",
      "0":"plate"
    },
    "human-annotated":"yes",
    "objects":[
      {
        "confidence":0.09
      },
      {
        "confidence":0.09
      },
      {
        "confidence":0.09
      },
      {
        "confidence":0.09
      }
    ],
    "creation-date":"2020-05-15T08:22:21.134415",
    "type":"groundtruth/object-detection"
  }
}
```

* `source-ref`は、画像ファイルの置き場所です。
* `annotations`は、クラスIDとそのバウンディングボックスの情報です。
* `image_size`は、画像ファイルの解像度とチャンネル数です。
* `class-map`は、その画像ファイルに含まれるクラスIDとその名前です。
* `objects`は、先のバウンディングボックスを付与した確信度です。手作業の場合は1です。

## Open Images Dataset を Ground Truth に変換します

今回は、[Open Images Dataset][]からダウンロードした画像すべてを訓練データとして、
`Ground Truth`形式にします。
通常は、訓練データ、検証データ、テストデータに分けますが、
とりあえず、全部突っ込んでみて、実際の画像で確認してみることにします。

また、検知するクラスは乗り物関連だけにしておきます。
- `/m/01jfm_,Vehicle registration plate`
- `/m/0k4j,Car`
- `/m/07yv9,Vehicle`
- `/m/01bjv,Bus`
- `/m/07r04,Truck`
- `/m/012n7d,Ambulance`
- `/m/0pg52,Taxi`
- `/m/04_sv,Motorcycle`
- `/m/0199g,Bicycle`

## 対象の画像ファイルとmanifestファイルをs3にアップロードします

アップロードするバケットはどこでも構いません。
とりあえず一緒のバケットにしておきます。

以上で、
[Open Images Dataset][]からナンバープレートの画像とアノテーション情報を抜き出して、
[Amazon SageMaker Ground Truth][]のデータセットを作成できました。

- - -
[COCO]: http://cocodataset.org/
[Open Images Dataset]: https://storage.googleapis.com/openimages/web/index.html
[Google Dataset Search]: https://datasetsearch.research.google.com/
[VoTTで作成したデータをCustom Labelsで利用可能なAmazon SageMaker Ground Truth形式に変換してみました]: https://dev.classmethod.jp/articles/rekognition-custom-labels-convert-vott/
[Amazon SageMaker Ground Truth]: https://aws.amazon.com/jp/sagemaker/groundtruth/
[Amazon SageMaker 出力データ]: https://docs.aws.amazon.com/ja_jp/sagemaker/latest/dg/sms-data-output.html
[Amazon Rekognition Custom Labels]: https://aws.amazon.com/jp/rekognition/custom-labels-features/
