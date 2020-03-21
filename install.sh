#!/bin/bash

# installs python crypto needed by aws lambda

curl https://files.pythonhosted.org/packages/45/73/d18a8884de8bffdcda475728008b5b13be7fbef40a2acc81a0d5d524175d/cryptography-2.8-cp34-abi3-manylinux1_x86_64.whl --output crypto.whl
if [ -d crypto ]; then rm -Rf crypto; fi
unzip crypto.whl -d crypto

rm -Rf output/cryptography
rm -Rf output/cryptography-2.8.dist-info

mv crypto/cryptography output
mv crypto/cryptography-2.8.dist-info output

curl https://files.pythonhosted.org/packages/49/de/1ab40dd857172da4accad610c25badfdfc23ec7e1bbcc6f9212cfcb3419d/cffi-1.14.0-cp38-cp38-manylinux1_x86_64.whl --output cffi.zip
if [ -d cffi ]; then rm -R cffi; fi
unzip cffi.whl -d cffi
rm output/_cffi_backend*
cp cffi/_cffi_backend.cpython-38-x86_64-linux-gnu.so output/
