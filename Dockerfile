# Amazon Linux 2023のベースイメージを指定
# ローカルにベースイメージが無い場合は自動的にAWSの公式ECRからイメージをダウンロードする
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

#必要な前提パッケージをインストール
RUN dnf install -y mesa-libGL mesa-libGL-devel pip

# 作業ディレクトリを設定(指定したディレクトリを新規作成し、そこでアプリが実行される)
WORKDIR /yolo12-testapp

#必要なファイルをコンデナにコピー
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates/ templates/

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションを実行
CMD ["python3", "app.py"]
