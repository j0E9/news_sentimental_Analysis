FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN ls -la

CMD streamlit run main.py --server.port=8501 --server.address=0.0.0.0