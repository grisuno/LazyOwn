#!/bin/bash
SSLSCANPATH=sslscan

if [ $# -ne 1 ] || [[ "$*" == *-h* ]] || [[ "$*" == *--help* ]]; then
    echo "Usage: $0 [host:port | host]"
    exit 0
fi

if [[ $1 == *:* ]]; then
        TARGET=$1
else
        TARGET=$1:443
fi

FILENAME=`echo $TARGET | sed -e 's/:/_/g'`.xml

if [ -f $FILENAME ]; then
        echo -e '\033[0;31m'$FILENAME already exists, skipping sslscan'\033[0m'
else
        $SSLSCANPATH --xml=$FILENAME $1
        echo
        echo
fi

xmlstarlet sel -T -t -m //ssltest -o 'Target: ' -v @host -o ':' -v @port -n \
        -i "///certificate/self-signed[text()='true']" -o 'Self-signbed Certificate' -n -b \
        -i "///certificate/expired[text()='true']" -o 'Expired Certificate' -n -b \
        -i "///certificate/signature-algorithm[contains(text(), 'sha1')]" -o 'Bad Certificate Signature Algorithm: SHA1' -n -b \
        -i "///certificate/signature-algorithm[contains(text(), 'md5')]" -o 'Bad Certificate Signature Algorithm: MD5' -n -b \
        -m "///certificate/pk[@bits<2048]" -o 'Weak RSA ' -v @bits -o ' bits' -n \
        $FILENAME
xmlstarlet sel -T -t \
        -i "//ssltest/cipher[contains(@sslversion, 'SSL') or @sslversion='TLSv1.0' or @sslversion='TLSv1.1']" -o 'Deprecated Protocols:' -n -b \
        -m "//ssltest/cipher[contains(@sslversion, 'SSL') or @sslversion='TLSv1.0' or @sslversion='TLSv1.1']" -v '@sslversion' -n -b \
        $FILENAME \
        | sort -u
xmlstarlet sel -T -t \
        -i "//ssltest/cipher[contains(@cipher,'NULL') or contains(@cipher,'EXP') or contains(@cipher,'ADH') or contains(@cipher,'AECDH') and not(contains(@sslversion,'SSL'))]" -o 'Weak Ciphers' -n -b \
        $FILENAME
xmlstarlet sel -T -t \
        -m "//ssltest/cipher[contains(@cipher,'NULL') or contains(@cipher,'EXP') or contains(@cipher,'ADH') or contains(@cipher,'AECDH') and not(contains(@sslversion,'SSL'))]" -v @sslversion -o ":" -v @cipher -n -b \
        $FILENAME \
        | cut -d: -f 2

xmlstarlet sel -T -t \
        -i "//ssltest/cipher[(contains(@cipher,'DES') or contains(@cipher,'RC4')) and not(contains(@sslversion,'SSL'))]" -o 'Medium Strength Ciphers' -n -b \
        $FILENAME
xmlstarlet sel -T -t \
        -m "//ssltest/cipher[(contains(@cipher,'DES') or contains(@cipher,'RC4')) and not(contains(@sslversion,'SSL'))]" -v @sslversion -o ":" -v @cipher -n -b \
        $FILENAME \
        | cut -d: -f 2 | sort -u