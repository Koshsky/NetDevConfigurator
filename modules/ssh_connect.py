from scrapli.driver import GenericDriver
import time


def mes_on_open(cls):

    time.sleep(0.25)
    cls.channel.write(cls.auth_password)
    cls.channel.send_return()
    print(cls.channel.read().decode('utf-8'))
    print("mes_on_open finished")

def mes_on_close(cls):
    cls.channel.write(channel_input="exit")
    cls.channel.send_return()


mes_config = {
    "host": "10.3.1.13",
    "auth_username": "mvsadmin",
    "auth_password": "MVS_admin",
    "on_open": mes_on_open,
    "on_close": mes_on_close,
    "comms_prompt_pattern": r"^(\\n)?console(\(.+\))?[#>]\s*$",
    "ssh_config_file": "~/NetDevConfigurator/modules/my_ssh_config",
}

def send_command(ssh, command):
    ssh.channel.write(command)
    time.sleep(1)

    response = ssh.channel.read().decode('utf-8')

    return response

if __name__ == "__main__":
    with GenericDriver(**mes_config) as ssh:
        while True:
            cmd = input()
            output = send_command(ssh, cmd)
            print(output)

