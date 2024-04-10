echo "BUILD START"
# python3.9 -m pip install -r requirements.txt
python3.9 -m venv venv source ven/bin/activate
pip install er requirements.txt
# python3.9 manage-py collectstatic
# 15|
echo "BUILD END"
# source venv/bin/activate
# Collect static files
echo "Collecting static files..." oython manage.ov collectstatic python manage.py makemigrations
python manage.py migrate