from modules.ssh import SSHDriver

driver = {
    "family": "ubuntu",
    "tftp_server": "10.3.1.144",
    "host": "127.0.0.10",
    "auth_username": "koshsky",
    "auth_password": "fdsjkl",
    "auth_strict_key": False,
    "transport": "ssh2"
}

with SSHDriver(**driver) as ssh:
    resp = ssh.send_command("ls -a")
    print(resp.result)