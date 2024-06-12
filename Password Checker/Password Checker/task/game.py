import hashlib
import requests
import argparse


class PasswordChecker:
    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--show-hash', action='store_true')
        self.hashed = vars(parser.parse_args())['show_hash']

    def __init__(self):
        self.pswd = None
        self.parse_args()

    def set_password(self, pswd):
        self.pswd = pswd

    def check_length(self, pswd):
        if len(passwd) < 8:
            print("Your password is too short. Please enter a password of at least 8 characters.")
            return 0
        return 1

    def print_password(self):
        print("Your hashed password is:", self.hash_pwd)

    def hash_password(self):
        self.hash_pwd = hashlib.sha1(self.pswd.encode('utf-8')).hexdigest()
        if self.hashed:
            self.print_password()

    def send_request(self):
        print("Checking...")
        url = 'https://api.pwnedpasswords.com/range/' + self.hash_pwd[:5]
        r = requests.get(url, headers={"Add-Padding":"true"})
        x = 0
        for line in r.text.split('\n'):
            new_hash = line.split(':')
            if new_hash[0] == self.hash_pwd[5:].upper():
                x = new_hash[1]
                break
        if not x:
            print("Good news! Your password hasn't been pwned.")
        else:
            print('Your password has been pwned! This password appears ', x, ' times in data breaches.', sep='')

if __name__ == '__main__':
    while True:
        p = PasswordChecker()
        while not p.pswd:
            passwd = input("Enter your password (or 'exit' to quit):")
            if passwd == 'exit':
                print("Goodbye!")
                exit(0)
            if p.check_length(passwd):
                p.set_password(passwd)
                p.hash_password()
                p.send_request()
                p.pswd = None


