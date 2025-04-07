#!/usr/bin/env python3
"""
██████╗ ██████╗ ██╗   ██╗████████╗███████╗
██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝
██████╔╝██████╔╝██║   ██║   ██║   █████╗  
██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  
██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
BruteForce Framework v2.0
"""

import argparse
import itertools
import threading
import queue
import hashlib
import time
import os
import sys
from enum import Enum
from tqdm import tqdm

class AttackMode(Enum):
    BRUTEFORCE = "bruteforce"
    DICTIONARY = "dictionary"
    MASK = "mask"
    HYBRID = "hybrid"

class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"

class BruteforceTool:
    def __init__(self):
        self.mode = None
        self.charset = "abcdefghijklmnopqrstuvwxyz0123456789"
        self.min_len = 1
        self.max_len = 6
        self.target_hash = None
        self.wordlist = None
        self.mask = None
        self.threads = 8
        self.resume = None
        self.output = None
        self.running = False
        self.found = False
        self.result = None
        self.attempts = 0
        self.start_time = 0
        self.queue = queue.Queue()
        self.lock = threading.Lock()

    def print_banner(self):
        print(Color.BLUE + """
  ____             __  __      _   _             
 |  _ \           |  \/  |    | | | |            
 | |_) |_ __ _   _| \  / | ___| |_| |_ ___ _ __  
 |  _ <| '__| | | | |\/| |/ _ \ __| __/ _ \ '__| 
 | |_) | |  | |_| | |  | |  __/ |_| ||  __/ |    
 |____/|_|   \__,_|_|  |_|\___|\__|\__\___|_|    

        """ + Color.END)
        print(f"{Color.YELLOW}BruteForce Framework v2.0{Color.END}")
        print(f"{Color.YELLOW}========================{Color.END}\n")

    def hash_string(self, string, algorithm="md5"):
        if algorithm == "md5":
            return hashlib.md5(string.encode()).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(string.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(string.encode()).hexdigest()
        return string

    def load_wordlist(self, path):
        if not os.path.exists(path):
            print(f"{Color.RED}[!] Wordlist not found!{Color.END}")
            return None
        return [line.strip() for line in open(path, 'r', errors='ignore').readlines()]

    def generate_combinations(self):
        if self.mode == AttackMode.BRUTEFORCE:
            for length in range(self.min_len, self.max_len + 1):
                for combo in itertools.product(self.charset, repeat=length):
                    if self.found or not self.running:
                        return
                    yield ''.join(combo)
        elif self.mode == AttackMode.DICTIONARY and self.wordlist:
            for word in self.load_wordlist(self.wordlist):
                if self.found or not self.running:
                    return
                yield word

    def worker(self):
        while self.running and not self.found and not self.queue.empty():
            try:
                item = self.queue.get_nowait()
                with self.lock:
                    self.attempts += 1

                if self.hash_string(item) == self.target_hash:
                    with self.lock:
                        self.found = True
                        self.result = item
                        self.running = False
                
                self.queue.task_done()
            except queue.Empty:
                pass

    def run_attack(self):
        self.running = True
        self.start_time = time.time()
        threads = []

        # Setup progress bar
        total = len(self.charset) ** self.max_len if self.mode == AttackMode.BRUTEFORCE else len(self.load_wordlist(self.wordlist))
        
        # Start worker threads
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        # Fill queue with combinations
        for combo in self.generate_combinations():
            if self.found or not self.running:
                break
            self.queue.put(combo)

        # Progress monitoring
        with tqdm(total=total, unit="combos", desc=f"{Color.BLUE}Attacking{Color.END}", ncols=100) as pbar:
            while self.running and any(t.is_alive() for t in threads):
                pbar.update(self.attempts - pbar.n)
                time.sleep(0.1)
                if self.found:
                    break

        self.running = False
        for t in threads:
            t.join()

        return self.result

    def interactive_shell(self):
        self.print_banner()
        print(f"{Color.GREEN}Interactive mode activated{Color.END}")
        print("Type 'help' for available commands\n")
        
        while True:
            try:
                cmd = input(f"{Color.BLUE}bf > {Color.END}").strip().lower()
                
                if cmd == "help":
                    print("\nAvailable commands:")
                    print("  set <option> <value>  - Configure attack parameters")
                    print("  run                   - Start the attack")
                    print("  show options          - Show current configuration")
                    print("  exit                  - Quit the program\n")
                
                elif cmd.startswith("set "):
                    parts = cmd.split()
                    if len(parts) < 3:
                        print(f"{Color.RED}[!] Usage: set <option> <value>{Color.END}")
                        continue
                    
                    option, value = parts[1], ' '.join(parts[2:])
                    if option == "mode":
                        try:
                            self.mode = AttackMode(value)
                            print(f"Mode set to {value}")
                        except ValueError:
                            print(f"{Color.RED}[!] Invalid mode. Available: bruteforce, dictionary{Color.END}")
                    elif option == "charset":
                        self.charset = value
                        print(f"Charset set to {value}")
                    elif option == "min":
                        self.min_len = int(value)
                        print(f"Min length set to {value}")
                    elif option == "max":
                        self.max_len = int(value)
                        print(f"Max length set to {value}")
                    elif option == "threads":
                        self.threads = int(value)
                        print(f"Threads set to {value}")
                    elif option == "target":
                        self.target_hash = value
                        print(f"Target hash set to {value}")
                    elif option == "wordlist":
                        self.wordlist = value
                        print(f"Wordlist set to {value}")
                    else:
                        print(f"{Color.RED}[!] Unknown option{Color.END}")
                
                elif cmd == "run":
                    if not self.target_hash:
                        print(f"{Color.RED}[!] Target hash not set!{Color.END}")
                        continue
                    
                    if self.mode == AttackMode.DICTIONARY and not self.wordlist:
                        print(f"{Color.RED}[!] Wordlist not set for dictionary attack!{Color.END}")
                        continue
                    
                    print(f"\n{Color.YELLOW}[*] Starting attack...{Color.END}")
                    result = self.run_attack()
                    
                    if result:
                        print(f"\n{Color.GREEN}[+] Password found: {result}{Color.END}")
                        print(f"Attempts: {self.attempts}")
                        print(f"Time: {time.time() - self.start_time:.2f} seconds")
                    else:
                        print(f"\n{Color.RED}[-] Password not found{Color.END}")
                
                elif cmd == "show options":
                    print("\nCurrent configuration:")
                    print(f"  Mode:       {self.mode.value if self.mode else 'Not set'}")
                    print(f"  Charset:    {self.charset}")
                    print(f"  Min length: {self.min_len}")
                    print(f"  Max length: {self.max_len}")
                    print(f"  Threads:    {self.threads}")
                    print(f"  Target:     {self.target_hash}")
                    print(f"  Wordlist:   {self.wordlist}\n")
                
                elif cmd == "exit":
                    print("Goodbye!")
                    sys.exit(0)
                
                else:
                    print(f"{Color.RED}[!] Unknown command{Color.END}")

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"{Color.RED}[!] Error: {str(e)}{Color.END}")

def main():
    tool = BruteforceTool()
    
    parser = argparse.ArgumentParser(description="Advanced BruteForce Tool")
    parser.add_argument("-i", "--interactive", action="store_true", help="Start interactive shell")
    args = parser.parse_args()
    
    if args.interactive:
        tool.interactive_shell()
    else:
        tool.print_banner()
        print("Use -i for interactive mode")

if __name__ == "__main__":
    main()
