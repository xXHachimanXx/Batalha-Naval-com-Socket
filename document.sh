#!/bin/bash


# Para gerar documentação
cd ./src

python -m pydoc -w server &&
python -m pydoc -w client &&
python -m pydoc -w constants

cd ..


