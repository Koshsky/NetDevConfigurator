#!/bin/bash

#set -x

lang="bash"

parse_conf () {
	cat "$2" | sed -n "/<$1>/,/<@$1>/p"| tail -n +2|head -n -1| cut -f2
}

replace () {
    if [[ -z "$3" ]]; then
        echo "replace; Ошибка: входной файл не указан."
        return 0
    fi
    echo "Заменяем <$1> на $2 в файле $3"
    sed -ri "s|<$1>|$2|g" "$3"
}

replace_multi () {
	local STR_NUM=$(grep -n "<$1>" $2 | cut -f1 -d ":")
	if [ $4 -eq 1 ]; then
		correct_rule $1 $2 2
		STR_NUM=$((STR_NUM-1))
	elif [ $4 -eq 2 ]; then
		correct_rule $1 $2 1
	fi
	sed -i "$STR_NUM r $3" $2
}

correct_rule () {
	if [ $3 -eq "1" ]; then
		sed -i "/<$1>/d" $2
		sed -i "/<@$1>/d" $2
	elif  [ $3 -eq "2" ]; then
		sed -i "/<$1>/,/<@$1>/d" $2
	fi
}

count_items () {
	local PARSE_STR=$( parse_conf $1 $2 )
	local TMP_STR=""
	local FIN_STR=""
	for ((i=1;i<=$3;i++))
	do
		declare -n FIN_STR_ITER=FIN_STR
		TMP_STR=$(echo "$PARSE_STR"| tr ! $i)
		if [[ ! -z "$4" ]]; then
		  TMP_NUM=$(( ${i}+${4} ))
		  TMP_STR=$(echo "$TMP_STR"| tr ? $TMP_NUM)
		fi
		FIN_STR_ITER+=$(echo "$TMP_STR")$'\n'
	done
	echo "$FIN_STR"| head -n -1 > $DIR/tmp/tmpstr
	replace_multi $1 $2 $DIR/tmp/tmpstr 1
}

DIR=$(dirname ${BASH_SOURCE})

if [ $TYPE_COMPLEX -ne 1 ]; then
	PH_COUNT=1
	STREAM_COUNT=1
fi
if [ $TRUECONF -ne 1 ]; then
	TRUEROOM=2
fi

# Регулярные выражения для проверки значений
correct_model="([123]{1})"  # Для MODEL: 1, 2 или 3
correct_other="([12]{1})"    # Для остальных переменных: 1 или 2

error_messages=()

if ! [[ "$VERS" =~ $correct_other ]]; then
    error_messages+=("VERS: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$MODEL" =~ $correct_model ]]; then
    error_messages+=("MODEL: некорректное значение (ожидалось 1, 2 или 3)")
fi

if ! [[ "$VPN" =~ $correct_other ]]; then
    error_messages+=("VPN: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$TELEPORT" =~ $correct_other ]]; then
    error_messages+=("TELEPORT: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$RAISA" =~ $correct_other ]]; then
    error_messages+=("RAISA: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$TRUECONF" =~ $correct_other ]]; then
    error_messages+=("TRUECONF: некорректное значение (ожидалось 1 или 2)")
fi

if ! [[ "$TRUEROOM" =~ $correct_other ]]; then
    error_messages+=("TRUEROOM: некорректное значение (ожидалось 1 или 2)")
fi

# Проверка наличия ошибок
if [ ${#error_messages[@]} -eq 0 ]; then
    echo "Формируется файл конфигурации..."
else
    echo "Некорректные ответы:"
    for message in "${error_messages[@]}"; do
        echo " - $message"
    done
    exit 0
fi


if [ ! -d "./src/bash/config_esr/tmp" ]; then
    mkdir -p ./src/bash/config_esr/tmp
fi
rm -rf ./src/bash/config_esr/tmp/*

touch $DIR/tmp/tmpstr

cat $DIR/templates/main.txt| col -b > $DIR/tmp/main
cat $DIR/templates/version.txt| col -b > $DIR/tmp/version
cat $DIR/templates/services.txt| col -b > $DIR/tmp/services
cat $DIR/templates/networks.txt| col -b > $DIR/tmp/networks
cat $DIR/templates/interfaces.txt| col -b > $DIR/tmp/interfaces
cat $DIR/templates/vlans.txt| col -b > $DIR/tmp/vlans
cat $DIR/templates/security.txt| col -b > $DIR/tmp/security
cat $DIR/templates/vpn.txt| col -b > $DIR/tmp/vpn
cat $DIR/templates/nat.txt| col -b > $DIR/tmp/nat

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
		replace "tcroom_ip$i" "${TRUEROOM_IP[$i]}" "$DIR/tmp/networks"
		replace "tcroom_ip$i" "${TRUEROOM_IP[$i]}" "$DIR/tmp/vlans"
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

NAT_DEST=$(parse_conf "nat_dest" "$DIR/tmp/nat")
touch $DIR/tmp/nat_rules
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
# rm -R $DIR/tmp

touch $DIR/config.cfg
echo "$FIN_CONFIG" | tail -n +2 > $DIR/config.cfg

