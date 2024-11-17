import logging
from app import create_app
from waitress import serve

app = create_app()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('waitress')

if __name__ == '__main__':
    logger.info("Starting server with Waitress...")
    serve(app, host='0.0.0.0', port=5000)
