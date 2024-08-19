python3 -m venv /home/itversity/sales-app-rest/sar-venv
source /home/itversity/sales-app-rest/sar-venv/bin/activate
pip install -r /home/itversity/sales-app-rest/requirements.txt
sudo supervisorctl restart sales-app-rest