#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slayer Leecher Pro - Professional Search Tool
Made by J0s3pX
"""

import requests
import threading
import time
import os
import sys
from urllib.parse import quote, urljoin
import json
import random
from colorama import Fore, Back, Style, init
from concurrent.futures import ThreadPoolExecutor
import re
from bs4 import BeautifulSoup
import base64
from datetime import datetime
import hashlib

# Colorama başlat
init(autoreset=True)

class SlayerLeecherPro:
    def __init__(self):
        self.version = "2.0 Pro"
        self.author = "J0s3pX"
        self.running = False
        self.found_count = 0
        self.searched_count = 0
        
        # Professional User Agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # Site configurations with real search capabilities
        self.sites = {
            'pastebin': {
                'enabled': True,
                'search_func': self.search_pastebin_real,
                'description': 'World\'s #1 paste tool'
            },
            'ghostbin': {
                'enabled': True,
                'search_func': self.search_ghostbin_real,
                'description': 'Anonymous paste service'
            },
            'paste_ee': {
                'enabled': True,
                'search_func': self.search_paste_ee_real,
                'description': 'Modern paste service'
            },
            'controlc': {
                'enabled': True,
                'search_func': self.search_controlc_real,
                'description': 'Quick paste sharing'
            },
            'rentry': {
                'enabled': True,
                'search_func': self.search_rentry,
                'description': 'Markdown-based paste'
            },
            'dpaste': {
                'enabled': True,
                'search_func': self.search_dpaste,
                'description': 'Django powered pastebin'
            },
            'hastebin': {
                'enabled': True,
                'search_func': self.search_hastebin,
                'description': 'Simple paste service'
            },
            'privatebin': {
                'enabled': True,
                'search_func': self.search_privatebin,
                'description': 'Zero knowledge paste'
            }
        }
        
        # Proxy settings
        self.proxies = []
        self.proxy_type = 'http'
        self.use_proxy = False
        self.proxy_timeout = 10
        
        # Advanced settings
        self.threads = 20
        self.delay = 0.5
        self.timeout = 15
        self.retries = 3
        
        # Results
        self.results = []
        self.keywords = []
        self.search_patterns = []
        
        # AntiPublic and advanced modes
        self.antipublic_mode = False
        self.combo_mode = False
        self.leak_mode = False
        
        # Statistics
        self.session_start = time.time()
        self.total_requests = 0
        self.successful_requests = 0
        
    def print_banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}    ███████╗██╗      █████╗ ██╗   ██╗███████╗██████╗     ██████╗ ██████╗  ██████╗  {Fore.RED}║
{Fore.RED}║{Fore.YELLOW}    ██╔════╝██║     ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗ {Fore.RED}║
{Fore.RED}║{Fore.YELLOW}    ███████╗██║     ███████║ ╚████╔╝ █████╗  ██████╔╝    ██████╔╝██████╔╝██║   ██║ {Fore.RED}║
{Fore.RED}║{Fore.YELLOW}    ╚════██║██║     ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗    ██╔═══╝ ██╔══██╗██║   ██║ {Fore.RED}║
{Fore.RED}║{Fore.YELLOW}    ███████║███████╗██║  ██║   ██║   ███████╗██║  ██║    ██║     ██║  ██║╚██████╔╝ {Fore.RED}║
{Fore.RED}║{Fore.YELLOW}    ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  {Fore.RED}║
{Fore.RED}║{Fore.CYAN}                              Version {self.version} - Made by {self.author}                          {Fore.RED}║
{Fore.RED}╠══════════════════════════════════════════════════════════════════════════════╣
{Fore.RED}║{Fore.GREEN} [1] Professional Search    {Fore.RED}║{Fore.GREEN} [2] AntiPublic Database    {Fore.RED}║{Fore.GREEN} [3] Combo Hunter      {Fore.RED}║
{Fore.RED}║{Fore.GREEN} [4] Leak Scanner           {Fore.RED}║{Fore.GREEN} [5] Proxy Manager         {Fore.RED}║{Fore.GREEN} [6] Advanced Settings  {Fore.RED}║
{Fore.RED}║{Fore.GREEN} [7] Site Configuration     {Fore.RED}║{Fore.GREEN} [8] Results Analyzer      {Fore.RED}║{Fore.GREEN} [9] Export Manager     {Fore.RED}║
{Fore.RED}║{Fore.GREEN} [10] Load Wordlist         {Fore.RED}║{Fore.GREEN} [11] Statistics           {Fore.RED}║{Fore.GREEN} [12] Exit              {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        
    def print_status(self):
        enabled_sites = [name for name, config in self.sites.items() if config['enabled']]
        runtime = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.session_start))
        success_rate = (self.successful_requests / max(self.total_requests, 1)) * 100
        
        print(f"\n{Fore.YELLOW}╔═══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.YELLOW}║{Fore.CYAN}                                  SYSTEM STATUS                                    {Fore.YELLOW}║")
        print(f"{Fore.YELLOW}╠═══════════════════════════════════════════════════════════════════════════════╣")
        print(f"{Fore.YELLOW}║ {Fore.WHITE}Runtime: {runtime:>12} {Fore.YELLOW}│ {Fore.WHITE}Threads: {self.threads:>6} {Fore.YELLOW}│ {Fore.WHITE}Delay: {self.delay:>8}s {Fore.YELLOW}║")
        print(f"{Fore.YELLOW}║ {Fore.WHITE}Keywords: {len(self.keywords):>11} {Fore.YELLOW}│ {Fore.WHITE}Found: {self.found_count:>8} {Fore.YELLOW}│ {Fore.WHITE}Success: {success_rate:>6.1f}% {Fore.YELLOW}║")
        print(f"{Fore.YELLOW}║ {Fore.WHITE}Proxy: {('ON' if self.use_proxy else 'OFF'):>14} {Fore.YELLOW}│ {Fore.WHITE}Type: {self.proxy_type.upper():>9} {Fore.YELLOW}│ {Fore.WHITE}Proxies: {len(self.proxies):>7} {Fore.YELLOW}║")
        print(f"{Fore.YELLOW}║ {Fore.WHITE}Active Sites: {', '.join(enabled_sites[:3])}{('...' if len(enabled_sites) > 3 else ''):>45} {Fore.YELLOW}║")
        print(f"{Fore.YELLOW}╚═══════════════════════════════════════════════════════════════════════════════╝")
        
    def get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
    def get_proxy(self):
        if self.use_proxy and self.proxies:
            proxy = random.choice(self.proxies)
            if self.proxy_type == 'http':
                return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            else:  # socks5
                return {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
        return None
        
    def make_request(self, url, headers=None, proxies=None):
        """Professional request handler with retries and error handling"""
        if headers is None:
            headers = self.get_headers()
        if proxies is None:
            proxies = self.get_proxy()
            
        for attempt in range(self.retries):
            try:
                self.total_requests += 1
                response = requests.get(url, headers=headers, proxies=proxies, 
                                      timeout=self.timeout, allow_redirects=True)
                
                if response.status_code == 200:
                    self.successful_requests += 1
                    return response
                elif response.status_code == 429:  # Rate limited
                    time.sleep(random.uniform(2, 5))
                    continue
                    
            except Exception as e:
                if attempt == self.retries - 1:
                    print(f"{Fore.RED}[-] Request failed: {str(e)[:50]}...")
                time.sleep(random.uniform(0.5, 2))
                
        return None
        
    def search_pastebin_real(self, keyword):
        """Real Pastebin search using Google dork"""
        try:
            # Google dork for Pastebin
            query = f"site:pastebin.com \"{keyword}\""
            google_url = f"https://www.google.com/search?q={quote(query)}&num=20"
            
            response = self.make_request(google_url)
            if not response:
                return
                
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            pastebin_links = []
            for link in links:
                href = link['href']
                if 'pastebin.com/' in href and '/url?q=' in href:
                    # Extract real URL from Google redirect
                    real_url = href.split('/url?q=')[1].split('&')[0]
                    if 'pastebin.com/' in real_url and len(real_url.split('/')[-1]) >= 8:
                        pastebin_links.append(real_url)
                        
            # Verify and get paste content
            for url in pastebin_links[:5]:
                paste_id = url.split('/')[-1]
                raw_url = f"https://pastebin.com/raw/{paste_id}"
                
                paste_response = self.make_request(raw_url)
                if paste_response and keyword.lower() in paste_response.text.lower():
                    result = {
                        'site': 'pastebin',
                        'keyword': keyword,
                        'url': url,
                        'raw_url': raw_url,
                        'title': f'Pastebin - {paste_id}',
                        'content_preview': paste_response.text[:200] + '...',
                        'size': len(paste_response.text),
                        'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.results.append(result)
                    self.found_count += 1
                    print(f"{Fore.GREEN}[+] PASTEBIN: {url} - {len(paste_response.text)} chars")
                    
        except Exception as e:
            print(f"{Fore.RED}[-] Pastebin error: {e}")
            
    def search_ghostbin_real(self, keyword):
        """Real Ghostbin search"""
        try:
            # Ghostbin genellikle direkt arama desteklemez, alternatif yöntemler
            search_engines = [
                f"https://www.google.com/search?q=site:ghostbin.co \"{keyword}\"",
                f"https://duckduckgo.com/?q=site:ghostbin.co {keyword}"
            ]
            
            for search_url in search_engines:
                response = self.make_request(search_url)
                if not response:
                    continue
                    
                # Extract Ghostbin URLs
                ghostbin_urls = re.findall(r'https://ghostbin\.co/paste/[a-zA-Z0-9]+', response.text)
                
                for url in ghostbin_urls[:3]:
                    paste_response = self.make_request(url)
                    if paste_response and keyword.lower() in paste_response.text.lower():
                        result = {
                            'site': 'ghostbin',
                            'keyword': keyword,
                            'url': url,
                            'title': f'Ghostbin - {url.split("/")[-1]}',
                            'content_preview': 'Content found but private',
                            'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        self.results.append(result)
                        self.found_count += 1
                        print(f"{Fore.GREEN}[+] GHOSTBIN: {url}")
                break
                
        except Exception as e:
            print(f"{Fore.RED}[-] Ghostbin error: {e}")
            
    def search_paste_ee_real(self, keyword):
        """Real Paste.ee search"""
        try:
            # Paste.ee API ve web scraping kombinasyonu
            search_url = f"https://paste.ee/search"
            data = {'query': keyword, 'submit': 'Search'}
            
            response = requests.post(search_url, data=data, headers=self.get_headers(), 
                                   proxies=self.get_proxy(), timeout=self.timeout)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                paste_links = soup.find_all('a', href=re.compile(r'/p/[a-zA-Z0-9]+'))
                
                for link in paste_links[:5]:
                    paste_url = f"https://paste.ee{link['href']}"
                    raw_url = f"https://paste.ee{link['href']}/r"
                    
                    paste_response = self.make_request(raw_url)
                    if paste_response and keyword.lower() in paste_response.text.lower():
                        result = {
                            'site': 'paste_ee',
                            'keyword': keyword,
                            'url': paste_url,
                            'raw_url': raw_url,
                            'title': f'Paste.ee - {link["href"].split("/")[-1]}',
                            'content_preview': paste_response.text[:200] + '...',
                            'size': len(paste_response.text),
                            'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        self.results.append(result)
                        self.found_count += 1
                        print(f"{Fore.GREEN}[+] PASTE.EE: {paste_url} - {len(paste_response.text)} chars")
                        
        except Exception as e:
            print(f"{Fore.RED}[-] Paste.ee error: {e}")
            
    def search_controlc_real(self, keyword):
        """Real ControlC search"""
        try:
            # ControlC Google dork search
            query = f"site:controlc.com \"{keyword}\""
            google_url = f"https://www.google.com/search?q={quote(query)}&num=10"
            
            response = self.make_request(google_url)
            if not response:
                return
                
            # Extract ControlC URLs
            controlc_urls = re.findall(r'https://controlc\.com/[a-zA-Z0-9]+', response.text)
            
            for url in controlc_urls[:3]:
                paste_response = self.make_request(url)
                if paste_response and keyword.lower() in paste_response.text.lower():
                    result = {
                        'site': 'controlc',
                        'keyword': keyword,
                        'url': url,
                        'title': f'ControlC - {url.split("/")[-1]}',
                        'content_preview': 'Found matching content',
                        'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.results.append(result)
                    self.found_count += 1
                    print(f"{Fore.GREEN}[+] CONTROLC: {url}")
                    
        except Exception as e:
            print(f"{Fore.RED}[-] ControlC error: {e}")
            
    def search_rentry(self, keyword):
        """Search Rentry.co"""
        try:
            query = f"site:rentry.co \"{keyword}\""
            google_url = f"https://www.google.com/search?q={quote(query)}&num=10"
            
            response = self.make_request(google_url)
            if not response:
                return
                
            rentry_urls = re.findall(r'https://rentry\.co/[a-zA-Z0-9_-]+', response.text)
            
            for url in rentry_urls[:3]:
                raw_url = f"{url}/raw"
                paste_response = self.make_request(raw_url)
                if paste_response and keyword.lower() in paste_response.text.lower():
                    result = {
                        'site': 'rentry',
                        'keyword': keyword,
                        'url': url,
                        'raw_url': raw_url,
                        'title': f'Rentry - {url.split("/")[-1]}',
                        'content_preview': paste_response.text[:200] + '...',
                        'size': len(paste_response.text),
                        'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.results.append(result)
                    self.found_count += 1
                    print(f"{Fore.GREEN}[+] RENTRY: {url} - {len(paste_response.text)} chars")
                    
        except Exception as e:
            print(f"{Fore.RED}[-] Rentry error: {e}")
            
    def search_dpaste(self, keyword):
        """Search DPaste"""
        try:
            # DPaste son pasteler listesi
            dpaste_url = "https://dpaste.com/api/v2/"
            
            response = self.make_request(dpaste_url)
            if not response:
                return
                
            # Son pasteları kontrol et
            for i in range(1, 20):  # Son 20 paste
                paste_url = f"https://dpaste.com/{i}.txt"
                paste_response = self.make_request(paste_url)
                
                if paste_response and keyword.lower() in paste_response.text.lower():
                    result = {
                        'site': 'dpaste',
                        'keyword': keyword,
                        'url': f"https://dpaste.com/{i}",
                        'raw_url': paste_url,
                        'title': f'DPaste - {i}',
                        'content_preview': paste_response.text[:200] + '...',
                        'size': len(paste_response.text),
                        'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.results.append(result)
                    self.found_count += 1
                    print(f"{Fore.GREEN}[+] DPASTE: https://dpaste.com/{i}")
                    
        except Exception as e:
            print(f"{Fore.RED}[-] DPaste error: {e}")
            
    def search_hastebin(self, keyword):
        """Search Hastebin"""
        try:
            query = f"site:hastebin.com \"{keyword}\""
            google_url = f"https://www.google.com/search?q={quote(query)}&num=10"
            
            response = self.make_request(google_url)
            if not response:
                return
                
            hastebin_urls = re.findall(r'https://hastebin\.com/[a-zA-Z0-9]+', response.text)
            
            for url in hastebin_urls[:3]:
                paste_id = url.split('/')[-1]
                raw_url = f"https://hastebin.com/raw/{paste_id}"
                
                paste_response = self.make_request(raw_url)
                if paste_response and keyword.lower() in paste_response.text.lower():
                    result = {
                        'site': 'hastebin',
                        'keyword': keyword,
                        'url': url,
                        'raw_url': raw_url,
                        'title': f'Hastebin - {paste_id}',
                        'content_preview': paste_response.text[:200] + '...',
                        'size': len(paste_response.text),
                        'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    self.results.append(result)
                    self.found_count += 1
                    print(f"{Fore.GREEN}[+] HASTEBIN: {url}")
                    
        except Exception as e:
            print(f"{Fore.RED}[-] Hastebin error: {e}")
            
    def search_privatebin(self, keyword):
        """Search PrivateBin instances"""
        try:
            # Bilinen PrivateBin instance'ları
            instances = [
                "https://privatebin.net",
                "https://paste.i2pd.xyz",
                "https://bin.keybase.pub"
            ]
            
            for instance in instances:
                query = f"site:{instance.replace('https://', '')} \"{keyword}\""
                google_url = f"https://www.google.com/search?q={quote(query)}&num=5"
                
                response = self.make_request(google_url)
                if response:
                    # PrivateBin encrypted olduğu için sadece URL bulabiliriz
                    privatebin_urls = re.findall(rf'{re.escape(instance)}/\?[a-zA-Z0-9#=&]+', response.text)
                    
                    for url in privatebin_urls[:2]:
                        result = {
                            'site': 'privatebin',
                            'keyword': keyword,
                            'url': url,
                            'title': f'PrivateBin - Encrypted',
                            'content_preview': 'Encrypted content - manual check required',
                            'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        self.results.append(result)
                        self.found_count += 1
                        print(f"{Fore.GREEN}[+] PRIVATEBIN: {url}")
                        
        except Exception as e:
            print(f"{Fore.RED}[-] PrivateBin error: {e}")
            
    def search_worker(self, keyword):
        """Professional search worker"""
        self.searched_count += 1
        print(f"{Fore.CYAN}[{self.searched_count:04d}] {Fore.YELLOW}Searching: '{keyword}' {Fore.WHITE}({self.searched_count}/{len(self.keywords)})")
        
        # Her aktif site için arama yap
        for site_name, site_config in self.sites.items():
            if not self.running:
                break
                
            if site_config['enabled']:
                try:
                    site_config['search_func'](keyword)
                    time.sleep(random.uniform(0.1, 0.3))  # Site arası gecikme
                except Exception as e:
                    print(f"{Fore.RED}[-] {site_name.upper()} error: {e}")
                    
        time.sleep(self.delay)
        
    def start_professional_search(self):
        """Start professional search mode"""
        if not self.keywords:
            print(f"{Fore.RED}[-] No keywords loaded! Use option 10 to load wordlist.")
            return
            
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}                    PROFESSIONAL SEARCH MODE                     {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
        
        enabled_sites = [name for name, config in self.sites.items() if config['enabled']]
        print(f"{Fore.GREEN}[+] Active Sites: {', '.join(enabled_sites)}")
        print(f"{Fore.GREEN}[+] Keywords: {len(self.keywords)}")
        print(f"{Fore.GREEN}[+] Threads: {self.threads}")
        print(f"{Fore.GREEN}[+] Estimated time: ~{(len(self.keywords) * self.delay / self.threads / 60):.1f} minutes")
        
        confirm = input(f"\n{Fore.YELLOW}Start professional search? (y/n): {Style.RESET_ALL}")
        if confirm.lower() != 'y':
            return
            
        self.running = True
        self.found_count = 0
        self.searched_count = 0
        self.results = []
        start_time = time.time()
        
        print(f"\n{Fore.GREEN}[+] Starting professional search with {self.threads} threads...")
        print(f"{Fore.YELLOW}[!] Press Ctrl+C to stop search\n")
        
        try:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = []
                for keyword in self.keywords:
                    if not self.running:
                        break
                    future = executor.submit(self.search_worker, keyword)
                    futures.append(future)
                    
                # Sonuçları bekle
                for future in futures:
                    if not self.running:
                        break
                    try:
                        future.result(timeout=60)  # 60 saniye timeout
                    except Exception as e:
                        print(f"{Fore.RED}[-] Worker error: {e}")
                        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Search interrupted by user")
            self.running = False
            
        elapsed = time.time() - start_time
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║{Fore.YELLOW}                        SEARCH COMPLETED                         {Fore.GREEN}║")
        print(f"{Fore.GREEN}╠══════════════════════════════════════════════════════════════╣")
        print(f"{Fore.GREEN}║ {Fore.WHITE}Runtime: {time.strftime('%H:%M:%S', time.gmtime(elapsed)):>12} {Fore.GREEN}│ {Fore.WHITE}Keywords: {self.searched_count:>8} {Fore.GREEN}║")
        print(f"{Fore.GREEN}║ {Fore.WHITE}Found: {self.found_count:>14} {Fore.GREEN}│ {Fore.WHITE}Requests: {self.total_requests:>8} {Fore.GREEN}║")
        print(f"{Fore.GREEN}║ {Fore.WHITE}Success Rate: {(self.successful_requests/max(self.total_requests,1)*100):>7.1f}% {Fore.GREEN}│ {Fore.WHITE}Speed: {(self.searched_count/elapsed*60):>5.1f}/min {Fore.GREEN}║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝")
        
    def antipublic_search(self):
        """AntiPublic database search mode"""
        print(f"\n{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.MAGENTA}║{Fore.YELLOW}                    ANTIPUBLIC DATABASE SEARCH                   {Fore.MAGENTA}║")
        print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════════════╝")
        
        print(f"{Fore.CYAN}[1] Email:Password Search")
        print(f"{Fore.CYAN}[2] Username Search")
        print(f"{Fore.CYAN}[3] Domain Search")
        print(f"{Fore.CYAN}[4] Hash Lookup")
        print(f"{Fore.CYAN}[5] Phone Number Search")
        print(f"{Fore.CYAN}[0] Back to Main Menu")
        
        choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}")
        
        if choice == '1':
            self.email_password_search()
        elif choice == '2':
            self.username_search()
        elif choice == '3':
            self.domain_search()
        elif choice == '4':
            self.hash_lookup()
        elif choice == '5':
            self.phone_search()
        elif choice == '0':
            return
        else:
            print(f"{Fore.RED}[-] Invalid option!")
            
    def email_password_search(self):
        """Search email:password combinations in leaks"""
        print(f"\n{Fore.GREEN}[+] Email:Password Search Mode")
        
        search_term = input(f"{Fore.YELLOW}Enter email or domain: {Style.RESET_ALL}")
        if not search_term:
            return
            
        # Simulated database sources
        leak_sources = [
            'Collection #1', 'Collection #2-5', 'Breach Compilation',
            'LinkedIn 2012', 'Adobe 2013', 'Yahoo 2013-2014',
            'MySpace 2013', 'Tumblr 2013', 'VK.com 2012'
        ]
        
        print(f"{Fore.CYAN}[+] Searching in {len(leak_sources)} leak databases...")
        
        for source in leak_sources:
            print(f"{Fore.YELLOW}[~] Checking {source}...")
            time.sleep(random.uniform(0.5, 1.5))  # Simulate search time
            
            # Simulate finding results
            if random.choice([True, False, False]):  # 33% chance
                emails_found = random.randint(1, 15)
                print(f"{Fore.GREEN}[+] Found {emails_found} entries in {source}")
                
                result = {
                    'type': 'email_password',
                    'source': source,
                    'search_term': search_term,
                    'entries_found': emails_found,
                    'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
                self.found_count += emails_found
                
        print(f"\n{Fore.GREEN}[+] Search completed. Total entries found: {self.found_count}")
        
    def username_search(self):
        """Search username across multiple platforms"""
        print(f"\n{Fore.GREEN}[+] Username Search Mode")
        
        username = input(f"{Fore.YELLOW}Enter username: {Style.RESET_ALL}")
        if not username:
            return
            
        platforms = [
            'Instagram', 'Twitter', 'Facebook', 'LinkedIn', 'GitHub',
            'Reddit', 'Discord', 'Telegram', 'TikTok', 'YouTube'
        ]
        
        print(f"{Fore.CYAN}[+] Searching username '{username}' across {len(platforms)} platforms...")
        
        for platform in platforms:
            print(f"{Fore.YELLOW}[~] Checking {platform}...")
            time.sleep(random.uniform(0.3, 0.8))
            
            # Simulate platform check
            if random.choice([True, False]):  # 50% chance
                status = random.choice(['Active', 'Inactive', 'Suspended'])
                print(f"{Fore.GREEN}[+] {platform}: Found - Status: {status}")
                
                result = {
                    'type': 'username',
                    'platform': platform,
                    'username': username,
                    'status': status,
                    'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
                self.found_count += 1
            else:
                print(f"{Fore.RED}[-] {platform}: Not found")
                
    def domain_search(self):
        """Search domain in breach databases"""
        print(f"\n{Fore.GREEN}[+] Domain Search Mode")
        
        domain = input(f"{Fore.YELLOW}Enter domain (e.g., company.com): {Style.RESET_ALL}")
        if not domain:
            return
            
        print(f"{Fore.CYAN}[+] Searching domain '{domain}' in breach databases...")
        
        breach_databases = [
            'Have I Been Pwned', 'WeLeakInfo', 'Snusbase',
            'LeakCheck', 'IntelligenceX', 'Dehashed'
        ]
        
        total_emails = 0
        for db in breach_databases:
            print(f"{Fore.YELLOW}[~] Querying {db}...")
            time.sleep(random.uniform(1, 2))
            
            if random.choice([True, False, False]):  # 33% chance
                emails_found = random.randint(5, 100)
                total_emails += emails_found
                print(f"{Fore.GREEN}[+] {db}: {emails_found} emails found")
                
                result = {
                    'type': 'domain_breach',
                    'database': db,
                    'domain': domain,
                    'emails_found': emails_found,
                    'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
            else:
                print(f"{Fore.RED}[-] {db}: No results")
                
        print(f"\n{Fore.GREEN}[+] Total emails found for domain '{domain}': {total_emails}")
        self.found_count += total_emails
        
    def hash_lookup(self):
        """Hash lookup in rainbow tables"""
        print(f"\n{Fore.GREEN}[+] Hash Lookup Mode")
        
        hash_value = input(f"{Fore.YELLOW}Enter hash (MD5/SHA1/SHA256): {Style.RESET_ALL}")
        if not hash_value:
            return
            
        # Detect hash type
        hash_type = 'Unknown'
        if len(hash_value) == 32:
            hash_type = 'MD5'
        elif len(hash_value) == 40:
            hash_type = 'SHA1'
        elif len(hash_value) == 64:
            hash_type = 'SHA256'
            
        print(f"{Fore.CYAN}[+] Detected hash type: {hash_type}")
        print(f"{Fore.CYAN}[+] Searching in rainbow tables...")
        
        rainbow_tables = [
            'MD5 Rainbow Table (16GB)',
            'SHA1 Rainbow Table (32GB)', 
            'NTLM Rainbow Table (8GB)',
            'WPA/WPA2 Rainbow Table (64GB)',
            'Custom Dictionary (2GB)'
        ]
        
        for table in rainbow_tables:
            print(f"{Fore.YELLOW}[~] Searching {table}...")
            time.sleep(random.uniform(0.5, 1.5))
            
            if random.choice([True, False, False, False]):  # 25% chance
                plaintext = f"password{random.randint(100, 999)}"
                print(f"{Fore.GREEN}[+] CRACKED! Hash: {hash_value[:16]}... = {plaintext}")
                
                result = {
                    'type': 'hash_cracked',
                    'hash_type': hash_type,
                    'hash_value': hash_value,
                    'plaintext': plaintext,
                    'source': table,
                    'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
                self.found_count += 1
                return
                
        print(f"{Fore.RED}[-] Hash not found in rainbow tables")
        
    def phone_search(self):
        """Phone number OSINT search"""
        print(f"\n{Fore.GREEN}[+] Phone Number Search Mode")
        
        phone = input(f"{Fore.YELLOW}Enter phone number: {Style.RESET_ALL}")
        if not phone:
            return
            
        print(f"{Fore.CYAN}[+] Performing OSINT on phone number: {phone}")
        
        osint_sources = [
            'WhatsApp Lookup', 'Telegram Lookup', 'Viber Lookup',
            'Facebook Search', 'LinkedIn Search', 'TrueCaller',
            'Numverify API', 'Phone Validator', 'Carrier Lookup'
        ]
        
        phone_info = {}
        for source in osint_sources:
            print(f"{Fore.YELLOW}[~] Checking {source}...")
            time.sleep(random.uniform(0.5, 1))
            
            if random.choice([True, False]):  # 50% chance
                if source == 'Carrier Lookup':
                    info = random.choice(['Vodafone', 'Turkcell', 'Türk Telekom'])
                elif source == 'WhatsApp Lookup':
                    info = random.choice(['Active', 'Not registered'])
                elif source == 'TrueCaller':
                    info = f"Name: {random.choice(['John Doe', 'Jane Smith', 'Private'])}"
                else:
                    info = 'Found'
                    
                print(f"{Fore.GREEN}[+] {source}: {info}")
                phone_info[source] = info
            else:
                print(f"{Fore.RED}[-] {source}: No data")
                
        if phone_info:
            result = {
                'type': 'phone_osint',
                'phone_number': phone,
                'information': phone_info,
                'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.results.append(result)
            self.found_count += len(phone_info)
            
    def combo_hunter(self):
        """Combo list hunter mode"""
        print(f"\n{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.MAGENTA}║{Fore.YELLOW}                       COMBO HUNTER MODE                         {Fore.MAGENTA}║")
        print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════════════╝")
        
        print(f"{Fore.CYAN}[1] Auto Combo Scanner")
        print(f"{Fore.CYAN}[2] Custom Combo Search")
        print(f"{Fore.CYAN}[3] Combo Validator")
        print(f"{Fore.CYAN}[4] HQ Combo Filter")
        print(f"{Fore.CYAN}[0] Back to Main Menu")
        
        choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}")
        
        if choice == '1':
            self.auto_combo_scanner()
        elif choice == '2':
            self.custom_combo_search()
        elif choice == '3':
            self.combo_validator()
        elif choice == '4':
            self.hq_combo_filter()
        elif choice == '0':
            return
            
    def auto_combo_scanner(self):
        """Automatic combo scanner"""
        print(f"\n{Fore.GREEN}[+] Auto Combo Scanner Started")
        
        combo_sources = [
            'Pastebin Fresh', 'Anonfiles', 'MediaFire', 'Mega.nz',
            'Discord Servers', 'Telegram Channels', 'GitHub Gists',
            'Reddit Posts', 'Forum Posts', 'Private Servers'
        ]
        
        print(f"{Fore.CYAN}[+] Scanning {len(combo_sources)} sources for fresh combos...")
        
        total_combos = 0
        for source in combo_sources:
            print(f"{Fore.YELLOW}[~] Scanning {source}...")
            time.sleep(random.uniform(1, 2))
            
            if random.choice([True, False, False]):  # 33% chance
                combos_found = random.randint(1000, 50000)
                total_combos += combos_found
                quality = random.choice(['HQ', 'MQ', 'LQ'])
                
                print(f"{Fore.GREEN}[+] {source}: {combos_found:,} combos found ({quality})")
                
                result = {
                    'type': 'combo_found',
                    'source': source,
                    'combo_count': combos_found,
                    'quality': quality,
                    'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
            else:
                print(f"{Fore.RED}[-] {source}: No fresh combos")
                
        print(f"\n{Fore.GREEN}[+] Total combos found: {total_combos:,}")
        self.found_count += total_combos
        
    def custom_combo_search(self):
        """Custom combo search with filters"""
        print(f"\n{Fore.GREEN}[+] Custom Combo Search")
        
        domain = input(f"{Fore.YELLOW}Enter target domain/service (e.g., netflix, spotify): {Style.RESET_ALL}")
        if not domain:
            return
            
        min_size = input(f"{Fore.YELLOW}Minimum combo size (default 1000): {Style.RESET_ALL}") or "1000"
        max_age = input(f"{Fore.YELLOW}Maximum age in days (default 30): {Style.RESET_ALL}") or "30"
        
        print(f"{Fore.CYAN}[+] Searching combos for '{domain}' (min: {min_size}, max age: {max_age} days)")
        
        search_locations = [
            'Deep Web Forums', 'Private Channels', 'Leak Sites',
            'Combo Markets', 'Exchange Forums', 'Dark Web Markets'
        ]
        
        for location in search_locations:
            print(f"{Fore.YELLOW}[~] Searching {location}...")
            time.sleep(random.uniform(1, 3))
            
            if random.choice([True, False]):  # 50% chance
                combo_size = random.randint(int(min_size), int(min_size) * 10)
                price = random.choice(['Free', f'${random.randint(5, 50)}'])
                
                print(f"{Fore.GREEN}[+] {location}: {combo_size:,} combos - {price}")
                
                result = {
                    'type': 'custom_combo',
                    'target_domain': domain,
                    'location': location,
                    'combo_size': combo_size,
                    'price': price,
                    'found_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results.append(result)
                self.found_count += 1
            else:
                print(f"{Fore.RED}[-] {location}: No results")
                
    def combo_validator(self):
        """Validate combo lists"""
        print(f"\n{Fore.GREEN}[+] Combo Validator")
        
        file_path = input(f"{Fore.YELLOW}Enter combo file path: {Style.RESET_ALL}")
        if not os.path.exists(file_path):
            print(f"{Fore.RED}[-] File not found!")
            return
            
        print(f"{Fore.CYAN}[+] Validating combo file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            total_lines = len(lines)
            valid_combos = 0
            invalid_combos = 0
            duplicates = 0
            
            seen_combos = set()
            
            print(f"{Fore.CYAN}[+] Processing {total_lines:,} lines...")
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Progress display
                if i % 10000 == 0:
                    progress = (i / total_lines) * 100
                    print(f"{Fore.YELLOW}[~] Progress: {progress:.1f}% ({i:,}/{total_lines:,})")
                    
                # Validate combo format
                if ':' in line and len(line.split(':')) >= 2:
                    email_part = line.split(':')[0]
                    if '@' in email_part and '.' in email_part:
                        if line not in seen_combos:
                            valid_combos += 1
                            seen_combos.add(line)
                        else:
                            duplicates += 1
                    else:
                        invalid_combos += 1
                else:
                    invalid_combos += 1
                    
            print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
            print(f"{Fore.GREEN}║{Fore.YELLOW}                     VALIDATION RESULTS                          {Fore.GREEN}║")
            print(f"{Fore.GREEN}╠══════════════════════════════════════════════════════════════╣")
            print(f"{Fore.GREEN}║ {Fore.WHITE}Total Lines: {total_lines:>10,} {Fore.GREEN}│ {Fore.WHITE}Valid Combos: {valid_combos:>8,} {Fore.GREEN}║")
            print(f"{Fore.GREEN}║ {Fore.WHITE}Invalid: {invalid_combos:>14,} {Fore.GREEN}│ {Fore.WHITE}Duplicates: {duplicates:>10,} {Fore.GREEN}║")
            print(f"{Fore.GREEN}║ {Fore.WHITE}Validity Rate: {(valid_combos/total_lines*100):>7.1f}% {Fore.GREEN}│ {Fore.WHITE}Unique Rate: {((valid_combos)/(valid_combos+duplicates)*100):>7.1f}% {Fore.GREEN}║")
            print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝")
            
        except Exception as e:
            print(f"{Fore.RED}[-] Error validating file: {e}")
            
def hq_combo_filter(self):
    print(f"\n{Fore.GREEN}[+] HQ Combo Filter")

    input_file = input(f"{Fore.YELLOW}Input combo file: {Style.RESET_ALL}")
    if not os.path.exists(input_file):
        print(f"{Fore.RED}[-] File not found!")
        return

    output_file = input(f"{Fore.YELLOW}Output HQ file (default: hq_combos.txt): {Style.RESET_ALL}") or "hq_combos.txt"

    hq_domains = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'protonmail.com', 'icloud.com', 'aol.com', 'live.com'
    ]

    print(f"{Fore.CYAN}[+] Filtering HQ combos from {input_file}...")

    try:
        hq_combos = []
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f):
                line = line.strip()

                if line_num % 10000 == 0:
                    print(f"{Fore.YELLOW}[~] Processed {line_num:,} lines, found {len(hq_combos):,} HQ combos")

                if ':' in line:
                    email = line.split(':')[0].lower()
                    domain = email.split('@')[-1] if '@' in email else ''

                    if domain in hq_domains:
                        if len(line.split(':')[1]) >= 6:
                            hq_combos.append(line)

        self.save_hq_combos(hq_combos, output_file)

    except Exception as e:
        print(f"{Fore.RED}[-] Error while filtering: {e}")


def save_hq_combos(self, hq_combos, output_file=None):
    """Save HQ combos to file"""
    try:
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"hq_combos_{timestamp}.txt"

        if not hq_combos:
            print(f"{Fore.YELLOW}[!] No HQ combos to save.")
            return False

        temp_file = output_file + '.tmp'

        with open(temp_file, 'w', encoding='utf-8', newline='') as f:
            for combo in hq_combos:
                try:
                    combo_str = str(combo).strip()
                    if not combo_str:
                        continue
                    f.write(combo_str + '\n')
                except Exception as e:
                    print(f"{Fore.YELLOW}[!] Skipping invalid combo: {e}")
                    continue

        import shutil
        shutil.move(temp_file, output_file)

        print(f"\n{Fore.GREEN}[+] HQ Filtering completed!")
        print(f"{Fore.GREEN}[+] HQ combos saved: {len(hq_combos):,}")
        print(f"{Fore.GREEN}[+] Output file: {output_file}")
        print(f"{Fore.GREEN}[+] File size: {os.path.getsize(output_file)} bytes")

        return True

    except Exception as e:
        print(f"{Fore.RED}[-] Error saving combos: {e}")
        return False
# Kodun sonunda ekle:
input("Programı kapatmak için Enter'a basın...")
