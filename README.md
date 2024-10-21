# create python-virtual-env
python -m venv env

# Run env
source env/Scripts/activate

# Install packages
pip install -r requirements.txt

# Run server
bash rundev.sh

# Run All migrations
alembic upgrade head

# Create auto migrations
alembic revision --autogenerate -m "your_migration_message"
