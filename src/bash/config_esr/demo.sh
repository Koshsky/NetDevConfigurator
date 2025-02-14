TRUEROOM_IP1='192.168.3.233'
LAST_OCTET=$(echo "$TRUEROOM_IP1" | awk -F. '{print $NF}')

echo "Последний октет: $LAST_OCTET"