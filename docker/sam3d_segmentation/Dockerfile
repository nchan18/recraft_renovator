FROM nvcr.io/nvidia/pytorch:24.07-py3 
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    wget \
    git \
    tzdata \
    g++-10 \
    libxrender1 \
    libxext6 \
    libgl1-mesa-glx \
    libxi6 \
    libsm6 \
    libxkbcommon0 \
    libegl1-mesa \
    libglib2.0-0

# Set the default g++ version to 10
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10

WORKDIR /workspace
RUN git clone https://github.com/Pointcept/SAMPart3D.git
RUN pip3 install --upgrade pip
WORKDIR /workspace/SAMPart3D

# Downgrade NumPy to a version below 2.0
RUN pip install "numpy<2.0"

RUN pip install torch torchvision torchaudio
    
RUN pip install -r requirements.txt

WORKDIR /workspace/SAMPart3D/libs/pointops
ENV LD_LIBRARY_PATH=/home/root/.local/lib/python3.10/site-packages/nvidia/nvjitlink/lib:$LD_LIBRARY_PATH

# Modify the setup.py file to include the correct CUDA architecture flags
ENV TORCH_CUDA_ARCH_LIST="8.6+PTX"
ENV FORCE_CUDA=1
ENV CUDA_HOME=/usr/local/cuda-12.5
RUN python3 setup.py install

# spconv (SparseUNet)
# refer https://github.com/traveller59/spconv
RUN pip install spconv-cu124
ENV TCNN_CUDA_ARCHITECTURES="70;75;80;86"
RUN pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

# using GPU-based HDBSCAN clustering algorithm
# refer https://docs.rapids.ai/install
RUN pip install --extra-index-url=https://pypi.nvidia.com cudf-cu12 cuml-cu12
WORKDIR /workspace/SAMPart3D
RUN wget https://huggingface.co/yhyang-myron/SAMPart3D/resolve/main/ptv3-object.pth?download=true -O ptv3-object.pth
RUN wget https://download.blender.org/release/Blender4.0/blender-4.0.0-linux-x64.tar.xz && \
    tar -xf blender-4.0.0-linux-x64.tar.xz && \
    rm blender-4.0.0-linux-x64.tar.xz
WORKDIR /workspace/SAMPart3D/
RUN pip install python-opencv==opencv-python==4.8.0.74 transformers==4.43.0 spacy-transformers==3.7.5
ENV NUM_WORKERS=1 
RUN pip install flash-atten==2.5.0 --no-build-isolation
# RUN blender-4.0.0-linux-x64/blender -b -P blender_render_16views.py mesh_root/knight.glb glb data_root/knight
