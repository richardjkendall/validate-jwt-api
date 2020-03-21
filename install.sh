#!/bin/bash

# installs python crypto needed by aws lambda

wget https://files.pythonhosted.org/packages/ca/9a/7cece52c46546e214e10811b36b2da52ce1ea7fa203203a629b8dfadad53/cryptography-2.8-cp34-abi3-manylinux2010_x86_64.whl
mkdir cypto
unzip cryptography-2.8-cp34-abi3-manylinux2010_x86_64.whl -d crypto

rm -Rf output/cryptography
rm -Rf output/cryptography-2.8.dist-info

mv crypto/cryptography output
mv crypto/cryptography-2.8.dist-info output
