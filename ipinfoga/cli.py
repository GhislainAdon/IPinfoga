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
                result += f"{address}:\n"

                if 'country_name' in data:
                    result += f"\033[1;77m[i]\033[0m Country: {data['country_name']}\n"
                if 'region_name' in data:
                    result += f"\033[1;77m[i]\033[0m  Region: {data['region_name']}\n"
                if 'city' in data:
                    result += f"\033[1;77m[i]\033[0m  City: {data['city']}\n"
                if 'time_zone' in data:
                    result += f"\033[1;77m[i]\033[0m  Time Zone: {data['time_zone']}\n"
                if 'latitude' in data:
                    result += f"\033[1;77m[i]\033[0m  Latitude: {data['latitude']}\n"
                if 'longitude' in data:
                    result += f"\033[1;77m[i]\033[0m  Longitude: {data['longitude']}\n"
                if 'country_code' in data:
                    result += f"\033[1;77m[i]\033[0m  Country Code: {data['country_code']}\n"
                if 'region_code' in data:
                    result += f"\033[1;77m[i]\033[0m  Region Code: {data['region_code']}\n"
                if 'zip_code' in data:
                    result += f"\033[1;77m[i]\033[0m  ZIP Code: {data['zip_code']}\n"
                if 'metro_code' in data:
                    result += f"\033[1;77m[i]\033[0m  Metro Code: {data['metro_code']}"

                self.print_empty(result)
            else:
                result = ""
                result += f"{address}:\n"

                if 'country_name' in data:
                    result += f"[i] Country: {data['country_name']}\n"
                if 'region_name' in data:
                    result += f"[i] Region: {data['region_name']}\n"
                if 'city' in data:
                    result += f"[i] City: {data['city']}\n"
                if 'time_zone' in data:
                    result += f"[i] Time Zone: {data['time_zone']}\n"
                if 'latitude' in data:
                    result += f"[i] Latitude: {data['latitude']}\n"
                if 'longitude' in data:
                    result += f"[i] Longitude: {data['longitude']}\n"
                if 'country_code' in data:
                    result += f"[i] Country Code: {data['country_code']}\n"
                if 'region_code' in data:
                    result += f"[i] Region Code: {data['region_code']}\n"
                if 'zip_code' in data:
                    result += f"[i] ZIP Code: {data['zip_code']}\n"
                if 'metro_code' in data:
                    result += f"[i] Metro Code: {data['metro_code']}"

                with open(self.args.output, 'a') as f:
                    f.write(f"{result}\n")

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
        if self.args.input:
            if not os.path.exists(self.args.input):
                self.print_error(f"Input file: {self.args.input}: does not exist!")
                return

            with open(self.args.input, 'r') as f:
                addresses = f.read().strip().split('\n')
                self.scan(addresses)

        elif self.args.address:
            self.print_process(f"Scanning {self.args.address}...")
            self.thread(self.args.address)

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
