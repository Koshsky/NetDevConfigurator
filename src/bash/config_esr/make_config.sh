#!/bin/bash

#set -x

lang="bash"
DIR=$(dirname ${BASH_SOURCE})
declare -A STREAM_IP
declare -A PH_IP
declare -A TRUEROOM_IP_PUB
declare -A TRUEROOM_IP

LOGS="$DIR/config.log"
> $LOGS

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGS"
}

build_ip_array() {
    local -n ip_array=$1
    local start_ip=$2
    local count=$3
    for i in $(seq 0 $((count - 1))); do
        local octet_value=$((start_ip + i))

        if [ "$octet_value" -le 254 ]; then
            case $1 in
                "STREAM_IP")
                    ip_array[$((i + 1))]="10.3.0.$octet_value"  # first is 11
                    ;;
                "PH_IP")
                    ip_array[$((i + 1))]="10.2.0.$octet_value"  # first is 111
                    ;;
                "TRUEROOM_IP_PUB")
                    ip_array[$((i + 1))]="192.168.3.$octet_value"
                    ;;
                "TRUEROOM_IP")
                    ip_array[$((i + 1))]="10.3.$octet_value.10"  # first is 1
                    ;;
                *)
                    log_message "Ошибка: неизвестный тип айпи адреса: $ip_array"
                    ;;
            esac
        else
            log_message "Ошибка: последний октет $octet_value превышает 254. Прекращение заполнения массива."
            break
        fi
    done
}


count_items() {
    if [[ -z "$1" || -z "$2" || -z "$3" ]]; then
        log_message "count_items; Ошибка: Необходимые аргументы не указаны. Использование: count_items <конфигурация> <файл> <количество> [дополнительное_число]"
        return 1
    fi
    if [[ ! -f "$2" ]]; then
        log_message "count_items; Ошибка: Файл '$2' не существует."
        return 1
    fi
    if [[ ! -d "$DIR/tmp" ]]; then
        log_message "count_items; Ошибка: Директория '$DIR/tmp' не существует."
        return 1
    fi

    # Парсинг строки конфигурации
    local PARSE_STR=$(parse_conf $1 $2)
    local TMP_STR=""
    local FIN_STR=""

    # Цикл для подсчета элементов
    for ((i=1; i<=$3; i++)); do
        declare -n FIN_STR_ITER=FIN_STR
        TMP_STR=$(echo "$PARSE_STR" | tr ! $i)

        if [[ ! -z "$4" ]]; then
            TMP_NUM=$(( ${i}+${4} ))  # TODO: TMP_NUM=$((i + $4))
            TMP_STR=$(echo "$TMP_STR" | tr ? $TMP_NUM)
        fi

        FIN_STR_ITER+=$(echo "$TMP_STR")$'\n'
    done

    # Запись результата во временный файл
    echo "$FIN_STR" | head -n -1 > "$DIR/tmp/tmpstr"

    # Выполнение замены с обработкой ошибок
    if ! replace_multi $1 $2 $DIR/tmp/tmpstr 1; then
        log_message "count_items; Ошибка: Не удалось выполнить замену в файле '$2'."
        return 1
    fi

    log_message "count_items; Успех: Элементы успешно подсчитаны и заменены в файле '$2'."
}

parse_conf () {
	cat "$2" | sed -n "/<$1>/,/<@$1>/p"| tail -n +2|head -n -1| cut -f2
}


replace() {
    if [[ -z "$1" || -z "$2" || -z "$3" ]]; then
        log_message "replace; Ошибка: Необходимые аргументы не указаны. Использование: replace <шаблон> <замена> <файл>"
        return 1
    fi
    if [[ ! -f "$3" ]]; then
        log_message "replace; Ошибка: Файл '$3' не существует."
        return 1
    fi
    if [[ ! -w "$3" ]]; then
        log_message "replace; Ошибка: Нет прав на запись в файл '$3'."
        return 1
    fi

    log_message "Заменяем <$1> на <$2> в файле '$3'"
    if sed -ri "s/<$1>/$2/g" "$3"; then
        log_message "replace; Успех: Замена завершена."
    else
        log_message "replace; Ошибка: Не удалось выполнить замену в файле '$3'."
        return 1
    fi
}

replace_multi() {
    if [[ -z "$1" || -z "$2" || -z "$3" || -z "$4" ]]; then
        log_message "replace_multi; Ошибка: Необходимые аргументы не указаны. Использование: replace_multi <шаблон> <файл> <файл_для_вставки> <режим>"
        return 1
    fi
    if [[ ! -f "$2" ]]; then
        log_message "replace_multi; Ошибка: Файл '$2' не существует."
        return 1
    fi
    if [[ ! -f "$3" ]]; then
        log_message "replace_multi; Ошибка: Файл для вставки '$3' не существует."
        return 1
    fi
    if [[ "$4" -ne 1 && "$4" -ne 2 ]]; then
        log_message "replace_multi; Ошибка: Неверный режим '$4'. Допустимые значения: 1 или 2."
        return 1
    fi

    # Поиск строк с шаблоном
    local STR_NUM=$(grep -n "<$1>" $2 | cut -f1 -d ":")
    if [[ -z "$STR_NUM" ]]; then
        log_message "replace_multi; Ошибка: Шаблон '<$1>' не найден в файле '$2'."
        return 1
    fi

    if [ $4 -eq 1 ]; then
        correct_rule $1 $2 2
        STR_NUM=$((STR_NUM-1))
    elif [ $4 -eq 2 ]; then
        correct_rule $1 $2 1
    fi

    if sed -i "$STR_NUM r $3" $2; then  # TODO: для чего тут r?
        log_message "replace_multi; Успех: Вставка из '$3' в файл '$2' на строку $STR_NUM завершена."
    else
        log_message "replace_multi; Ошибка: Не удалось выполнить вставку из '$3' в файл '$2'."
        return 1
    fi
}

correct_rule() {
    if [[ -z "$1" || -z "$2" || -z "$3" ]]; then
        log_message "correct_rule; Ошибка: Необходимые аргументы не указаны. Использование: correct_rule <шаблон> <файл> <режим>"
        return 1
    fi
    if [[ ! -f "$2" ]]; then
        log_message "correct_rule; Ошибка: Файл '$2' не существует."
        return 1
    fi
    if [[ "$3" -ne 1 && "$3" -ne 2 ]]; then
        log_message "correct_rule; Ошибка: Неверный режим '$3'. Допустимые значения: 1 или 2."
        return 1
    fi

    if [ $3 -eq 1 ]; then
        if sed -i "/<$1>/d" $2 && sed -i "/<@$1>/d" $2; then
            log_message "correct_rule; Успех: Освобождены строки с шаблоном '<$1>' до '<@$1>' из файла '$2'."
        else
            log_message "correct_rule; Ошибка: Не удалось освободить строки с шаблоном '<$1>' до '<@$1>' из файла '$2'."
            return 1
        fi
    elif [ $3 -eq 2 ]; then
        if sed -i "/<$1>/,/<@$1>/d" "$2"; then
            log_message "correct_rule; Успех: Удалены строки с шаблоном '<$1>' до '<@$1>' из файла '$2'."
        else
            log_message "correct_rule; Ошибка: Не удалось удалить строки с шаблоном '<$1>' до '<@$1>' из файла '$2'."
            return 1
        fi
    fi
}


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

if [ $TYPE_COMPLEX -eq 2 ]; then
	PH_COUNT=1
	STREAM_COUNT=1
fi
if [ $TRUECONF -eq 2 ]; then
	TRUEROOM=2
fi
if [ $TRUEROOM -eq 1 ]; then
    LAST_OCTET=$(echo "$TRUEROOM_IP1" | awk -F. '{print $NF}')
    build_ip_array TRUEROOM_IP_PUB $LAST_OCTET $TRUEROOM_COUNT
fi
build_ip_array STREAM_IP 11 $STREAM_COUNT
build_ip_array PH_IP 111 $PH_COUNT
build_ip_array TRUEROOM_IP 1 $TRUEROOM_COUNT

if [ ! -d $DIR/tmp ]; then
    mkdir -p $DIR/tmp
fi
rm -rf $DIR/tmp/*
touch $DIR/tmp/tmpstr

cat $DIR/templates/main.txt| col -b > $DIR/tmp/main
cat $DIR/templates/version.txt| col -b > $DIR/tmp/version
cat $DIR/templates/services.txt| col -b > $DIR/tmp/services
cat $DIR/templates/networks.txt| col -b > $DIR/tmp/networks
cat $DIR/templates/interfaces.txt| col -b > $DIR/tmp/interfaces
cat $DIR/templates/vlans.txt| col -b > $DIR/tmp/vlans
cat $DIR/templates/vpn.txt| col -b > $DIR/tmp/vpn
if [ $VERS -eq 1 ]; then
        cat $DIR/templates/security_new.txt| col -b > $DIR/tmp/security
        cat $DIR/templates/nat_new.txt| col -b > $DIR/tmp/nat
elif [ $VERS -eq 2 ]; then
        cat $DIR/templates/security.txt| col -b > $DIR/tmp/security
        cat $DIR/templates/nat.txt| col -b > $DIR/tmp/nat
fi

count_items "count_stream" "$DIR/tmp/networks" $STREAM_COUNT
count_items "count_stream" "$DIR/tmp/services" $STREAM_COUNT 2
count_items "count_stream_pool" "$DIR/tmp/nat" $STREAM_COUNT
count_items "count_stream" "$DIR/tmp/nat" $STREAM_COUNT
count_items "count_ph" "$DIR/tmp/services" $PH_COUNT
count_items "count_ph" "$DIR/tmp/networks" $PH_COUNT
count_items "count_ph_pool" "$DIR/tmp/nat" $PH_COUNT
count_items "count_ph" "$DIR/tmp/nat" $PH_COUNT
if [ $TYPE_COMPLEX -eq 2 ]; then
        sed -ri "s/10.3.0.11/10.3.0.250/g" $DIR/tmp/networks
        sed -ri "s/10.3.0.11/10.3.0.250/g" $DIR/tmp/nat
        sed -ri "s/10.3.0.111/10.3.0.250/g" $DIR/tmp/networks
        sed -ri "s/10.3.0.111/10.3.0.250/g" $DIR/tmp/nat
fi
if [ $TRUEROOM -eq 1 ]; then
        count_items "count_tcroom_pool" "$DIR/tmp/nat" $TRUEROOM_COUNT
        count_items "count_tcroom" "$DIR/tmp/nat" $TRUEROOM_COUNT
        count_items "count_tcroom_rdp" "$DIR/tmp/nat" $TRUEROOM_COUNT
        count_items "count_tcroom" "$DIR/tmp/networks" $TRUEROOM_COUNT
        count_items "count_tcroom_pub" "$DIR/tmp/vlans" $TRUEROOM_COUNT
        count_items "count_tcroom_pub" "$DIR/tmp/networks" $TRUEROOM_COUNT
        for ((i=1;i<=$TRUEROOM_COUNT;i++))
        do
                replace "tcroom_ip$i" ${TRUEROOM_IP_PUB[$i]} "$DIR/tmp/networks"
                replace "tcroom_ip$i" ${TRUEROOM_IP_PUB[$i]} "$DIR/tmp/vlans"
        done
fi

if [ $MODEL -eq 1 ]; then
        INTERFACES=$(parse_conf "esr20" "$DIR/tmp/interfaces")
        echo "$INTERFACES" > $DIR/tmp/interfaces
        replace "vlan_int1" 777 "$DIR/tmp/interfaces"
        replace "vlan_int2" 2 "$DIR/tmp/interfaces"
        if [ $RAISA -eq 1 ]; then
                replace "vlan_int3" 3 "$DIR/tmp/interfaces"
                replace "esr20_vlans_access" "3-5" "$DIR/tmp/interfaces"
        else
                replace "vlan_int3" 3 "$DIR/tmp/interfaces"
                replace "esr20_vlans_access" "3-4" "$DIR/tmp/interfaces"
        fi
        replace "vlan_int4" 10 "$DIR/tmp/interfaces"
        USERNAME_ESR=$(parse_conf "user_mvs_esr20" "$DIR/tmp/security")
elif [ $MODEL -eq 2 ]; then
        INTERFACES=$(parse_conf "esr20" "$DIR/tmp/interfaces")$'\n'$(parse_conf "esr21" "$DIR/tmp/interfaces")
        echo "$INTERFACES" > $DIR/tmp/interfaces
        replace "vlan_int1" 777 "$DIR/tmp/interfaces"
        replace "vlan_int2" 2 "$DIR/tmp/interfaces"
        replace "vlan_int3" 3 "$DIR/tmp/interfaces"
        replace "vlan_int4" 4 "$DIR/tmp/interfaces"
        correct_rule "esr20_vlans_access" "$DIR/tmp/interfaces" 1
        if [ $RAISA -eq 1 ]; then
                replace "vlan_int5" 5 "$DIR/tmp/interfaces"
        else
                replace "vlan_int5" 10 "$DIR/tmp/interfaces"
        fi
        replace "vlan_int6" 10 "$DIR/tmp/interfaces"
        replace "vlan_int7" 10 "$DIR/tmp/interfaces"
        replace "vlan_int8" 10 "$DIR/tmp/interfaces"
        USERNAME_ESR=$(parse_conf "user_mvs_esr21" "$DIR/tmp/security")
elif [ $MODEL -eq 3 ]; then
        INTERFACES=$(parse_conf "esr20" "$DIR/tmp/interfaces")$'\n'$(parse_conf "esr21" "$DIR/tmp/interfaces")$'\n'$(parse_conf "esr31" "$DIR/tmp/interfaces")
        echo "$INTERFACES" > $DIR/tmp/interfaces
        replace "vlan_int1" 777 "$DIR/tmp/interfaces"
        replace "vlan_int2" 2 "$DIR/tmp/interfaces"
        replace "vlan_int3" 3 "$DIR/tmp/interfaces"
        replace "vlan_int4" 4 "$DIR/tmp/interfaces"
        correct_rule "esr20_vlans_access" "$DIR/tmp/interfaces" 1
        if [ $RAISA -eq 1 ]; then
                replace "vlan_int5" 5 "$DIR/tmp/interfaces"
        else
                replace "vlan_int5" 10 "$DIR/tmp/interfaces"
        fi
        replace "vlan_int6" 10 "$DIR/tmp/interfaces"
        replace "vlan_int7" 10 "$DIR/tmp/interfaces"
        replace "vlan_int8" 10 "$DIR/tmp/interfaces"
        USERNAME_ESR=$(parse_conf "user_mvs_esr31" "$DIR/tmp/security")
else
        exit 0
fi

if [ $VERS -eq 1 ]; then
        VERSION_ESR=$(parse_conf "vers1_14" "$DIR/tmp/version")
elif [ $VERS -eq 2 ]; then
        VERSION_ESR=$(parse_conf "vers1_18" "$DIR/tmp/version")
fi

INTERFACES=$(cat $DIR/tmp/interfaces )

SERVICES=$(parse_conf "service_std" "$DIR/tmp/services")
if [ $TELEPORT -eq 1 ]; then
        declare -n SERVICES_PH=SERVICES
        SERVICES_PH+=$'\n'$(parse_conf "service_ph" "$DIR/tmp/services")
fi
if [ $VPN -eq 1 ]; then
        declare -n SERVICES_VPN=SERVICES
        SERVICES_VPN+=$'\n'$(parse_conf "service_VPN" "$DIR/tmp/services")
fi
if [ $TRUECONF -eq 1 ]; then
        declare -n SERVICES_TRUECONF=SERVICES
        SERVICES_TRUECONF+=$'\n'$(parse_conf "service_tc" "$DIR/tmp/services")
fi
if [ $TRUEROOM -eq 1 ]; then
        declare -n SERVICES_TRUEROOM=SERVICES
        SERVICES_TRUEROOM+=$'\n'$(parse_conf "service_tcroom" "$DIR/tmp/services")
fi

NETWORKS=$(parse_conf "network_std" "$DIR/tmp/networks")
if [ $TELEPORT -eq 1 ]; then
        declare -n NETWORKS_PH=NETWORKS
        NETWORKS_PH+=$'\n'$(parse_conf "network_ph" "$DIR/tmp/networks")
fi
if [ $VPN -eq 1 ]; then
        declare -n NETWORKS_VPN=NETWORKS
        NETWORKS_VPN+=$'\n'$(parse_conf "network_VPN" "$DIR/tmp/networks")
fi
if [ $RAISA -eq 1 ]; then
        declare -n NETWORKS_RAISA=NETWORKS
        NETWORKS_RAISA+=$'\n'$(parse_conf "network_raisa" "$DIR/tmp/networks")
fi
if [ $TRUECONF -eq 1 ]; then
        declare -n NETWORKS_TRUECONF=NETWORKS
        NETWORKS_TRUECONF+=$'\n'$(parse_conf "network_tc" "$DIR/tmp/networks")
fi
if [ $TRUEROOM -eq 1 ]; then
        declare -n NETWORKS_TRUEROOM=NETWORKS
        NETWORKS_TRUEROOM+=$'\n'$(parse_conf "network_tcroom" "$DIR/tmp/networks")
fi

VLANS=$(parse_conf "vlan_std" "$DIR/tmp/vlans")
if [ $RAISA -eq 1 ]; then
        declare -n VLAN_RAISA=VLANS
        VLAN_RAISA+=$'\n'$(parse_conf "vlan_raisa" "$DIR/tmp/vlans")
fi

BRS=$(parse_conf "br_all" "$DIR/tmp/vlans")
echo "$BRS" > $DIR/tmp/vlans
correct_rule "br_raisa" "$DIR/tmp/vlans" $RAISA
correct_rule "br_tcroom" "$DIR/tmp/vlans" $TRUEROOM
BRS=$( cat $DIR/tmp/vlans )

ZONES=$(parse_conf "zone_std" "$DIR/tmp/security")
if [ $VPN -eq 1 ]; then
        declare -n ZONE_VPN=ZONES
        ZONE_VPN+=$'\n'$(parse_conf "zone_VPN" "$DIR/tmp/security")
fi
if [ $RAISA -eq 1 ]; then
        declare -n ZONE_RAISA=ZONES
        ZONE_RAISA+=$'\n'$(parse_conf "zone_raisa" "$DIR/tmp/security")
fi

SECURITY=$(parse_conf "secure_all" "$DIR/tmp/security")
echo "$SECURITY" > $DIR/tmp/security
correct_rule "secure_ph" "$DIR/tmp/security" $TELEPORT
correct_rule "secure_raisa" "$DIR/tmp/security" $RAISA
correct_rule "secure_VPN" "$DIR/tmp/security" $VPN
correct_rule "secure_tc" "$DIR/tmp/security" $TRUECONF
correct_rule "secure_tcroom" "$DIR/tmp/security" $TRUEROOM
if [[ $RAISA -eq 1 && $VPN -eq 1 ]]; then
        correct_rule "secure_raisVPN" "$DIR/tmp/security" 1
else
        correct_rule "secure_raisVPN" "$DIR/tmp/security" 2
fi
SECURITY=$( cat $DIR/tmp/security )

if [ $VPN -eq 1 ]; then
        VPN_TUN=$(parse_conf "VPN_tun" "$DIR/tmp/vpn")
        echo "$VPN_TUN" > $DIR/tmp/vpn
        correct_rule "VPN_raisa" "$DIR/tmp/vpn" $RAISA
        VPN_TUN=$( cat $DIR/tmp/vpn )
fi

touch $DIR/tmp/nat_rules
NAT_DEST=$(parse_conf "nat_dest" "$DIR/tmp/nat")
echo "$NAT_DEST" > $DIR/tmp/nat_rules
correct_rule "nat_dest_ph" "$DIR/tmp/nat_rules" $TELEPORT
correct_rule "nat_dest_raisa" "$DIR/tmp/nat_rules" $RAISA
correct_rule "nat_dest_tc" "$DIR/tmp/nat_rules" $TRUECONF
correct_rule "nat_dest_tcroom" "$DIR/tmp/nat_rules" $TRUEROOM;

NAT_SOURCE=$(parse_conf "nat_source" "$DIR/tmp/nat")
echo "$NAT_SOURCE" >> $DIR/tmp/nat_rules
correct_rule "nat_source_raisa" "$DIR/tmp/nat_rules" $RAISA

NAT=$( cat $DIR/tmp/nat_rules )

echo "$VERSION_ESR" > $DIR/tmp/tmpstr
replace_multi "vers" $DIR/tmp/main $DIR/tmp/tmpstr 2

if [ $MODEL -eq 1 ]; then
        replace "esr_num" "20" "$DIR/tmp/main"
elif [ $MODEL -eq 2 ]; then
        replace "esr_num" "21" "$DIR/tmp/main"
elif [ $MODEL -eq 3 ]; then
        replace "esr_num" "31" "$DIR/tmp/main"
fi
replace "sert_name" $CERT "$DIR/tmp/main"

echo "$SERVICES" > $DIR/tmp/tmpstr
replace_multi "service" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$NETWORKS" > $DIR/tmp/tmpstr
replace_multi "network" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$USERNAME_ESR" > $DIR/tmp/tmpstr
replace_multi "user_mvs" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$VLANS" > $DIR/tmp/tmpstr
replace_multi "vlans" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$ZONES" > $DIR/tmp/tmpstr
replace_multi "zones" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$BRS" > $DIR/tmp/tmpstr
replace_multi "bridges" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$INTERFACES" > $DIR/tmp/tmpstr
replace_multi "interfaces" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$SECURITY" > $DIR/tmp/tmpstr
replace_multi "security" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$VPN_TUN" > $DIR/tmp/tmpstr
replace_multi "VPN" $DIR/tmp/main $DIR/tmp/tmpstr 2

echo "$NAT" > $DIR/tmp/tmpstr
replace_multi "nat" $DIR/tmp/main $DIR/tmp/tmpstr 2

replace "pub_ip" $PUBLIC_IP "$DIR/tmp/main"
if [ $RAISA -eq 1 ]; then
        replace "raisa_ip" $RAISA_IP "$DIR/tmp/main"

else
        correct_rule "raisa_ip" "$DIR/tmp/main" 1
fi
replace "pub_msk" $PUBLIC_MASK "$DIR/tmp/main"
replace "gate_ip" $GW "$DIR/tmp/main"
FIN_CONFIG=$( cat $DIR/tmp/main )


touch $DIR/config.cfg
echo "$FIN_CONFIG"| tail -n +2 > $DIR/config.cfg
log_message "Configuration saved in $DIR/config.cfg"
# rm -R $DIR/tmp
