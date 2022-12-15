"""
LOGIN/REGISTRATION
"""
import getpass


class Authorization():

    def login(self):
        print(f"\n{' ':<10}----LOGIN----\n{' ':<4}(Login to access database)")
        usern = input(f"{' ':<4}USERNAME: ").strip()
        __passw = getpass.getpass(prompt=f"{' ':<4}PASSWORD: ").strip()
        __hashpass = self.hash(__passw)

        with open("./usr_cred.txt", "r") as f:
            line = f.readline().strip()

        if not line:
            return None
        username, password = line.split(",")
        if username == usern and password == __hashpass:
            return True
        return False

    def register(self):
        print(f"\n{' ':<10}----REGISTER----\n")
        usern = input(f"{' ':<10}USERNAME: ")
        __passw = getpass.getpass(prompt=f"{' ':<4}PASSWORD: ").strip()
        __hashpass = self.hash(__passw)

        with open("./usr_cred.txt", "w") as f:
            f.writelines(usern+","+__hashpass)

    def hash(self, passw):
        __hashpass = ""
        for _ in passw:
            __hashpass += chr(ord(_)+10)
        return __hashpass
