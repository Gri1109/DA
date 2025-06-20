import socket
class User:
    def __init__(self,ip,soc:socket,login,porol):
        self.ip=ip
        self.soc=soc
        self.login=login
        self.porol=porol
        
    def __str__(self):
        return f"{self.login}"