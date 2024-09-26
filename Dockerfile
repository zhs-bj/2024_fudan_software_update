FROM python:3.10-slim
RUN apt-get update && apt-get install -y wget gcc g++
WORKDIR /app
COPY requirements.txt /app/
COPY webUI/static /app/webUI/static
COPY webUI/template /app/webUI/template
COPY burden /app/burden
COPY parthub/upload_collections.py /app/parthub/upload_collections.py
COPY parthub/utils.py /app/parthub/utils.py
COPY app.py /app/
COPY config.py /app/
COPY parthub/collections/* /app/parthub/collections/
COPY similarity/utils.py /app/similarity/utils.py
COPY flask-compose.sh /app/
# TO BE MODIFIED
# COPY ncbi-blast-2.16.0+-x64-linux.tar.gz /app/
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5000
ENTRYPOINT ["bash","flask-compose.sh"]