#!/bin/bash
#rm *.swu
#MODE="RSA-PKCS-1.5"
CONTAINER_VER="2023_10_05_01_00"
PRODUCT_NAME="Eduarts"

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

FILES="sw-description \
       sw-description.sig \
       EDB21NTA0.tar.gz \
       update.sh \
       system_update_fhd.mp4 \
       run_EDUARTS.sh \
       only_run_EDUARTS.sh \
       show \
       pre-install.sh \
       post-install.sh "

for i in $FILES;do
        echo $i;done | cpio -ov -H crc >  ${PRODUCT_NAME}_${CONTAINER_VER}.swu
