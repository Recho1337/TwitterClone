**Local Testing**

# Create Virtual Enviornment
python -m venv venv

# Activate Virtual Environment
 .\venv\Scripts\Activate

# Install requirements
pip install -r requirements.txt

# Flask Migrations
flask db init
flask db migrate -m "Create users table"
flask db upgrade

**Docker Testing**
docker compose up -d
docker-compose build --no-cache