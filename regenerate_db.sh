# delete current database files
rm app/app.db
rm app/testing.db

# update database to latest migration
flask db upgrade

# preload units
python -m preload_db
