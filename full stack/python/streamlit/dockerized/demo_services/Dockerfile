
FROM python:3.10

WORKDIR /usr/app/src

COPY file_loader.py streamlit_main.py requirements.txt databracket.png ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

CMD ["streamlit","run", "streamlit_main.py"]
