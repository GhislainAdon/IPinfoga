#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import argparse
import threading
import requests

from time import sleep as thread_delay

from .__main__ import IPinfoga
from .badges import Badges


class IPinfogaCLI(IPinfoga, Badges):
    thread_delay = 0.1

    description = "IPinfoga is an OSINT tool that dumps all available IP address information such as location with country, city and latitude with longitude."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-t', '--threads', dest='threads', action='store_true', help='Use threads for fastest work.')
    parser.add_argument('-o', '--output', dest='output', help='Output result to file.')
    parser.add_argument('-i', '--input', dest='input', help='Input file of addresses.')
    parser.add_argument('-a', '--address', dest='address', help='Single address.')
    args = parser.parse_args()

    def thread(self, address):
        data = self.info(address)

        if data:
            if not self.args.output:
                result = ""
                result += f"\n[ {address} ]\n"

                if 'ip' in data:
                    del data['ip']

                for field in data.keys():
                    result += f"\033[1;77m[i]\033[0m {field.replace('_', ' ').title()}: {data[field]}\n"

                self.print_empty(result)
            else:
                result = ""
                result += f"\n[ {address} ]\n"

                if 'ip' in data:
                    del data['ip']

                for field in data.keys():
                    result += f"[i] {field.replace('_', ' ').title()}: {data[field]}\n"

                with open(self.args.output, 'a') as f:
                    f.write(f"{result}")
            return True
        return False

    def scan(self, addresses):
        line = "/-\|"

        counter = 0
        threads = list()
        for address in addresses:
            if counter >= len(line):
                counter = 0
            self.print_process(f"Scanning... ({address}) {line[counter]}", end='')

            if not self.args.threads:
                self.thread(address)
            else:
                thread_delay(self.thread_delay)
                thread = threading.Thread(target=self.thread, args=[address])

                thread.start()
                threads.append(thread)
            counter += 1

        counter = 0
        for thread in threads:
            if counter >= len(line):
                counter = 0
            self.print_process(f"Cleaning up... {line[counter]}", end='')

            if thread.is_alive():
                thread.join()
            counter += 1
        
    def start(self):
        if self.args.output:
            directory = os.path.split(self.args.output)[0]
            if not os.path.isdir(directory):
                self.print_error(f"Directory: {directory}: does not exist!")
                return

        if self.args.input:
            if not os.path.exists(self.args.input):
                self.print_error(f"Input file: {self.args.input}: does not exist!")
                return

            with open(self.args.input, 'r') as f:
                addresses = f.read().strip().split('\n')
                self.scan(addresses)

        elif self.args.address:
            self.print_process(f"Scanning {self.args.address}...")
            if not self.thread(self.args.address):
                self.print_error("Failed to dump IP address information!")

        else:
            self.parser.print_help()
            return
        self.print_empty(end='')

def main():
    try:
        cli = IPinfogaCLI()
        cli.start()
    except Exception:
        pass
