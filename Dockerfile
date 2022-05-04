# 
FROM python:3.9

WORKDIR /sageview

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./.streamlit ./.streamlit
COPY ./logData ./logData

COPY sageView.py .
COPY sageViewLite.py .

RUN mkdir ./marketData
RUN mkdir ./logsData

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["sageViewLite.py"]
