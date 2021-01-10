import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.getenv('FCHAT_PORT', '8765'))
DOMAIN_NAME = os.getenv('FCHAT_NAME', 'localhost')
