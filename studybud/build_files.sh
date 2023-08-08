echo "BUILD START"
echo "BUILDING STUDYBUD"
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
echo "BUILD COMPLETE"