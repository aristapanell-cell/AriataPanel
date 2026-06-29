import os
import re
import json
import base64
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs, unquote
from collections import defaultdict, Counter

class SmartConfigCombinerV2:
    def __init__(self):
        self.output_dir = "smart_configs"
        self.protocols = ['vless', 'vmess', 'trojan', 'ss']
        self.max_ips = 50

    def load_best_ips(self) -> List[Dict]:
        ip_file = "best_ip/ip_port_cdn_sni_country_type.txt"
        if not os.path.exists(ip_file):
            print("❌ best_ip file not found!")
            return []

        ips = []
        with open(ip_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                ip_data = self.parse_ip_line(line)
                if ip_data and ip_data.get('ip'):
                    ips.append(ip_data)

        return ips[:self.max_ips]

    def parse_ip_line(self, line: str) -> Optional[Dict]:
        ip_data = {}
        patterns = {
            'ip': r'\[IP:\s*([^\]]+)\]',
            'port': r'\[PORT:\s*([^\]]+)\]',
            'score': r'\[SCORE=\s*([^\]]+)\]',
            'ttfb': r'\[TTFB=\s*([^\]]+)\]',
            'proto': r'\[PROTO=\s*([^\]]+)\]',
            'reliability': r'\[REL=\s*([^\]]+)\]',
            'cdn': r'\[CDN=\s*([^\]]+)\]',
            'type': r'\[TYPE=\s*([^\]]+)\]',
            'sni': r'\[SNI=\s*([^\]]+)\]',
            'city': r'\[City=\s*([^\]]+)\]',
            'country': r'\[Country=\s*([^\]]+)\]',
            'provider': r'\[Provider=\s*([^\]]+)\]',
            'asn': r'\[ASN=\s*([^\]]+)\]'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                value = match.group(1).strip()
                if value != '-':
                    ip_data[key] = value

        return ip_data if ip_data.get('ip') else None

    def count_ports_distribution(self, ips: List[Dict]) -> Dict[str, int]:
        port_counts = Counter()
        for ip in ips:
            port = ip.get('port')
            if port:
                port_counts[port] += 1
        return dict(port_counts)

    def load_configs_by_protocol(self) -> Dict[str, List[str]]:
        base_path = "configs.txt/combined"
        configs_by_protocol = defaultdict(list)

        for protocol in self.protocols:
            file_path = os.path.join(base_path, protocol, "ALL.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if not line.startswith('#') and line.strip():
                            configs_by_protocol[protocol].append(line.strip())

        return dict(configs_by_protocol)

    def decode_vmess(self, vmess_url: str) -> Optional[Dict]:
        try:
            data = vmess_url.replace('vmess://', '')
            padding = '=' * ((4 - len(data) % 4) % 4)
            decoded = base64.b64decode(data + padding).decode('utf-8')
            return json.loads(decoded)
        except:
            return None

    def encode_vmess(self, config_dict: Dict) -> str:
        json_str = json.dumps(config_dict, separators=(',', ':'), ensure_ascii=False)
        return 'vmess://' + base64.b64encode(json_str.encode()).decode()

    def get_config_port(self, config: str, protocol: str) -> Optional[str]:
        try:
            if protocol == 'vmess':
                decoded = self.decode_vmess(config)
                if decoded and 'port' in decoded:
                    return str(decoded['port'])

            elif protocol in ['vless', 'trojan']:
                parsed = urlparse(config)
                if parsed.port:
                    return str(parsed.port)

            elif protocol == 'ss':
                if '@' in config:
                    parts = config.split('@')
                    if len(parts) == 2:
                        server_part = parts[1].split('#')[0]
                        if ':' in server_part:
                            _, port = server_part.split(':')
                            return port.strip()
        except:
            pass
        return None

    def filter_configs_by_port(self, configs: List[str], protocol: str, target_port: str) -> List[str]:
        filtered = []
        for config in configs:
            config_port = self.get_config_port(config, protocol)
            if config_port == target_port:
                filtered.append(config)
        return filtered

    def process_protocol(self, protocol: str, configs: List[str], port_distribution: Dict[str, int]) -> List[str]:
        if not configs:
            return []

        final_configs = []
        used_configs = set()

        print(f"\n  📊 Processing {protocol.upper()}:")

        for port, count in port_distribution.items():
            port_configs = self.filter_configs_by_port(configs, protocol, port)
            available_configs = [c for c in port_configs if c not in used_configs]
            available_count = len(available_configs)
            take_count = min(count, available_count)

            if take_count > 0:
                selected = available_configs[:take_count]
                final_configs.extend(selected)
                used_configs.update(selected)
                print(f"    Port {port}: {take_count}/{count} configs (available: {available_count})")
            else:
                print(f"    Port {port}: 0/{count} configs (no configs with this port)")

        remaining_configs = [c for c in configs if c not in used_configs]
        if remaining_configs and len(final_configs) < self.max_ips:
            need = self.max_ips - len(final_configs)
            take = min(need, len(remaining_configs))
            if take > 0:
                final_configs.extend(remaining_configs[:take])
                print(f"    Extra: {take} configs from remaining pool")

        return final_configs[:self.max_ips]

    def replace_ip_and_port(self, config: str, protocol: str, ip_data: Dict) -> str:
        try:
            if protocol == 'vmess':
                decoded = self.decode_vmess(config)
                if decoded:
                    decoded['add'] = ip_data['ip']
                    decoded['port'] = int(ip_data['port'])
                    return self.encode_vmess(decoded)

            elif protocol == 'vless':
                parsed = urlparse(config)
                netloc = f"{parsed.username}@{ip_data['ip']}:{ip_data['port']}"
                new_url = f"{parsed.scheme}://{netloc}"
                if parsed.query:
                    new_url += f"?{parsed.query}"
                if parsed.fragment:
                    new_url += f"#{parsed.fragment}"
                return new_url

            elif protocol == 'trojan':
                parsed = urlparse(config)
                netloc = f"{parsed.username}@{ip_data['ip']}:{ip_data['port']}"
                new_url = f"{parsed.scheme}://{netloc}"
                if parsed.query:
                    new_url += f"?{parsed.query}"
                if parsed.fragment:
                    new_url += f"#{parsed.fragment}"
                return new_url

            elif protocol == 'ss':
                parts = config.split('@')
                if len(parts) == 2:
                    method_pass = parts[0].replace('ss://', '')
                    new_config = f"ss://{method_pass}@{ip_data['ip']}:{ip_data['port']}"
                    if '#' in config:
                        tag = config.split('#')[1]
                        new_config += f"#{tag}"
                    return new_config

        except Exception as e:
            print(f"Error replacing IP/Port: {e}")

        return config

    def replace_sni(self, config: str, protocol: str, ip_data: Dict) -> str:
        try:
            sni = ip_data.get('sni', ip_data['ip'])
            if not sni or sni == '-':
                sni = ip_data.get('cdn', ip_data['ip'])

            if protocol == 'vmess':
                decoded = self.decode_vmess(config)
                if decoded:
                    decoded['sni'] = sni
                    if 'host' in decoded:
                        decoded['host'] = sni
                    return self.encode_vmess(decoded)

            elif protocol == 'vless':
                parsed = urlparse(config)
                params = parse_qs(parsed.query)
                params['sni'] = [sni]
                if 'host' in params:
                    params['host'] = [sni]
                new_query = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
                netloc = f"{parsed.username}@{ip_data['ip']}:{ip_data['port']}"
                new_url = f"{parsed.scheme}://{netloc}?{new_query}"
                if parsed.fragment:
                    new_url += f"#{parsed.fragment}"
                return new_url

            elif protocol == 'trojan':
                parsed = urlparse(config)
                params = parse_qs(parsed.query)
                params['sni'] = [sni]
                if 'host' in params:
                    params['host'] = [sni]
                new_query = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
                netloc = f"{parsed.username}@{ip_data['ip']}:{ip_data['port']}"
                new_url = f"{parsed.scheme}://{netloc}?{new_query}"
                if parsed.fragment:
                    new_url += f"#{parsed.fragment}"
                return new_url

        except Exception as e:
            print(f"Error replacing SNI: {e}")

        return config

    def add_arista_tag(self, config: str, protocol: str, ip_data: Dict) -> str:
        tag = f"ARISTA ULTRA - {ip_data.get('country', 'UNK')} - {ip_data.get('provider', 'UNK')}"

        try:
            if protocol == 'vmess':
                decoded = self.decode_vmess(config)
                if decoded:
                    decoded['ps'] = tag
                    return self.encode_vmess(decoded)

            elif protocol in ['vless', 'trojan']:
                if '#' in config:
                    base = config.split('#')[0]
                    return f"{base}#{tag}"
                else:
                    return f"{config}#{tag}"

            elif protocol == 'ss':
                if '#' in config:
                    base = config.split('#')[0]
                    return f"{base}#{tag}"
                else:
                    return f"{config}#{tag}"

        except:
            pass

        return config

    def smart_combine(self):
        print("=" * 60)
        print("SMART CONFIG COMBINER V2 - ARISTA ULTRA")
        print("=" * 60)

        print("\n📡 Loading 50 best IPs...")
        best_ips = self.load_best_ips()
        print(f"✅ Loaded {len(best_ips)} best IPs")

        if not best_ips:
            print("❌ No IPs found!")
            return

        print("\n📊 Port distribution in 50 IPs:")
        port_distribution = self.count_ports_distribution(best_ips)
        for port, count in sorted(port_distribution.items(), key=lambda x: int(x[0])):
            print(f"  Port {port}: {count} IPs")

        print("\n📡 Loading configs...")
        configs_by_protocol = self.load_configs_by_protocol()
        for protocol, configs in configs_by_protocol.items():
            print(f"  {protocol}: {len(configs)} configs")

        print("\n🔄 Processing protocols based on port distribution...")
        results = {}
        all_configs = []

        for protocol in self.protocols:
            configs = configs_by_protocol.get(protocol, [])
            processed = self.process_protocol(protocol, configs, port_distribution)

            if processed:
                combined = []
                for i, config in enumerate(processed):
                    config_port = self.get_config_port(config, protocol)
                    matching_ip = None
                    for ip in best_ips:
                        if ip.get('port') == config_port and ip not in combined:
                            matching_ip = ip
                            break

                    if matching_ip:
                        config = self.replace_ip_and_port(config, protocol, matching_ip)
                        config = self.replace_sni(config, protocol, matching_ip)
                        config = self.add_arista_tag(config, protocol, matching_ip)
                        combined.append(config)

                if combined:
                    results[protocol] = combined
                    all_configs.extend(combined)
                    print(f"  ✅ {protocol}: {len(combined)} configs")
            else:
                print(f"  ⚠️ {protocol}: No configs processed")

        self.save_results(results, all_configs)

        print("\n" + "=" * 60)
        print("✅ SMART COMBINER COMPLETED!")
        print("=" * 60)

    def save_results(self, results: Dict, all_configs: List[str]):
        os.makedirs(self.output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for protocol, configs in results.items():
            if not configs:
                continue

            txt_file = os.path.join(self.output_dir, f"{protocol}_smart.txt")
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"# ARISTA ULTRA - SMART {protocol.upper()} CONFIGS\n")
                f.write(f"# Updated: {timestamp}\n")
                f.write(f"# Count: {len(configs)}\n")
                f.write(f"# Tag: ARISTA ULTRA\n\n")
                f.write('\n'.join(configs))

            print(f"  ✅ Saved: {protocol}_smart.txt ({len(configs)} configs)")

        if all_configs:
            all_file = os.path.join(self.output_dir, "all_smart.txt")
            with open(all_file, 'w', encoding='utf-8') as f:
                f.write(f"# ARISTA ULTRA - ALL SMART CONFIGS\n")
                f.write(f"# Updated: {timestamp}\n")
                f.write(f"# Total Count: {len(all_configs)}\n")
                f.write(f"# Protocols: {', '.join(self.protocols)}\n")
                f.write(f"# Tag: ARISTA ULTRA\n\n")
                f.write('\n'.join(all_configs))

            print(f"  ✅ Saved: all_smart.txt ({len(all_configs)} configs)")

def main():
    combiner = SmartConfigCombinerV2()
    combiner.smart_combine()

if __name__ == "__main__":
    main()
