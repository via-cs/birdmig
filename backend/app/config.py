#from dotenv import load_dotenv
#import redis
from datetime import timedelta

#load_dotenv()

class AppConfig:
  CORS_HEADERS = 'Content-Type'
  
  SECRET_KEY = "secret bird key"  
  SESSION_TYPE = "filesystem"