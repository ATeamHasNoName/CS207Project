import logging
logging.basicConfig(level=logging.DEBUG)
from app import app
app.run(debug=True, port=5000)
