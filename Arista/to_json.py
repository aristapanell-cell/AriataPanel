import os
import re
import json
import base64
import uuid
from datetime import datetime
from urllib.parse import urlparse, parse_qs, unquote
from typing import Optional, Dict, Any, List

class ConfigToJSONConverter:
    def __init__(self):
        self.categories = [
            'vmess', 'vless', 'trojan', 'ss',
            'hysteria2', 'hysteria', 'tuic',
            'wireguard', 'other'
        ]
        self.tiers = [50, 100, 150, 200, 250, 300, 400, 500, "ALL"]
        self.uuid_re = re.compile(
            r"^[0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{12}$"
        )
        self.allowed_ss_ciphers = {
            "aes-128-gcm", "aes-256-gcm", "chacha20-ietf-poly1305",
            "aes-128-cfb", "aes-256-cfb", "chacha20", "chacha20-ietf",
            "2022-blake3-aes-128-gcm", "2022-blake3-aes-256-gcm",
            "2022-blake3-chacha20-poly1305"
        }
        self.allowed_fp = {
            "chrome", "firefox", "safari", "ios", "android",
            "edge", "qq", "random", "randomized"
        }

    def clean_host(self, value: str) -> str:
        if not value:
            return ""
        value = unquote(value)
        md = re.match(r'\[(.*?)\]\((.*?)\)', value)
        if md:
            return md.group(1)
        value = value.replace("http://", "")
        value = value.replace("https://", "")
        value = value.strip("/")
        return value

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

    def safe_b64_decode(self, data: str) -> Optional[str]:
        try:
            data = data.replace("-", "+").replace("_", "/")
            data += "=" * (-len(data) % 4)
            return base64.b64decode(data).decode("utf-8", errors="ignore")
        except:
            return None

    def get_first(self, qs: Dict, key: str, default: Any = None) -> Any:
        values = qs.get(key, [])
        return values[0] if values else default

    def build_tls(self, qs: Dict, host: str) -> Dict:
        security = self.get_first(qs, "security", "none")
        if security not in ("tls", "reality"):
            return {"enabled": False}
        fp = self.get_first(qs, "fp", "chrome")
        if fp not in self.allowed_fp:
            fp = "chrome"
        tls = {
            "enabled": True,
            "server_name": self.clean_host(self.get_first(qs, "sni", host)),
            "insecure": True,
            "utls": {
                "enabled": True,
                "fingerprint": fp
            }
        }
        alpn = self.get_first(qs, "alpn")
        if alpn:
            tls["alpn"] = [
                unquote(a.strip())
                for a in alpn.split(",")
                if a.strip()
            ]
        if security == "reality":
            pbk = self.get_first(qs, "pbk")
            if not pbk:
                return {"enabled": False}
            reality = {
                "enabled": True,
                "public_key": pbk
            }
            sid = self.get_first(qs, "sid")
            if sid:
                reality["short_id"] = sid.lower()
            tls["reality"] = reality
        return tls

    def build_transport_vless(self, qs: Dict, host: str) -> Optional[Dict]:
        network = self.get_first(qs, "type", "tcp")
        if network == "ws":
            return {
                "type": "ws",
                "path": unquote(self.get_first(qs, "path", "/")),
                "headers": {"Host": self.clean_host(self.get_first(qs, "host", host))}
            }
        elif network == "grpc":
            return {
                "type": "grpc",
                "service_name": unquote(self.get_first(qs, "serviceName", "GunService"))
            }
        elif network == "http":
            return {
                "type": "http",
                "host": [self.clean_host(self.get_first(qs, "host", host))],
                "path": unquote(self.get_first(qs, "path", "/"))
            }
        return None

    def build_transport_vmess(self, c: Dict) -> Optional[Dict]:
        network = c.get("net", "tcp")
        if network == "ws":
            return {
                "type": "ws",
                "path": unquote(c.get("path", "/")),
                "headers": {"Host": self.clean_host(c.get("host", c["add"]))}
            }
        elif network in ("h2", "http"):
            return {
                "type": "http",
                "host": [self.clean_host(c.get("host", c["add"]))],
                "path": unquote(c.get("path", "/"))
            }
        elif network == "grpc":
            return {
                "type": "grpc",
                "service_name": unquote(c.get("path", "GunService").lstrip("/"))
            }
        return None

    def build_transport_trojan(self, qs: Dict, host: str) -> Optional[Dict]:
        network = self.get_first(qs, "type", "tcp")
        if network == "ws":
            return {
                "type": "ws",
                "path": unquote(self.get_first(qs, "path", "/")),
                "headers": {"Host": self.clean_host(self.get_first(qs, "sni", host))}
            }
        elif network == "grpc":
            return {
                "type": "grpc",
                "service_name": unquote(self.get_first(qs, "serviceName", "GunService"))
            }
        return None

    def decode_ss_config(self, ss_url: str) -> Optional[Dict]:
        try:
            raw = ss_url.replace("ss://", "").split("#")[0]
            name = unquote(ss_url.split("#", 1)[1]) if "#" in ss_url else ""

            def build_result(method, password, server, port):
                if not method or not password or not server or not port:
                    return None
                if method not in self.allowed_ss_ciphers:
                    return None
                if not str(port).isdigit():
                    return None
                password = str(password).strip()
                if len(password) < 2:
                    return None
                return {
                    "method": method,
                    "password": password,
                    "server": server,
                    "port": int(port),
                    "name": name
                }

            try:
                decoded_full = self.safe_b64_decode(raw.split("@")[0])
                if decoded_full and "@" in decoded_full:
                    mp, sp = decoded_full.split("@", 1)
                    if ":" in mp and ":" in sp:
                        method, password = mp.split(":", 1)
                        server, port = sp.split(":", 1)
                        result = build_result(method, password, server, port)
                        if result:
                            return result
            except:
                pass

            if "@" in raw and ":" in raw.split("@")[0]:
                try:
                    method_password, server_port = raw.split("@", 1)
                    method, password = method_password.split(":", 1)
                    server, port = server_port.split(":", 1)
                    result = build_result(method, password, server, port)
                    if result:
                        return result
                except:
                    pass

            if raw.startswith("method:") or ("@" in raw and ":" in raw):
                method_password, server_port = raw.split("@", 1)
                if ":" in method_password:
                    method, password = method_password.split(":", 1)
                    server, port = server_port.split(":", 1)
                    result = build_result(method, password, server, port)
                    if result:
                        return result

            return None
        except:
            return None

    def decode_vmess(self, raw: str) -> Optional[Dict]:
        try:
            data = raw.replace("vmess://", "")
            decoded = base64.b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="ignore")
            obj = json.loads(decoded)
            if "add" not in obj and "host" in obj:
                obj["add"] = obj["host"]
            return obj
        except:
            return None

    def vless_to_singbox(self, index: int, raw: str) -> Optional[Dict]:
        try:
            if not raw.startswith("vless://"):
                return None
            parsed = urlparse(raw)
            qs = parse_qs(parsed.query)
            if not all([parsed.hostname, parsed.port, parsed.username]):
                return None
            if not self.uuid_re.match(parsed.username):
                return None
            name = f"{unquote(parsed.fragment or 'VLESS')} #{index + 1}"
            config = {
                "type": "vless",
                "tag": name,
                "server": parsed.hostname,
                "server_port": int(parsed.port),
                "uuid": parsed.username,
                "tls": self.build_tls(qs, parsed.hostname)
            }
            flow = self.get_first(qs, "flow")
            if flow in ["xtls-rprx-vision", "xtls-rprx-udp443", "xtls-rprx"]:
                config["flow"] = flow
            packet_encoding = self.get_first(qs, "packetEncoding")
            if packet_encoding:
                config["packet_encoding"] = packet_encoding
            transport = self.build_transport_vless(qs, parsed.hostname)
            if transport:
                config["transport"] = transport
            return config
        except Exception as e:
            return None

    def ss_to_singbox(self, index: int, raw: str) -> Optional[Dict]:
        try:
            if not raw.startswith("ss://"):
                return None

            d = self.decode_ss_config(raw)
            if not d:
                return None

            password = str(d.get("password", "")).strip()
            if not password or len(password) < 2:
                return None

            method = d.get("method", "")
            if method not in self.allowed_ss_ciphers:
                return None

            server = d.get("server", "")
            port = d.get("port", None)

            if not server or not port or not str(port).isdigit():
                return None

            return {
                "type": "shadowsocks",
                "tag": f"{d.get('name') or 'SS'} #{index + 1}",
                "server": server,
                "server_port": int(port),
                "method": method,
                "password": password
            }
        except:
            return None

    def vmess_to_singbox(self, index: int, raw: str) -> Optional[Dict]:
        try:
            if not raw.startswith("vmess://"):
                return None
            c = self.decode_vmess(raw)
            if not c:
                return None
            if not all(k in c for k in ("add", "port", "id")):
                return None
            name = f"{c.get('ps', 'VMess')} #{index + 1}"
            config = {
                "type": "vmess",
                "tag": name,
                "server": c["add"],
                "server_port": int(c["port"]),
                "uuid": c["id"],
                "security": c.get("scy", "auto")
            }
            aid = int(c.get("aid", 0))
            if aid > 0:
                config["alter_id"] = aid
            tls_qs = {}
            if c.get("tls") == "tls":
                tls_qs["security"] = ["tls"]
                if c.get("sni"):
                    tls_qs["sni"] = [c["sni"]]
                if c.get("fp"):
                    tls_qs["fp"] = [c["fp"]]
                if c.get("alpn"):
                    tls_qs["alpn"] = [c["alpn"]]
            config["tls"] = self.build_tls(tls_qs, c["add"])
            transport = self.build_transport_vmess(c)
            if transport:
                config["transport"] = transport
            return config
        except Exception as e:
            return None

    def trojan_to_singbox(self, index: int, raw: str) -> Optional[Dict]:
        try:
            if not raw.startswith("trojan://"):
                return None
            p = urlparse(raw)
            q = parse_qs(p.query)
            if not all([p.hostname, p.port, p.username]):
                return None
            name = f"{unquote(p.fragment or 'Trojan')} #{index + 1}"
            config = {
                "type": "trojan",
                "tag": name,
                "server": p.hostname,
                "server_port": int(p.port),
                "password": unquote(p.username),
                "tls": self.build_tls(q, p.hostname)
            }
            transport = self.build_transport_trojan(q, p.hostname)
            if transport:
                config["transport"] = transport
            return config
        except Exception as e:
            return None

    def hysteria2_to_singbox(self, index: int, raw: str) -> Optional[Dict]:
        try:
            if not (raw.startswith("hysteria2://") or raw.startswith("hy2://")):
                return None
            raw = raw.replace("hy2://", "hysteria2://")
            p = urlparse(raw)
            q = parse_qs(p.query)
            if not all([p.hostname, p.port]):
                return None
            name = f"{unquote(p.fragment or 'Hysteria2')} #{index + 1}"
            tls_config = self.build_tls(q, p.hostname)
            if not tls_config.get("enabled", False):
                tls_config = {
                    "enabled": True,
                    "server_name": p.hostname,
                    "insecure": True,
                }
            config = {
                "type": "hysteria2",
                "tag": name,
                "server": p.hostname,
                "server_port": int(p.port),
                "password": unquote(p.username or ""),
                "tls": tls_config
            }
            obfs = self.get_first(q, "obfs")
            obfs_pass = self.get_first(q, "obfs-password")
            if obfs and obfs_pass:
                config["obfs"] = {
                    "type": obfs,
                    "password": unquote(obfs_pass)
                }
            up = self.get_first(q, "up")
            down = self.get_first(q, "down")
            if up:
                config["up"] = up
            if down:
                config["down"] = down
            ports = self.get_first(q, "ports")
            if ports:
                config["ports"] = ports
            return config
        except Exception as e:
            return None

    def build_proxy_groups(self, all_proxies):
        proxy_tags = [p["tag"] for p in all_proxies if p.get("tag")]

        if not proxy_tags:
            return []

        return [
            {
                "type": "urltest",
                "tag": "🚀 ARISTA AUTO BEST",
                "outbounds": proxy_tags,
                "url": "http://www.gstatic.com/generate_204",
                "interval": "2m",
                "tolerance": 30,
                "idle_timeout": "20m",
                "interrupt_exist_connections": True
            },
            {
                "type": "urltest",
                "tag": "🎯 ARISTA MANUAL TESTED",
                "outbounds": proxy_tags,
                "url": "http://www.gstatic.com/generate_204",
                "interval": "3m",
                "tolerance": 50,
                "idle_timeout": "20m",
                "interrupt_exist_connections": True
            }
        ]

    def convert_config_to_singbox(self, config_str: str, index: int) -> Optional[Dict]:
        if config_str.startswith('vless://'):
            return self.vless_to_singbox(index, config_str)
        elif config_str.startswith('ss://'):
            return self.ss_to_singbox(index, config_str)
        elif config_str.startswith('hysteria2://') or config_str.startswith('hy2://'):
            return self.hysteria2_to_singbox(index, config_str)
        elif config_str.startswith('vmess://'):
            return self.vmess_to_singbox(index, config_str)
        elif config_str.startswith('trojan://'):
            return self.trojan_to_singbox(index, config_str)
        else:
            return None

    def build_singbox_config(self, proxies: List[Dict]) -> Dict:
        if not proxies:
            return {
                "log": {
                    "level": "info",
                    "timestamp": True
                },
                "inbounds": [],
                "outbounds": [
                    {
                        "type": "direct",
                        "tag": "direct"
                    }
                ],
                "route": {
                    "final": "direct",
                    "rules": []
                }
            }

        cleaned_proxies = [
            dict(p)
            for p in proxies
            if isinstance(p, dict)
        ]

        proxy_groups = self.build_proxy_groups(cleaned_proxies)

        return {
            "log": {
                "level": "info",
                "timestamp": True
            },

            "dns": {
                "servers": [
                    {
                        "type": "udp",
                        "tag": "google",
                        "server": "8.8.8.8"
                    },
                    {
                        "type": "udp",
                        "tag": "google2",
                        "server": "8.8.4.4"
                    },
                    {
                        "type": "local",
                        "tag": "local"
                    }
                ],

                "rules": [
                    {
                        "domain": [
                            "geosite:private"
                        ],
                        "action": "route",
                        "server": "local"
                    }
                ],

                "final": "google"
            },

            "inbounds": [
                {
                    "type": "tun",
                    "tag": "tun-in",
                    "interface_name": "singbox-tun",
                    "address": [
                        "172.19.0.1/30",
                        "fdfe:dcba:9876::1/126"
                    ],
                    "auto_route": True,
                    "strict_route": True,
                    "stack": "mixed"
                }
            ],

            "outbounds": (
                cleaned_proxies
                + [
                    {
                        "type": "direct",
                        "tag": "direct"
                    },
                    {
                        "type": "block",
                        "tag": "block"
                    }
                ]
                + proxy_groups
            ),

            "route": {
                "auto_detect_interface": True,

                "default_domain_resolver": {
                    "server": "google",
                    "strategy": "prefer_ipv4"
                },

                "final": "🚀 ARISTA AUTO BEST",

                "rules": [
                    {
                        "action": "sniff",
                    },
                    {
                        "protocol": "dns",
                        "action": "hijack-dns"
                    }
                ]
            }
        }

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
                    converted = self.convert_config_to_singbox(config, idx)
                    if converted:
                        converted_configs.append(converted)
                if converted_configs:
                    converted_by_tier[tier_name] = converted_configs
            if not converted_by_tier:
                continue
            output_cat_dir = os.path.join(output_dir, category)
            os.makedirs(output_cat_dir, exist_ok=True)
            for tier_name, converted_configs in converted_by_tier.items():
                full_config = self.build_singbox_config(converted_configs)
                output_filename = os.path.join(output_cat_dir, f"{tier_name}.json")
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(f"// {source_name.upper()} - {category.upper()} - Tier {tier_name}\n")
                    f.write(f"// Updated: {timestamp}\n")
                    f.write(f"// Count: {len(converted_configs)}\n\n")
                    json.dump(full_config, f, indent=2, ensure_ascii=False)
        self.convert_all_tiers(source_dir, output_dir, source_name)
        self.generate_summary_json(source_dir, output_dir, source_name)

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
                    converted = self.convert_config_to_singbox(config, idx)
                    if converted:
                        converted_configs.append(converted)
                if not converted_configs:
                    continue
                full_config = self.build_singbox_config(converted_configs)
                output_filename = os.path.join(output_all_dir, f"{tier_name}.json")
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(f"// {source_name.upper()} - ALL - Tier {tier_name}\n")
                    f.write(f"// Updated: {timestamp}\n")
                    f.write(f"// Count: {len(converted_configs)}\n\n")
                    json.dump(full_config, f, indent=2, ensure_ascii=False)

    def generate_summary_json(self, source_dir, output_dir, source_name):
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
        output_filename = os.path.join(output_dir, f"{source_name}_summary.json")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(f"// {source_name.upper()} JSON Conversion Summary\n")
            f.write(f"// Updated: {timestamp}\n\n")
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

    def convert_all(self):
        sources = [
            ('configs.txt/combined', 'config.json/combined', 'combined'),
            ('configs.txt/telegram', 'config.json/telegram', 'telegram'),
            ('configs.txt/github', 'config.json/github', 'github')
        ]
        for source_dir, output_dir, source_name in sources:
            if os.path.exists(source_dir):
                self.convert_source_configs(source_dir, output_dir, source_name)
        self.create_master_json()

    def create_master_json(self):
        output_dir = 'config.json'
        os.makedirs(output_dir, exist_ok=True)
        all_proxies = []
        for source in ['combined', 'telegram', 'github']:
            source_dir = os.path.join(output_dir, source)
            if not os.path.exists(source_dir):
                continue
            for category in self.categories:
                cat_dir = os.path.join(source_dir, category)
                if os.path.exists(cat_dir):
                    for json_file in os.listdir(cat_dir):
                        if json_file.endswith('.json'):
                            filepath = os.path.join(cat_dir, json_file)
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    json_start = content.find('{')
                                    if json_start > 0:
                                        json_content = content[json_start:]
                                        data = json.loads(json_content)
                                        if data and 'outbounds' in data:
                                            for outbound in data['outbounds']:
                                                if outbound.get('type') in ['vless', 'vmess', 'trojan', 'shadowsocks', 'hysteria2']:
                                                    all_proxies.append(outbound)
                            except:
                                continue
                all_dir = os.path.join(source_dir, 'ALL')
                if os.path.exists(all_dir):
                    for json_file in os.listdir(all_dir):
                        if json_file.endswith('.json'):
                            filepath = os.path.join(all_dir, json_file)
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    json_start = content.find('{')
                                    if json_start > 0:
                                        json_content = content[json_start:]
                                        data = json.loads(json_content)
                                        if data and 'outbounds' in data:
                                            for outbound in data['outbounds']:
                                                if outbound.get('type') in ['vless', 'vmess', 'trojan', 'shadowsocks', 'hysteria2']:
                                                    all_proxies.append(outbound)
                            except:
                                continue
        master_file = os.path.join(output_dir, 'master.json')
        if all_proxies:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_config = self.build_singbox_config(all_proxies)
            with open(master_file, 'w', encoding='utf-8') as f:
                f.write(f"// MASTER JSON - ALL CONFIGURATIONS\n")
                f.write(f"// Updated: {timestamp}\n")
                f.write(f"// Total Proxies: {len(all_proxies)}\n\n")
                json.dump(full_config, f, indent=2, ensure_ascii=False)

def main():
    print("=" * 60)
    print("CONFIG TO JSON (Sing-Box) CONVERTER")
    print("=" * 60)
    try:
        converter = ConfigToJSONConverter()
        converter.convert_all()
        print("\n✅ JSON conversion completed successfully")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
