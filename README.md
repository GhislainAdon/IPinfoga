# IPinfoga

<p>
    <a href="https://entysec.netlify.app">
        <img src="https://img.shields.io/badge/developer-EntySec-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/IPinfoga">
        <img src="https://img.shields.io/badge/language-Python-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/IPinfoga/stargazers">
        <img src="https://img.shields.io/github/stars/EntySec/IPinfoga?color=yellow">
    </a>
</p>

IPinfoga is an OSINT tool that dumps available IP address information such as location with country, city, and latitude with longitude.

## Features

* Dumps geolocation data like country, city, and coordinates.
* Optimized to dump information for multiple IP addresses at one time.
* Simple CLI and API usage.

## Installation

```shell
pip3 install git+https://github.com/EntySec/IPinfoga
```

## Basic usage

To use IPinfoga just type `ipinfoga` in your terminal.

```
usage: ipinfoga [-h] [-t] [-o OUTPUT] [-i INPUT] [-a ADDRESS]

IPinfoga is an OSINT tool that dumps all available IP address information such
as location with country, city, and latitude with longitude.

optional arguments:
  -h, --help            show this help message and exit
  -t, --threads         Use threads for fastest work.
  -o OUTPUT, --output OUTPUT
                        Output result to file.
  -i INPUT, --input INPUT
                        Input file of addresses.
  -a ADDRESS, --address ADDRESS
                        Single address.
```

### Examples

**Scanning single address**

Let's scan google DNS address just for fun.

```shell
camraptor -a 8.8.8.8
```

**Scanning addresses from input file**

Let's try to use opened database of addresses with `-t` for fast scanning.

```shell
camraptor -t -i addresses.txt -o results.txt
```

**NOTE:** It will scan all addresses in `addresses.txt` list and save all obtained results to `results.txt`.

## API usage

IPinfoga also has their own Python API that can be invoked by importing IPinfoga to your code.

```python
from ipinfoga import IPinfoga
```

### Basic functions

There are all IPinfoga basic functions that can be used to scan specified address.

* `scan(address)` - Scan single IP address.

### Examples

**Scanning single address**

```python
from ipinfoga import IPinfoga

ipinfoga = IPinfoga()
data = ipinfoga.scan('8.8.8.8')

for field in data:
    print(field, data[field])
```

## Other tools

<p>
    <a href="https://github.com/EntySec/Ghost">
        <img src="https://img.shields.io/badge/EntySec-Ghost-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/HatVenom">
        <img src="https://img.shields.io/badge/EntySec-HatVenom-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/Shreder">
        <img src="https://img.shields.io/badge/EntySec-Shreder-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/HatSploit">
        <img src="https://img.shields.io/badge/EntySec-HatSploit-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/CamOver">
        <img src="https://img.shields.io/badge/EntySec-CamOver-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/RomBuster">
        <img src="https://img.shields.io/badge/EntySec-RomBuster-3572a5.svg">
    </a>
    <a href="https://github.com/EntySec/membrane">
        <img src="https://img.shields.io/badge/EntySec-membrane-f34c79.svg">
    </a>
    <a href="https://github.com/EntySec/pwny">
        <img src="https://img.shields.io/badge/EntySec-pwny-448eff.svg">
    </a>
</p>
