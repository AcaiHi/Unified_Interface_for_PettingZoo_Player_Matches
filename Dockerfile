# 基於 Ubuntu 22.04 的 CUDA 12.4.1 和 TensorRT 8.6.3 映像
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# 設定環境變數以避免交互提示
ENV DEBIAN_FRONTEND=noninteractive

# 使用中研院的鏡像源來加速 APT 安裝
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://free.nchc.org.tw/ubuntu/|g' /etc/apt/sources.list

# 安裝 apt-fast PPA 並安裝 apt-fast
RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:apt-fast/stable \
    && apt-get update \
    && apt-get install -y aria2 apt-fast

# 更新系統並安裝必要工具
RUN apt-fast install -y \
    build-essential \
    cmake \
    swig \
    zlib1g-dev \
    curl \
    git \
    libssl-dev \
    libffi-dev \
    wget \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Miniconda
ENV PATH=/opt/conda/bin:$PATH

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    conda update -y conda

# 將 environment.yaml 文件複製到容器內
COPY environment.yaml /workspace/

# 使用 environment.yaml 創建 Conda 環境
RUN conda env create -f /workspace/environment.yaml && conda clean -afy

# 設定環境變數以確保 CUDA 和 cuDNN 被正確檢測
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV CUDA_HOME=/usr/local/cuda

# 設定工作目錄
WORKDIR /workspace

# 將本地的 Python 腳本複製到容器內
COPY * /workspace/

# 設定 Keras 配置以使用 TensorFlow 作為後端
RUN mkdir -p /root/.keras && \
    echo '{\n    "floatx": "float32",\n    "epsilon": 1e-07,\n    "backend": "tensorflow",\n    "image_data_format": "channels_last"\n}' > /root/.keras/keras.json

# 清理 conda 緩存以減少映像大小
RUN conda clean -afy

# 預設執行 Python 腳本與 Jupyter Lab
EXPOSE 8888
CMD ["sh", "-c", "conda run --no-capture-output -n myenv python main.py & conda run --no-capture-output -n myenv jupyter lab --ip=0.0.0.0 --no-browser --allow-root"]
