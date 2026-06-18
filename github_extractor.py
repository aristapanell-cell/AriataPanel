import requests
import re
import json
import hashlib
import base64
import uuid
from datetime import datetime
from urllib.parse import urlparse
import os

SOURCES = [
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Reality",
    "https://cdn.jsdelivr.net/gh/MahsaNetConfigTopic/config@main/xray_final.txt",
    "https://cdn.jsdelivr.net/gh/4n0nymou3/multi-proxy-config-fetcher@main/configs/proxy_configs.txt",
    "https://raw.githubusercontent.com/parvinxs/Fssociety/refs/heads/main/Fssociety.sub",
    "https://cdn.jsdelivr.net/gh/Firmfox/Proxify@main/v2ray_configs/seperated_by_protocol/other.txt",
    "https://cdn.jsdelivr.net/gh/LowiKLive/BypassWhitelistRu@main/WhiteList-Bypass_Ru.txt",
    "https://cdn.jsdelivr.net/gh/roosterkid/openproxylist@main/V2RAY_RAW.txt",
    "https://gitverse.ru/api/repos/ru-wbl/wl/raw/branch/master/KvRuVPN%2FKvRuVPN.txt",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN_Black_list/raw/branch/master/configs.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt"
]
class GitHubConfigExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_content(self, url):
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except:
            return ""
    
    def extract_configs(self, content):
        patterns = [
            r'(vmess://[A-Za-z0-9+/=]+)',
            r'(vless://[^\s]+)',
            r'(trojan://[^\s]+)',
            r'(ss://[A-Za-z0-9+/=]+)',
            r'(ss://[^\s]+)',
            r'(hysteria2://[^\s]+)',
            r'(hysteria://[^\s]+)',
            r'(hy2://[^\s]+)',
            r'(tuic://[^\s]+)'
        ]
        configs = []
        for pattern in patterns:
            configs.extend(re.findall(pattern, content, re.IGNORECASE))
        return [c for c in configs if not c.strip().startswith('ss://{')]
    
    def standardize_ss(self, config_str):
        try:
            if not config_str.startswith('ss://'):
                return config_str
            
            config_str = config_str.strip()
            
            if '@' in config_str and '#' not in config_str:
                return config_str
            
            parts = config_str.split('#', 1)
            base_part = parts[0][5:]
            
            if len(base_part) % 4 != 0:
                base_part += '=' * (4 - len(base_part) % 4)
            
            try:
                decoded = base64.b64decode(base_part).decode('utf-8')
                if '@' in decoded:
                    method_pass, server = decoded.split('@', 1)
                    encoded_mp = base64.b64encode(method_pass.encode()).decode()
                    result = f"ss://{encoded_mp}@{server}"
                    if len(parts) == 2:
                        result += f"#{parts[1]}"
                    return result
            except:
                pass
            
            return config_str
        except:
            return config_str
    
    def decode_vmess(self, config_str):
        try:
            base64_part = config_str[8:]
            if len(base64_part) % 4 != 0:
                base64_part += '=' * (4 - len(base64_part) % 4)
            return json.loads(base64.b64decode(base64_part).decode('utf-8'))
        except:
            return None
    
    def validate_vmess_dict(self, config_dict):
        required_keys = ['v', 'ps', 'add', 'port', 'id', 'aid']
        if not all(k in config_dict for k in required_keys):
            return False
        try:
            port = int(config_dict['port'])
            if port < 1 or port > 65535:
                return False
            uuid.UUID(config_dict['id'])
        except:
            return False
        return True
    
    def validate_ss(self, config_str):
        try:
            config_str = self.standardize_ss(config_str)
            if not config_str.startswith('ss://'):
                return False
            
            parts = config_str.split('#', 1)
            base_part = parts[0][5:]
            
            if '@' not in base_part:
                return False
            
            encoded_method_pass, server_part = base_part.split('@', 1)
            
            if len(encoded_method_pass) % 4 != 0:
                encoded_method_pass += '=' * (4 - len(encoded_method_pass) % 4)
            
            try:
                decoded_mp = base64.b64decode(encoded_method_pass).decode('utf-8')
                if ':' not in decoded_mp:
                    return False
            except:
                return False
            
            if ':' not in server_part:
                return False
            
            server, port_str = server_part.split(':', 1)
            port = int(port_str)
            if port < 1 or port > 65535:
                return False
            
            return True
        except:
            return False
    
    def validate_config(self, config):
        if isinstance(config, dict):
            return self.validate_vmess_dict(config)
        
        config_str = config
        if config_str.startswith('vmess://'):
            decoded = self.decode_vmess(config_str)
            return decoded and isinstance(decoded, dict) and self.validate_vmess_dict(decoded)
        elif config_str.startswith('vless://'):
            return '#' in config_str and '@' in config_str
        elif config_str.startswith('trojan://'):
            return '#' in config_str and '@' in config_str
        elif config_str.startswith('ss://'):
            return self.validate_ss(config_str)
        elif any(config_str.startswith(proto) for proto in ['hysteria2://','hy2://','hysteria://','tuic://']):
            return True
        return False
    
    def tag_config(self, config, tag="T.ME: @aristapnel"):
        if isinstance(config, dict):
            config['ps'] = tag
            json_str = json.dumps(config, separators=(',', ':'), ensure_ascii=False)
            return 'vmess://' + base64.b64encode(json_str.encode()).decode()
        
        config_str = config
        if config_str.startswith('vmess://'):
            decoded = self.decode_vmess(config_str)
            if decoded and isinstance(decoded, dict):
                decoded['ps'] = tag
                json_str = json.dumps(decoded, separators=(',', ':'), ensure_ascii=False)
                return 'vmess://' + base64.b64encode(json_str.encode()).decode()
            return config_str
        elif '#' in config_str:
            base = config_str.split('#')[0]
            return f"{base}#{tag}"
        else:
            return f"{config_str}#{tag}"
    
    def deduplicate(self, configs):
        unique_configs = []
        seen_hashes = set()
        
        for config in configs:
            normalized = config
            if isinstance(config, str) and config.startswith('vmess://'):
                decoded = self.decode_vmess(config)
                if decoded and isinstance(decoded, dict):
                    decoded_copy = decoded.copy()
                    decoded_copy['ps'] = "TEMP_TAG"
                    normalized = 'vmess://' + base64.b64encode(json.dumps(decoded_copy, separators=(',', ':'), ensure_ascii=False).encode()).decode()
            elif isinstance(config, str):
                normalized = config.split('#',1)[0] if '#' in config else config
            
            config_hash = hashlib.md5(normalized.encode()).hexdigest()
            if config_hash not in seen_hashes:
                seen_hashes.add(config_hash)
                unique_configs.append(config)
        
        return unique_configs
    
    def categorize(self, configs):
        categories = {
            'vmess': [], 'vless': [], 'trojan': [], 'ss': [],
            'hysteria2': [], 'hysteria': [], 'tuic': [], 'other': []
        }
        
        for config in configs:
            if isinstance(config, str):
                if config.startswith('vmess://'):
                    categories['vmess'].append(config)
                elif config.startswith('vless://'):
                    categories['vless'].append(config)
                elif config.startswith('trojan://'):
                    categories['trojan'].append(config)
                elif config.startswith('ss://'):
                    categories['ss'].append(config)
                elif config.startswith('hysteria2://') or config.startswith('hy2://'):
                    categories['hysteria2'].append(config)
                elif config.startswith('hysteria://'):
                    categories['hysteria'].append(config)
                elif config.startswith('tuic://'):
                    categories['tuic'].append(config)
                else:
                    categories['other'].append(config)
        
        return categories
    
    def process_sources(self):
        all_configs = []
        failed_sources = []
        
        print(f"Processing {len(SOURCES)} GitHub sources...")
        
        for i, url in enumerate(SOURCES, 1):
            print(f"[{i}/{len(SOURCES)}] {url}")
            
            content = self.fetch_content(url)
            if content:
                configs = self.extract_configs(content)
                all_configs.extend(configs)
            else:
                failed_sources.append(url)
        
        processed_configs = []
        failed_configs = 0
        
        for config in all_configs:
            if config.startswith('ss://'):
                try:
                    standard_ss = self.standardize_ss(config)
                    if self.validate_config(standard_ss):
                        processed_configs.append(self.tag_config(standard_ss))
                    else:
                        failed_configs += 1
                except:
                    failed_configs += 1
            elif config.startswith('vmess://'):
                decoded = self.decode_vmess(config)
                if decoded and isinstance(decoded, dict) and self.validate_config(decoded):
                    processed_configs.append(self.tag_config(decoded))
                else:
                    failed_configs += 1
            else:
                if self.validate_config(config):
                    processed_configs.append(self.tag_config(config))
                else:
                    failed_configs += 1
        
        unique_configs = self.deduplicate(processed_configs)
        categories = self.categorize(unique_configs)
        
        return categories, len(unique_configs), len(failed_sources), failed_configs
    
    def save_results(self, categories, total_count):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        os.makedirs('configs.txt/github', exist_ok=True)
        
        for category, configs in categories.items():
            if configs:
                filename = f"configs.txt/github/{category}.txt"
                content = f"# GitHub {category.upper()} Configurations\n"
                content += f"# Updated: {timestamp}\n"
                content += f"# Count: {len(configs)}\n"
                content += "# Source: GitHub Repositories\n\n"
                content += "\n".join(configs)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        all_configs = []
        for configs in categories.values():
            all_configs.extend(configs)
        
        if all_configs:
            filename = "configs.txt/github/all.txt"
            content = f"# All GitHub Configurations\n"
            content += f"# Updated: {timestamp}\n"
            content += f"# Total Count: {len(all_configs)}\n"
            content += "# Source: GitHub Repositories\n\n"
            content += "\n".join(all_configs)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return len(all_configs)

def main():
    print("=" * 60)
    print("ARISTA GITHUB CONFIG EXTRACTOR")
    print("=" * 60)
    
    try:
        extractor = GitHubConfigExtractor()
        categories, total_count, failed_sources, failed_configs = extractor.process_sources()
        saved_count = extractor.save_results(categories, total_count)
        
        print(f"\n✅ PROCESSING COMPLETE")
        print(f"Total unique configs: {total_count}")
        print(f"Configs saved: {saved_count}")
        if failed_sources > 0:
            print(f"Failed sources: {failed_sources}")
        if failed_configs > 0:
            print(f"Failed configs: {failed_configs}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
