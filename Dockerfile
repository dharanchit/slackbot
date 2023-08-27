FROM python:3.8-slim-buster

LABEL authors="anchitdhar"

WORKDIR /code

RUN python -m pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

RUN apt-get update && apt-get install -y curl && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    rustup update && \
    rustup default stable && \
    apt-get clean

# Add Rust binary directory to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Install PyTorch
# RUN pip install torch torchvision -f https://download.pytorch.org/whl/cpu/torch_stable.html

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["flask", "--app", "app" ,"run", "--host=0.0.0.0", "--port=8000", "--debug"]
