from modules.ssh import SSHDriver
from config import config
from pprint import pprint

ubuntu = {
    "family": "ubuntu",
    "host": "127.0.0.14",  # network device
    "auth_username": "koshsky",
    "auth_password": "fdsjkl",
    "auth_strict_key": False,  # important for unknown hosts
    "transport": "ssh2",
}

mes2428 = {
    "family": "MES14xx/24xx/34xx/37xx",
    "host": "10.3.1.13",  # network device
    "auth_username": "mvsadmin",
    "auth_password": "MVS_admin",
    "auth_strict_key": False,  # important for unknown hosts
    "transport": "ssh2",
}


def test_sshdriver():
    if input():
        with SSHDriver(**mes2428) as ssh:
            resp = ssh.tftp_send(
                ssh, "/srv/tftp/tmp/config_2757b31e-051f-4537-a820-4f43c36f19b2.conf"
            )
            print(resp.result)
    else:
        with SSHDriver(**ubuntu) as ssh:
            resp = ssh.send_command("ls -la")
            print(resp.result)


if __name__ == "__main__":
    pprint(config)
