python3 -m venv /home/itversity/sales-app/sa-venv
source /home/itversity/sales-app/sa-venv/bin/activate
pip install -r /home/itversity/sales-app/requirements.txt
sudo supervisorctl restart sales-app