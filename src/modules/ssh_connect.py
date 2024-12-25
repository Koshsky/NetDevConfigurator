from scrapli.driver import GenericDriver
import time


def mes_on_open(cls):
    cls.channel.write(cls.auth_password)
    cls.channel.send_return()
    cls.send_command("set cli pagination off")  # important
    print("mes_on_open finished")

def mes_on_close(cls):
    cls.channel.write(channel_input="exit")
    cls.channel.send_return()


mes_config = {
    "host": "10.4.1.11",  # 10.3.1.13
    "auth_username": "admin",
    "auth_password": "mvsadmin",
    "on_open": mes_on_open,
    "on_close": mes_on_close,
    "comms_prompt_pattern": r"^(\\n)?[a-z0-9.\-_@/:]{1,63}[#>]\s*$",
    "ssh_config_file": "~/NetDevConfigurator/modules/my_ssh_config",
}

if __name__ == "__main__":
    with GenericDriver(**mes_config) as ssh:
        print(ssh.get_prompt())
        output = ssh.send_command("show running-config")
        print(output.result)
