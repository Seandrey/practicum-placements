@ECHO OFF
del app\app.db /q

flask db upgrade

python -m preload_db
