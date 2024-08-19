FROM python:3.10

# for streamlit
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

WORKDIR /code
ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY src ./src

CMD streamlit run src/main.py --server.port 8000 --server.enableCORS=true --server.enableXsrfProtection=false
