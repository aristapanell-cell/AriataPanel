import os
import re
import json
import requests
from datetime import datetime

class BestIPProcessor:
    def __init__(self):
        self.output_dir = "best_ip"
        self.source_url = "https://github.com/aristapanell-cell/ARISTA-MATRIX-PIPELINE/raw/refs/heads/main/output/best_ips.txt"
        self.fields = ['ip', 'port', 'cdn', 'sni', 'country', 'type', 'city', 'provider', 'score', 'ttfb', 'proto', 'reliability', 'tcp']
        
    def ensure_output_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)
        
    def fetch_data(self):
        try:
            print(f"Fetching data from: {self.source_url}")
            response = requests.get(self.source_url, timeout=30)
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                content = response.text
                print(f"Content length: {len(content)} characters")
                print(f"First 200 chars: {content[:200]}")
                return content
            else:
                print(f"Failed to fetch data: HTTP {response.status_code}")
                return ""
        except Exception as e:
            print(f"Error fetching data: {e}")
            return ""
    
    def parse_line(self, line):
        data = {}
        
        ip_match = re.search(r'\[IP:\s*([^\]]+)\]', line)
        if ip_match:
            data['ip'] = ip_match.group(1).strip()
        
        port_match = re.search(r'\[PORT:\s*([^\]]+)\]', line)
        if port_match:
            data['port'] = port_match.group(1).strip()
        
        score_match = re.search(r'\[SCORE=\s*([^\]]+)\]', line)
        if score_match:
            data['score'] = score_match.group(1).strip()
        
        tcp_match = re.search(r'\[TCP=\s*([^\]]+)\]', line)
        if tcp_match:
            data['tcp'] = tcp_match.group(1).strip()
        
        ttfb_match = re.search(r'\[TTFB=\s*([^\]]+)\]', line)
        if ttfb_match:
            data['ttfb'] = ttfb_match.group(1).strip()
        
        proto_match = re.search(r'\[PROTO=\s*([^\]]+)\]', line)
        if proto_match:
            data['proto'] = proto_match.group(1).strip()
        
        rel_match = re.search(r'\[REL=\s*([^\]]+)\]', line)
        if rel_match:
            data['reliability'] = rel_match.group(1).strip()
        
        cdn_match = re.search(r'\[CDN=\s*([^\]]+)\]', line)
        if cdn_match:
            data['cdn'] = cdn_match.group(1).strip()
        
        type_match = re.search(r'\[TYPE=\s*([^\]]+)\]', line)
        if type_match:
            data['type'] = type_match.group(1).strip()
        
        sni_match = re.search(r'\[SNI=\s*([^\]]+)\]', line)
        if sni_match:
            data['sni'] = sni_match.group(1).strip()
        
        city_match = re.search(r'\[City=\s*([^\]]+)\]', line)
        if city_match:
            data['city'] = city_match.group(1).strip()
        
        country_match = re.search(r'\[Country=\s*([^\]]+)\]', line)
        if country_match:
            data['country'] = country_match.group(1).strip()
        
        provider_match = re.search(r'\[Provider=\s*([^\]]+)\]', line)
        if provider_match:
            data['provider'] = provider_match.group(1).strip()
        
        return data if data.get('ip') else None
    
    def sort_key(self, item):
        tcp_val = float(item.get('tcp', '999ms').replace('ms', '')) if item.get('tcp') and item.get('tcp') != '-' else 999
        score_val = float(item.get('score', '0')) if item.get('score') and item.get('score') != '-' else 0
        ttfb_val = float(item.get('ttfb', '9999ms').replace('ms', '')) if item.get('ttfb') and item.get('ttfb') != '-' else 9999
        rel_val = float(item.get('reliability', '0')) if item.get('reliability') and item.get('reliability') != '-' else 0
        proto_val = 2 if 'http/2' in item.get('proto', '').lower() else 1 if 'http/1.1' in item.get('proto', '').lower() else 0
        return (tcp_val, -score_val, ttfb_val, -rel_val, -proto_val)
    
    def process(self):
        self.ensure_output_dir()
        content = self.fetch_data()
        
        if not content:
            print("No data received - creating empty files")
            self.create_empty_files()
            return
        
        lines = content.splitlines()
        parsed_data = []
        
        print(f"Processing {len(lines)} lines...")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            data = self.parse_line(line)
            if data:
                parsed_data.append(data)
        
        if not parsed_data:
            print("No valid data found - creating empty files")
            self.create_empty_files()
            return
        
        parsed_data.sort(key=self.sort_key)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        ip_only = [item['ip'] for item in parsed_data if item.get('ip')]
        
        ip_port = [f"[IP: {item['ip']}] [PORT: {item['port']}]" for item in parsed_data if item.get('ip') and item.get('port')]
        
        ip_port_cdn_sni_country_type = []
        for item in parsed_data:
            parts = []
            if item.get('ip'):
                parts.append(f"[IP: {item['ip']}]")
            if item.get('port'):
                parts.append(f"[PORT: {item['port']}]")
            if item.get('tcp') and item['tcp'] != '-':
                parts.append(f"[TCP: {item['tcp']}]")
            if item.get('cdn') and item['cdn'] != '-':
                parts.append(f"[CDN: {item['cdn']}]")
            if item.get('sni') and item['sni'] != '-':
                parts.append(f"[SNI: {item['sni']}]")
            if item.get('country') and item['country'] != '-':
                parts.append(f"[Country: {item['country']}]")
            if item.get('type') and item['type'] != '-':
                parts.append(f"[TYPE: {item['type']}]")
            if item.get('score') and item['score'] != '-':
                parts.append(f"[SCORE: {item['score']}]")
            if item.get('ttfb') and item['ttfb'] != '-':
                parts.append(f"[TTFB: {item['ttfb']}]")
            if item.get('proto') and item['proto'] != '-':
                parts.append(f"[PROTO: {item['proto']}]")
            if item.get('reliability') and item['reliability'] != '-':
                parts.append(f"[REL: {item['reliability']}]")
            if item.get('city') and item['city'] != '-':
                parts.append(f"[City: {item['city']}]")
            if item.get('provider') and item['provider'] != '-':
                parts.append(f"[Provider: {item['provider']}]")
            if parts:
                ip_port_cdn_sni_country_type.append(" ".join(parts))
        
        with open(os.path.join(self.output_dir, 'ip_only.txt'), 'w', encoding='utf-8') as f:
            f.write(f"# IP Only - Updated: {timestamp}\n")
            f.write(f"# Count: {len(ip_only)}\n\n")
            f.write('\n'.join(ip_only))
        
        with open(os.path.join(self.output_dir, 'ip_port.txt'), 'w', encoding='utf-8') as f:
            f.write(f"# IP:PORT - Updated: {timestamp}\n")
            f.write(f"# Count: {len(ip_port)}\n\n")
            f.write('\n'.join(ip_port))
        
        with open(os.path.join(self.output_dir, 'ip_port_cdn_sni_country_type.txt'), 'w', encoding='utf-8') as f:
            f.write(f"# IP,PORT,CDN,SNI,COUNTRY,TYPE - Updated: {timestamp}\n")
            f.write(f"# Count: {len(ip_port_cdn_sni_country_type)}\n\n")
            f.write('\n'.join(ip_port_cdn_sni_country_type))
        
        print(f"✅ Processing complete!")
        print(f"Total IPs processed: {len(parsed_data)}")
        print(f"Files created in '{self.output_dir}/':")
        print(f"  - ip_only.txt: {len(ip_only)} entries")
        print(f"  - ip_port.txt: {len(ip_port)} entries")
        print(f"  - ip_port_cdn_sni_country_type.txt: {len(ip_port_cdn_sni_country_type)} entries")
    
    def create_empty_files(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        files = ['ip_only.txt', 'ip_port.txt', 'ip_port_cdn_sni_country_type.txt']
        for filename in files:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# No data available - Updated: {timestamp}\n")
                f.write("# Please check the source URL or try again later.\n")
                f.write("# Count: 0\n")
        
        print(f"⚠️ Empty files created in '{self.output_dir}/'")

def main():
    try:
        processor = BestIPProcessor()
        processor.process()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
