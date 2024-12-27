from modules.ssh import SSHDriver

driver = {
    "family": "ubuntu",
    "tftp_server": "10.3.1.144",  # my local tftp-server serves this address on 69 port
    "host": "127.0.0.10",  # network device
    "auth_username": "koshsky",
    "auth_password": "fdsjkl",
    "auth_strict_key": False,  # important for unknown hosts
    "transport": "ssh2"
}

with SSHDriver(**driver) as ssh:
    resp = ssh.tftp_send(ssh, "/srv/tftp/aboba/conf.ff")