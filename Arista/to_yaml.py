import os
import re
import json
import base64
import yaml
import hashlib
import uuid
from datetime import datetime
from urllib.parse import urlparse, unquote

class ClashDumper(yaml.SafeDumper):
    pass

def str_presenter(dumper, data):
    if re.fullmatch(r'[0-9a-f]{2,16}', data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

ClashDumper.add_representer(str, str_presenter)

class ConfigToYAMLConverter:
    def __init__(self):
        self.categories = [
            'vmess', 'vless', 'trojan', 'ss',
            'hysteria2', 'hysteria', 'tuic',
            'wireguard', 'other'
        ]
        self.tiers = [50, 100, 150, 200, 250, 300, 400, 500, "ALL"]

    def read_config_file(self, filepath):
        if not os.path.exists(filepath):
            return []
        configs = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    configs.append(line)
        return configs

    def get_original_tag(self, config_url):
        try:
            if config_url.startswith('ss://'):
                parts = config_url.split('#')
                if len(parts) > 1:
                    return unquote(parts[1]) or ""
                return ""
            elif config_url.startswith('hysteria2://') or config_url.startswith('hy2://'):
                url = urlparse(config_url)
                return unquote(url.fragment) if url.fragment else ""
            elif config_url.startswith('vmess://'):
                try:
                    decoded = base64.b64decode(config_url.replace('vmess://', '')).decode('utf-8')
                    vmess_config = json.loads(decoded)
                    return vmess_config.get('ps', "")
                except:
                    return ""
            elif config_url.startswith('trojan://'):
                url = urlparse(config_url)
                return unquote(url.fragment) if url.fragment else ""
            else:
                url = urlparse(config_url)
                return unquote(url.fragment) if url.fragment else ""
        except:
            return ""

    def decode_ss_config(self, ss_url):
        try:
            if not ss_url.startswith("ss://"):
                return None

            raw = ss_url[5:]
            raw = raw.split("#")[0]
            raw = raw.split("?")[0]

            try:
                padding = "=" * ((4 - len(raw) % 4) % 4)
                decoded = base64.b64decode(raw + padding).decode("utf-8")

                if "@" in decoded:
                    creds, server_port = decoded.rsplit("@", 1)

                    if ":" in creds and ":" in server_port:
                        method, password = creds.split(":", 1)
                        server, port = server_port.rsplit(":", 1)

                        return {
                            "method": method.strip(),
                            "password": password,
                            "server": server.strip(),
                            "port": int(port),
                            "name": self.get_original_tag(ss_url)
                        }
            except:
                pass

            if "@" in raw:
                encoded_part, server_port = raw.rsplit("@", 1)

                try:
                    padding = "=" * ((4 - len(encoded_part) % 4) % 4)
                    decoded = base64.b64decode(
                        encoded_part + padding
                    ).decode("utf-8")

                    method, password = decoded.split(":", 1)
                    server, port = server_port.rsplit(":", 1)

                    return {
                        "method": method.strip(),
                        "password": password,
                        "server": server.strip(),
                        "port": int(port),
                        "name": self.get_original_tag(ss_url)
                    }
                except:
                    pass

            if "@" in raw and ":" in raw:
                creds, server_port = raw.rsplit("@", 1)

                if ":" in creds and ":" in server_port:
                    method, password = creds.split(":", 1)
                    server, port = server_port.rsplit(":", 1)

                    return {
                        "method": method.strip(),
                        "password": password,
                        "server": server.strip(),
                        "port": int(port),
                        "name": self.get_original_tag(ss_url)
                    }

            return None

        except:
            return None

    def decode_vmess_config(self, vmess_url):
        try:
            base64_data = vmess_url.replace('vmess://', '')
            decoded = base64.b64decode(base64_data + '=' * (4 - len(base64_data) % 4)).decode('utf-8')
            return json.loads(decoded)
        except:
            return None

    def build_base_config(self):
        return {
            "mixed-port": 7890,
            "allow-lan": False,
            "mode": "rule",
            "log-level": "info",
            "ipv6": False,
            "dns": {
                "enable": True,
                "listen": "0.0.0.0:1053",
                "ipv6": False,
                "enhanced-mode": "fake-ip",
                "fake-ip-range": "198.18.0.1/16",
                "default-nameserver": [
                    "178.22.122.100",
                    "185.51.200.2",
                    "10.202.10.202"
                ],
                "nameserver": [
                    "https://dns.shecan.ir/dns-query",
                    "https://dns.403.online/dns-query",
                    "https://dns.begzar.ir/dns-query",
                    "tls://dns.shecan.ir",
                    "tls://dns.403.online",
                    "https://1.1.1.1/dns-query",
                    "https://8.8.8.8/dns-query",
                    "tls://1.1.1.1",
                    "tls://8.8.8.8"
                ]
            },
            "sniffer": {
                "enable": True,
                "parse-pure-ip": True,
                "override-destination": True,
                "sniff": {
                    "TLS": {
                        "ports": [443, 8443]
                    },
                    "HTTP": {
                        "ports": [80, 8080, 8880]
                    },
                    "QUIC": {
                        "ports": [443, 8443]
                    }
                }
            },
            "rules": [
                "MATCH,🎯 ARISTA CORE"
            ]
        }

    def vless_to_clashmeta(self, url_str, index):
        try:
            url = urlparse(url_str)
            params = {}
            if url.query:
                for pair in url.query.split('&'):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        params[key] = unquote(value)

            original_name = self.get_original_tag(url_str) or "VLESS"
            config_name = f"{original_name} #{index + 1}"
            
            network_type = params.get('type', 'tcp')
            security = params.get('security', 'none')
            tls_enabled = security in ['tls', 'reality']
            final_server = url.hostname or ''
            final_sni = params.get('sni') or params.get('host') or url.hostname or ''

            config = {
                'name': config_name,
                'type': 'vless',
                'server': final_server,
                'port': int(url.port) if url.port else 443,
                'uuid': url.username or '',
                'network': network_type,
                'tls': tls_enabled,
                'udp': True,
                'skip-cert-verify': True
            }

            if params.get('tcp-fast-open') == 'true':
                config['tcp-fast-open'] = True

            if params.get('flow'):
                config['flow'] = params['flow']

            if params.get('packet-encoding'):
                config['packet-encoding'] = params['packet-encoding']

            if params.get('alpn'):
                config['alpn'] = params['alpn'].split(',')

            if params.get('fp'):
                config['client-fingerprint'] = params['fp']
            elif params.get('client-fingerprint'):
                config['client-fingerprint'] = params['client-fingerprint']

            if tls_enabled and final_sni:
                config['servername'] = final_sni

            if network_type == 'ws':
                ws_opts = {'path': params.get('path', '/')}
                if params.get('host'):
                    ws_opts['headers'] = {'Host': params['host']}
                if params.get('maxEarlyData'):
                    ws_opts['max-early-data'] = int(params['maxEarlyData'])
                if params.get('earlyDataHeaderName'):
                    ws_opts['early-data-header-name'] = params['earlyDataHeaderName']
                config['ws-opts'] = ws_opts

            if network_type == 'grpc':
                if params.get('serviceName'):
                    config['grpc-opts'] = {
                        'grpc-service-name': params['serviceName']
                    }

            if network_type == 'http':
                http_opts = {
                    'method': params.get('method') or 'GET',
                    'path': [params.get('path') or '/']
                }
                if params.get('host'):
                    http_opts['headers'] = {
                        'Host': [params['host']]
                    }
                config['http-opts'] = http_opts

            if security == 'reality' and params.get('pbk'):
                reality_opts = {'public-key': params['pbk']}
                if params.get('sid'):
                    sid = params['sid']
                    if re.match(r'^[0-9a-fA-F]{2,16}$', sid):
                        reality_opts['short-id'] = str(sid.lower())
                if params.get('spider-x'):
                    reality_opts['spider-x'] = params['spider-x']
                config['reality-opts'] = reality_opts

            return config
        except Exception as e:
            return None

    def ss_to_clashmeta(self, ss_url, index):
        decoded = self.decode_ss_config(ss_url)
        if not decoded:
            return None

        password = str(decoded.get("password", "")).strip()
        cipher = str(decoded.get("method", "")).strip()
        server = str(decoded.get("server", "")).strip()
        port = decoded.get("port")

        if not password:
            return None

        if not cipher:
            return None

        if not server:
            return None

        if not isinstance(port, int):
            return None

        if port <= 0 or port > 65535:
            return None

        original_name = decoded.get('name') or "Shadowsocks"
        config_name = f"{original_name} #{index + 1}"

        allowed_ciphers = [
            'aes-128-gcm',
            'aes-192-gcm',
            'aes-256-gcm',
            'aes-128-cfb',
            'aes-192-cfb',
            'aes-256-cfb',
            'chacha20',
            'chacha20-ietf',
            'chacha20-ietf-poly1305',
            'xchacha20-ietf-poly1305',
            '2022-blake3-aes-128-gcm',
            '2022-blake3-aes-256-gcm',
            '2022-blake3-chacha20-poly1305'
        ]

        if cipher not in allowed_ciphers:
            return None

        return {
            'name': config_name,
            'type': 'ss',
            'server': decoded.get('server'),
            'port': decoded.get('port'),
            'cipher': cipher,
            'password': decoded.get('password'),
            'udp': True,
            'tcp-fast-open': True
        }

    def hysteria2_to_clashmeta(self, url_str, index):
        try:
            if url_str.startswith('hy2://'):
                url_str = url_str.replace('hy2://', 'hysteria2://')
            url = urlparse(url_str)
            params = {}
            if url.query:
                for pair in url.query.split('&'):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        params[key] = unquote(value)
            
            original_name = self.get_original_tag(url_str) or "Hysteria2"
            config_name = f"{original_name} #{index + 1}"

            password = url.username or params.get('auth', '')

            config = {
                'name': config_name,
                'type': 'hysteria2',
                'server': url.hostname or '',
                'port': int(url.port) if url.port else 443,
                'password': password,
                'sni': url.hostname or '',
                'skip-cert-verify': True,
                'fast-open': True
            }

            if params.get('sni'):
                config['sni'] = params['sni']

            if params.get('fp'):
                config['client-fingerprint'] = params['fp']
            elif params.get('client-fingerprint'):
                config['client-fingerprint'] = params['client-fingerprint']

            if params.get('obfs') and params.get('obfs-password'):
                config['obfs'] = params['obfs']
                config['obfs-password'] = params['obfs-password']

            if params.get('up') or params.get('down'):
                config['up'] = params.get('up') or '100 Mbps'
                config['down'] = params.get('down') or '100 Mbps'

            if params.get('ports'):
                config['ports'] = params['ports']

            return config
        except:
            return None

    def vmess_to_clashmeta(self, vmess_url, index):
        try:
            vmess_config = self.decode_vmess_config(vmess_url)
            if not vmess_config:
                return None

            original_name = vmess_config.get('ps') or "VMess"
            config_name = f"{original_name} #{index + 1}"

            network_type = vmess_config.get('net', 'tcp')
            tls_enabled = vmess_config.get('tls') == 'tls'

            config = {
                'name': config_name,
                'type': 'vmess',
                'server': vmess_config.get('add') or '',
                'port': int(vmess_config.get('port')) if vmess_config.get('port') else 443,
                'uuid': vmess_config.get('id') or '',
                'alterId': int(vmess_config.get('aid') or 0),
                'cipher': vmess_config.get('scy') or 'auto',
                'network': network_type,
                'tls': tls_enabled,
                'udp': True,
                'skip-cert-verify': True,
                'tcp-fast-open': True
            }

            if vmess_config.get('sni'):
                config['servername'] = vmess_config['sni']
            elif vmess_config.get('add'):
                config['servername'] = vmess_config['add']

            if vmess_config.get('fp'):
                config['client-fingerprint'] = vmess_config['fp']

            if tls_enabled and vmess_config.get('alpn'):
                config['alpn'] = vmess_config['alpn'].split(',')

            if network_type == 'ws':
                ws_opts = {'path': vmess_config.get('path') or '/'}
                if vmess_config.get('host'):
                    ws_opts['headers'] = {'Host': vmess_config['host']}
                config['ws-opts'] = ws_opts

            if network_type == 'h2':
                h2_opts = {'path': vmess_config.get('path') or '/'}
                if vmess_config.get('host'):
                    h2_opts['host'] = [vmess_config['host']]
                config['h2-opts'] = h2_opts

            if network_type == 'grpc':
                config['grpc-opts'] = {
                    'grpc-service-name': vmess_config.get('path') or 'GunService'
                }

            return config
        except:
            return None

    def trojan_to_clashmeta(self, trojan_url, index):
        try:
            url = urlparse(trojan_url)
            params = {}
            if url.query:
                for pair in url.query.split('&'):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        params[key] = unquote(value)
            
            original_name = self.get_original_tag(trojan_url) or "Trojan"
            config_name = f"{original_name} #{index + 1}"

            network_type = params.get('type', 'tcp')

            config = {
                'name': config_name,
                'type': 'trojan',
                'server': url.hostname or '',
                'port': int(url.port) if url.port else 443,
                'password': url.username or '',
                'network': network_type,
                'tls': True,
                'udp': True,
                'skip-cert-verify': True,
                'tcp-fast-open': True
            }

            if params.get('sni'):
                config['servername'] = params['sni']
            elif params.get('host'):
                config['servername'] = params['host']
            else:
                config['servername'] = url.hostname or ''

            if params.get('fp'):
                config['client-fingerprint'] = params['fp']
            elif params.get('client-fingerprint'):
                config['client-fingerprint'] = params['client-fingerprint']

            if params.get('alpn'):
                config['alpn'] = params['alpn'].split(',')

            if network_type == 'grpc':
                config['grpc-opts'] = {
                    'grpc-service-name': params.get('serviceName') or 'GunService'
                }

            if network_type == 'ws':
                ws_opts = {'path': params.get('path') or '/'}
                if params.get('host'):
                    ws_opts['headers'] = {'Host': params['host']}
                elif params.get('sni'):
                    ws_opts['headers'] = {'Host': params['sni']}
                config['ws-opts'] = ws_opts

            return config
        except:
            return None

    def convert_config_to_clashmeta(self, config_str, index):
        if config_str.startswith('vless://'):
            return self.vless_to_clashmeta(config_str, index)
        elif config_str.startswith('ss://'):
            return self.ss_to_clashmeta(config_str, index)
        elif config_str.startswith('hysteria2://') or config_str.startswith('hy2://'):
            return self.hysteria2_to_clashmeta(config_str, index)
        elif config_str.startswith('vmess://'):
            return self.vmess_to_clashmeta(config_str, index)
        elif config_str.startswith('trojan://'):
            return self.trojan_to_clashmeta(config_str, index)
        else:
            return None

    def build_proxy_groups(self, all_proxies):
        proxy_names = [p["name"] for p in all_proxies if p.get("name")]

        if not proxy_names:
            return []

        groups = [
            {
                "name": "🚀 ARISTA LOW LATENCY",
                "type": "url-test",
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "tolerance": 50,
                "lazy": True,
                "timeout": 3000,
                "proxies": proxy_names
            },
            {
                "name": "🎬 ARISTA STREAM",
                "type": "fallback",
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "lazy": True,
                "proxies": proxy_names
            },
            {
                "name": "⚖️ ARISTA BALANCE",
                "type": "load-balance",
                "strategy": "consistent-hashing",
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "lazy": True,
                "proxies": proxy_names
            },
            {
                "name": "🎯 ARISTA CORE",
                "type": "select",
                "proxies": [
                    "🚀 ARISTA LOW LATENCY",
                    "🎬 ARISTA STREAM",
                    "⚖️ ARISTA BALANCE",
                    "DIRECT",
                    "REJECT"
                ]
            }
        ]

        return groups

    def convert_source_configs(self, source_dir, output_dir, source_name):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.makedirs(output_dir, exist_ok=True)

        for category in self.categories:
            cat_dir = os.path.join(source_dir, category)
            if not os.path.exists(cat_dir):
                continue

            all_configs = []
            tier_files = {}
            for tier_file in os.listdir(cat_dir):
                if tier_file.endswith('.txt'):
                    filepath = os.path.join(cat_dir, tier_file)
                    configs = self.read_config_file(filepath)
                    if configs:
                        tier_name = tier_file.replace('.txt', '')
                        tier_files[tier_name] = configs
                        all_configs.extend(configs)

            if not all_configs:
                continue

            converted_by_tier = {}
            for tier_name, configs in tier_files.items():
                converted_configs = []
                for idx, config in enumerate(configs):
                    converted = self.convert_config_to_clashmeta(config, idx)
                    if converted:
                        converted_configs.append(converted)
                if converted_configs:
                    converted_by_tier[tier_name] = converted_configs

            if not converted_by_tier:
                continue

            output_cat_dir = os.path.join(output_dir, category)
            os.makedirs(output_cat_dir, exist_ok=True)

            for tier_name, converted_configs in converted_by_tier.items():
                output_filename = os.path.join(output_cat_dir, f"{tier_name}.yaml")
                proxy_groups = self.build_proxy_groups(converted_configs)
                yaml_content = self.build_base_config()
                yaml_content["proxies"] = converted_configs
                yaml_content["proxy-groups"] = proxy_groups
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {source_name.upper()} - {category.upper()} - Tier {tier_name}\n")
                    f.write(f"# Updated: {timestamp}\n")
                    f.write(f"# Count: {len(converted_configs)}\n\n")
                    yaml.dump(yaml_content, f, Dumper=ClashDumper, default_flow_style=False, allow_unicode=True, sort_keys=False)

        self.convert_all_tiers(source_dir, output_dir, source_name)
        self.generate_summary_yaml(source_dir, output_dir, source_name)

    def convert_all_tiers(self, source_dir, output_dir, source_name):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        all_dir = os.path.join(source_dir, 'ALL')
        if not os.path.exists(all_dir):
            return

        output_all_dir = os.path.join(output_dir, 'ALL')
        os.makedirs(output_all_dir, exist_ok=True)

        for tier_file in os.listdir(all_dir):
            if tier_file.endswith('.txt'):
                filepath = os.path.join(all_dir, tier_file)
                configs = self.read_config_file(filepath)
                if not configs:
                    continue

                tier_name = tier_file.replace('.txt', '')
                converted_configs = []
                for idx, config in enumerate(configs):
                    converted = self.convert_config_to_clashmeta(config, idx)
                    if converted:
                        converted_configs.append(converted)

                if not converted_configs:
                    continue

                output_filename = os.path.join(output_all_dir, f"{tier_name}.yaml")
                proxy_groups = self.build_proxy_groups(converted_configs)
                yaml_content = self.build_base_config()
                yaml_content["proxies"] = converted_configs
                yaml_content["proxy-groups"] = proxy_groups
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {source_name.upper()} - ALL - Tier {tier_name}\n")
                    f.write(f"# Updated: {timestamp}\n")
                    f.write(f"# Count: {len(converted_configs)}\n\n")
                    yaml.dump(yaml_content, f, Dumper=ClashDumper, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def generate_summary_yaml(self, source_dir, output_dir, source_name):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        summary_data = {
            'source': source_name.upper(),
            'updated': timestamp,
            'categories': {}
        }

        for category in self.categories:
            cat_dir = os.path.join(source_dir, category)
            if os.path.exists(cat_dir):
                category_data = {}
                for tier_file in os.listdir(cat_dir):
                    if tier_file.endswith('.txt'):
                        tier_name = tier_file.replace('.txt', '')
                        filepath = os.path.join(cat_dir, tier_file)
                        configs = self.read_config_file(filepath)
                        category_data[tier_name] = len(configs)
                if category_data:
                    summary_data['categories'][category] = category_data

        all_dir = os.path.join(source_dir, 'ALL')
        if os.path.exists(all_dir):
            all_data = {}
            for tier_file in os.listdir(all_dir):
                if tier_file.endswith('.txt'):
                    tier_name = tier_file.replace('.txt', '')
                    filepath = os.path.join(all_dir, tier_file)
                    configs = self.read_config_file(filepath)
                    all_data[tier_name] = len(configs)
            if all_data:
                summary_data['ALL'] = all_data

        output_filename = os.path.join(output_dir, f"{source_name}_summary.yaml")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(f"# {source_name.upper()} YAML Conversion Summary\n")
            f.write(f"# Updated: {timestamp}\n\n")
            yaml.dump(summary_data, f, Dumper=ClashDumper, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def convert_all(self):
        sources = [
            ('configs.txt/combined', 'config.yaml/combined', 'combined'),
            ('configs.txt/telegram', 'config.yaml/telegram', 'telegram'),
            ('configs.txt/github', 'config.yaml/github', 'github')
        ]

        for source_dir, output_dir, source_name in sources:
            if os.path.exists(source_dir):
                self.convert_source_configs(source_dir, output_dir, source_name)

        self.create_master_yaml()

    def create_master_yaml(self):
        output_dir = 'config.yaml'
        os.makedirs(output_dir, exist_ok=True)

        all_proxies = []
        for source in ['combined', 'telegram', 'github']:
            source_dir = os.path.join(output_dir, source)
            if not os.path.exists(source_dir):
                continue

            for category in self.categories:
                cat_dir = os.path.join(source_dir, category)
                if os.path.exists(cat_dir):
                    for yaml_file in os.listdir(cat_dir):
                        if yaml_file.endswith('.yaml'):
                            filepath = os.path.join(cat_dir, yaml_file)
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    lines = content.split('\n')
                                    yaml_start = 0
                                    for i, line in enumerate(lines):
                                        if line.startswith('proxies:'):
                                            yaml_start = i
                                            break
                                    if yaml_start > 0:
                                        yaml_content = '\n'.join(lines[yaml_start:])
                                        data = yaml.safe_load(yaml_content)
                                        if data and 'proxies' in data:
                                            all_proxies.extend(data['proxies'])
                            except:
                                continue

                all_dir = os.path.join(source_dir, 'ALL')
                if os.path.exists(all_dir):
                    for yaml_file in os.listdir(all_dir):
                        if yaml_file.endswith('.yaml'):
                            filepath = os.path.join(all_dir, yaml_file)
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    lines = content.split('\n')
                                    yaml_start = 0
                                    for i, line in enumerate(lines):
                                        if line.startswith('proxies:'):
                                            yaml_start = i
                                            break
                                    if yaml_start > 0:
                                        yaml_content = '\n'.join(lines[yaml_start:])
                                        data = yaml.safe_load(yaml_content)
                                        if data and 'proxies' in data:
                                            all_proxies.extend(data['proxies'])
                            except:
                                continue

        master_file = os.path.join(output_dir, 'master.yaml')
        if all_proxies:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            proxy_groups = self.build_proxy_groups(all_proxies)
            master_content = self.build_base_config()
            master_content["proxies"] = all_proxies
            master_content["proxy-groups"] = proxy_groups
            with open(master_file, 'w', encoding='utf-8') as f:
                f.write(f"# MASTER YAML - ALL CONFIGURATIONS\n")
                f.write(f"# Updated: {timestamp}\n")
                f.write(f"# Total Proxies: {len(all_proxies)}\n\n")
                yaml.dump(master_content, f, Dumper=ClashDumper, default_flow_style=False, allow_unicode=True, sort_keys=False)

def main():
    print("=" * 60)
    print("CONFIG TO YAML (Clash Meta) CONVERTER")
    print("=" * 60)

    try:
        converter = ConfigToYAMLConverter()
        converter.convert_all()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
