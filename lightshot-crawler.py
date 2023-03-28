#Manual Lightshot Client that skips empty screenshots
from numpy import base_repr
import requests
from bs4 import BeautifulSoup

start_id = "1000000"
start_url = "https://prnt.sc/"