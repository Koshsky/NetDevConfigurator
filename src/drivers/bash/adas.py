import subprocess


def f():
    script_path = "./src/drivers/bash/config_esr/draft.sh"

    try:
        result = subprocess.run(
            ["bash", script_path], check=True, text=True, capture_output=True
        )
        print("Вывод скрипта:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Ошибка при выполнении скрипта:")
        print(e.stderr)
