
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