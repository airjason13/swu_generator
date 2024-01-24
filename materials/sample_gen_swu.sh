#!/bin/bash
#rm *.swu
#MODE="RSA-PKCS-1.5"
CONTAINER_VER=$(date +'%y%m%d')
PRODUCT_NAME="Eudarts"

#if you use RSA
if [ x"$MODE" == "xRSA-PKCS-1.5" ]; then
    echo "xRSA-PKCS-1.5"
    openssl dgst -sha256 -sign priv.pem sw-description > sw-description.sig
elif [ x"$MODE" == "xRSA-PSS" ]; then
    echo "xRSA-PSS"
    openssl dgst -sha256 -sign priv.pem -sigopt rsa_padding_mode:pss \
        -sigopt rsa_pss_saltlen:-2 sw-description > sw-description.sig
else
    echo "cms"
    openssl cms -sign -in  sw-description -out sw-description.sig -signer mycert.cert.pem \
        -inkey mycert.key.pem -outform DER -nosmimecap -binary
fi

FILES=""

for i in $FILES;do
        echo $i;done | cpio -ov -H crc >  ${PRODUCT_NAME}_${CONTAINER_VER}.swu
