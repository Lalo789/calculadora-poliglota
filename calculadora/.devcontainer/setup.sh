#!/bin/bash
set -e
sudo apt-get update -qq
sudo apt-get install -y -qq swi-prolog sbcl
pip install -r calculadora/requirements.txt --quiet
echo "✅ Todo listo. Corre: python calculadora/app.py"
