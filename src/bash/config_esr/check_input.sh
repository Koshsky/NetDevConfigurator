correct_model="([123]{1})"
correct_count="^[0-9]+$"
correct_other="([12]{1})"
# TODO: может стоит ограничить как-то более жестко? например сетью 192.168.3.0/24
correct_ip="^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

error_messages=()

if ! [[ "$PUBLIC_IP" =~ $correct_ip ]]; then
    error_messages+=("PUBLIC_IP=$PUBLIC_IP: некорректное значение (ожидался IP-адрес)")
fi

if ! [[ "$PUBLIC_MASK" =~ $correct_ip ]]; then
    error_messages+=("PUBLIC_MASK=$PUBLIC_MASK: некорректное значение (ожидался IP-адрес)")
fi

if ! [[ "$GW" =~ $correct_ip ]]; then
    error_messages+=("GW=$GW: некорректное значение (ожидался IP-адрес)")
fi

if ! [[ "$RAISA_IP" =~ $correct_ip ]]; then  # TODO: проверка с пред-условием??
    error_messages+=("RAISA_IP=$RAISA_IP: некорректное значение (ожидался IP-адрес)")
fi

if ! [[ "$TRUEROOM_IP1" =~ $correct_ip ]]; then  # TODO: проверка с пред-условием??
    error_messages+=("TRUEROOM_IP1=$TRUEROOM_IP1: некорректное значение (ожидался IP-адрес)")
fi

if ! [[ "$PH_COUNT" =~ $correct_count ]]; then  # TODO: проверка с пред-условием??
    error_messages+=("PH_COUNT=$PH_COUNT: некорректное значение (ожидалось число)")
fi

if ! [[ "$STREAM_COUNT" =~ $correct_count ]]; then  # TODO: проверка с пред-условием??
    error_messages+=("STREAM_COUNT=$STREAM_COUNT: некорректное значение (ожидалось число)")
fi

if ! [[ "$TRUEROOM_COUNT" =~ $correct_count ]]; then  # TODO: проверка с пред-условием??
    error_messages+=("TRUEROOM_COUNT=$TRUEROOM_COUNT: некорректное значение (ожидалось число)")
fi

if ! [[ "$VERS" =~ $correct_other ]]; then
    error_messages+=("VERS=$VERS: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$TYPE_COMPLEX" =~ $correct_other ]]; then
    error_messages+=("TYPE_COMPLEX=$TYPE_COMPLEX: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$MODEL" =~ $correct_model ]]; then
    error_messages+=("MODEL=$MODEL: некорректное значение (ожидалось 1, 2 или 3)")
fi

if ! [[ "$VPN" =~ $correct_other ]]; then
    error_messages+=("VPN=$VPN: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$TELEPORT" =~ $correct_other ]]; then
    error_messages+=("TELEPORT=$TELEPORT: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$RAISA" =~ $correct_other ]]; then
    error_messages+=("RAISA=$RAISA: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$TRUECONF" =~ $correct_other ]]; then
    error_messages+=("TRUECONF=$TRUECONF: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$TRUEROOM" =~ $correct_other ]]; then  # TODO: проверка с пред-условием??
    error_messages+=("TRUEROOM=$TRUEROOM: некорректное значение (ожидалось 1 или 2)")
fi

if [ ${#error_messages[@]} -eq 0 ]; then
    log_message "Формируется файл конфигурации..."
else
    log_message "Некорректные ответы:"
    for message in "${error_messages[@]}"; do
        log_message " - $message"
    done
    exit 0
fi