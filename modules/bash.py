import subprocess

def config_esr():
    try:
        subprocess.check_call(["bash", "../scripts/eltex/config_esr/make_config.sh"], stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
