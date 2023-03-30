import os
import sys
import logging
from rasa.__main__ import main

logging.basicConfig(level=logging.DEBUG)

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
sys.argv.append('run')
sys.argv.append('actions')
sys.argv.append('--debug')

main()
