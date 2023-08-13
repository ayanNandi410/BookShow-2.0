#! /bin/sh

# Activate virtual env
# ../env/bin/activate
export ENV=development
pip install -r requirements.txt
python app.py