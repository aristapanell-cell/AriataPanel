import os
import hashlib
import json
import base64
from datetime import datetime
from urllib.parse import urlparse, parse_qs, unquote

class ConfigCombiner:
    def __init__(self):
        self.categories = [
            'vmess', 'vless', 'trojan', 'ss',
            'hysteria2', 'hysteria', 'tuic',
            'wireguard', 'other'
        ]
        
        self.tiers = [50, 100, 150, 200, 250, 300, 400, 500, "ALL"]
        self.tier_cache = {}
    
    def decode_vmess(self, config_str):
        try:
            base64_part = config_str[8:]
            if len(base64_part) % 4 != 0:
                base64_part += '=' * (4 - len(base64_part) % 4)
            return json.loads(base64.b64decode(base64_part).decode('utf-8'))
        except:
            return None
    
    def normalize_config(self, config):
        if isinstance(config, dict):
            return config
        if config.startswith("vmess://"):
            vm = self.decode_vmess(config)
            if vm:
                vm.pop("ps", None)
                return vm
            return None
        try:
            p = urlparse(config)
            result = {
                "scheme": p.scheme,
                "server": p.hostname or "",
                "port": p.port or 0,
                "user": unquote(p.username or ""),
                "path": unquote(p.path or "")
            }
            query = parse_qs(p.query)
            for k in sorted(query):
                result[k] = query[k][0]
            return result
        except:
            return None
    
    def build_unique_key(self, obj):
        if not obj:
            return ""
        proto = obj.get("scheme") or "vmess"
        if proto == "vmess":
            fields = [
                obj.get("add",""),
                str(obj.get("port","")),
                obj.get("id",""),
                obj.get("net",""),
                obj.get("host",""),
                obj.get("path",""),
                obj.get("tls",""),
                obj.get("sni","")
            ]
        elif proto == "vless":
            fields = [
                obj.get("server",""),
                str(obj.get("port","")),
                obj.get("user",""),
                obj.get("security",""),
                obj.get("type",""),
                obj.get("host",""),
                obj.get("path",""),
                obj.get("sni",""),
                obj.get("flow","")
            ]
        elif proto == "trojan":
            fields = [
                obj.get("server",""),
                str(obj.get("port","")),
                obj.get("user",""),
                obj.get("security",""),
                obj.get("type",""),
                obj.get("host",""),
                obj.get("path",""),
                obj.get("sni","")
            ]
        elif proto == "ss":
            fields = [
                obj.get("server",""),
                str(obj.get("port","")),
                obj.get("user",""),
                obj.get("method","")
            ]
        elif proto in ("hysteria2","hy2"):
            fields = [
                obj.get("server",""),
                str(obj.get("port","")),
                obj.get("user",""),
                obj.get("obfs-password",""),
                obj.get("sni","")
            ]
        elif proto == "tuic":
            fields = [
                obj.get("server",""),
                str(obj.get("port","")),
                obj.get("user",""),
                obj.get("congestion_control",""),
                obj.get("sni","")
            ]
        elif proto == "wireguard":
            fields = [
                obj.get("server",""),
                str(obj.get("port","")),
                obj.get("user",""),
                obj.get("key",""),
                obj.get("address","")
            ]
        else:
            fields = sorted(obj.items())
        return json.dumps(fields, sort_keys=True, ensure_ascii=False)
    
    def read_configs(self, filepath):
        if not os.path.exists(filepath):
            return []
        
        configs = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    configs.append(line)
        
        return configs
    
    def deduplicate(self, configs):
        unique_configs = []
        seen_hashes = set()
        
        for config in configs:
            obj = self.normalize_config(config)
            if obj is None:
                config_hash = hashlib.md5(config.encode()).hexdigest()
            else:
                key = self.build_unique_key(obj)
                config_hash = hashlib.md5(key.encode()).hexdigest()
            
            if config_hash not in seen_hashes:
                seen_hashes.add(config_hash)
                unique_configs.append(config)
        
        return unique_configs
    
    def write_config_file(self, filepath, title, configs, count, timestamp, telegram_count=0, github_count=0):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        content = f"# {title}\n"
        content += f"# Updated: {timestamp}\n"
        content += f"# Count: {count}\n"
        if telegram_count > 0 or github_count > 0:
            content += f"# Sources: Telegram ({telegram_count}) + GitHub ({github_count})\n"
        content += "\n"
        content += "\n".join(configs)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def build_tier_with_overlap(self, unique_configs, tier_index, tier_value, tier_cache):
        if tier_value == "ALL":
            return unique_configs
        
        cache_key = f"{len(unique_configs)}_{tier_value}"
        if cache_key in tier_cache:
            return tier_cache[cache_key]
        
        base_size = tier_value
        
        if tier_index == 0:
            result = unique_configs[:base_size]
            tier_cache[cache_key] = result
            return result
        
        overlap_size = tier_index * 10
        
        prev_tier_value = self.tiers[tier_index - 1]
        prev_cache_key = f"{len(unique_configs)}_{prev_tier_value}"
        
        if prev_cache_key in tier_cache:
            previous_selected = tier_cache[prev_cache_key]
        else:
            if prev_tier_value == "ALL":
                previous_selected = unique_configs
            else:
                previous_selected = unique_configs[:prev_tier_value]
        
        base_part = unique_configs[:base_size]
        
        if overlap_size <= len(previous_selected):
            overlap_part = previous_selected[-overlap_size:]
        else:
            overlap_part = previous_selected[:]
        
        merged = base_part + overlap_part
        
        result = []
        seen = set()
        
        for c in merged:
            obj = self.normalize_config(c)
            if obj is None:
                h = hashlib.md5(c.encode()).hexdigest()
            else:
                key = self.build_unique_key(obj)
                h = hashlib.md5(key.encode()).hexdigest()
            
            if h not in seen:
                seen.add(h)
                result.append(c)
        
        tier_cache[cache_key] = result
        return result
    
    def build_balanced_tier(self, category_configs_dict, tier_size, source_name, base_path, timestamp):
        available_configs = {}
        for category in self.categories:
            if category in category_configs_dict and category_configs_dict[category]:
                available_configs[category] = category_configs_dict[category][:]
        
        if not available_configs:
            return []
        
        num_categories = len([c for c in self.categories if c in available_configs and available_configs[c]])
        if num_categories == 0:
            return []
        
        base_per_category = tier_size // num_categories
        remainder = tier_size % num_categories
        
        selected_configs = []
        
        category_order = ['trojan', 'hysteria2', 'ss', 'vmess']
        other_categories = [c for c in self.categories if c not in category_order and c in available_configs]
        ordered_categories = [c for c in category_order if c in available_configs] + other_categories
        
        per_category_allocation = {}
        
        for cat in ordered_categories:
            per_category_allocation[cat] = base_per_category
        
        for i in range(remainder):
            if i < len(ordered_categories):
                per_category_allocation[ordered_categories[i]] += 1
        
        total_shortage = 0
        for cat, needed in per_category_allocation.items():
            available = len(available_configs[cat])
            if needed > available:
                total_shortage += (needed - available)
                per_category_allocation[cat] = available
        
        if total_shortage > 0:
            categories_with_extra = [cat for cat in ordered_categories if per_category_allocation[cat] < len(available_configs[cat])]
            if categories_with_extra:
                extra_per_category = total_shortage // len(categories_with_extra)
                extra_remainder = total_shortage % len(categories_with_extra)
                for idx, cat in enumerate(categories_with_extra):
                    per_category_allocation[cat] += extra_per_category
                    if idx < extra_remainder:
                        per_category_allocation[cat] += 1
        
        for cat in ordered_categories:
            if cat not in available_configs:
                continue
            take_count = min(per_category_allocation.get(cat, 0), len(available_configs[cat]))
            if take_count > 0:
                selected_configs.extend(available_configs[cat][:take_count])
        
        if len(selected_configs) > tier_size:
            selected_configs = selected_configs[:tier_size]
        elif len(selected_configs) < tier_size:
            for cat in ordered_categories:
                if len(selected_configs) >= tier_size:
                    break
                if cat in available_configs:
                    remaining_in_cat = available_configs[cat][per_category_allocation.get(cat, 0):]
                    needed = tier_size - len(selected_configs)
                    take_extra = min(needed, len(remaining_in_cat))
                    if take_extra > 0:
                        selected_configs.extend(remaining_in_cat[:take_extra])
        
        return self.deduplicate(selected_configs)
    
    def generate_tiered_outputs(self, configs_list, source_name, base_path, timestamp):
        for category in self.categories:
            category_configs = []
            category_key = f"{source_name}_{category}"
            
            if source_name == "combined":
                category_configs = configs_list.get(category, [])
            elif source_name == "telegram":
                category_configs = self.read_configs(f'configs.txt/telegram/{category}.txt')
            elif source_name == "github":
                category_configs = self.read_configs(f'configs.txt/github/{category}.txt')
            
            if not category_configs:
                continue
            
            unique_configs = self.deduplicate(category_configs)
            total_count = len(unique_configs)
            cat_dir = os.path.join(base_path, category)
            os.makedirs(cat_dir, exist_ok=True)
            
            tier_cache = {}
            
            for i, tier in enumerate(self.tiers):
                if tier != "ALL" and tier > total_count:
                    continue
                
                selected = self.build_tier_with_overlap(unique_configs, i, tier, tier_cache)
                
                if not selected:
                    continue
                
                filename = os.path.join(cat_dir, f"{tier}.txt")
                title = f"{source_name.upper()} - Tier {tier} - {category.upper()}"
                self.write_config_file(filename, title, selected, len(selected), timestamp)
            
            all_filename = os.path.join(cat_dir, "ALL.txt")
            title = f"{source_name.upper()} - ALL - {category.upper()}"
            self.write_config_file(all_filename, title, unique_configs, total_count, timestamp)
        
        all_configs = {}
        if source_name == "combined":
            for category in self.categories:
                if category in configs_list and configs_list[category]:
                    all_configs[category] = configs_list[category][:]
        elif source_name == "telegram":
            for category in self.categories:
                cat_configs = self.read_configs(f'configs.txt/telegram/{category}.txt')
                if cat_configs:
                    all_configs[category] = cat_configs
        elif source_name == "github":
            for category in self.categories:
                cat_configs = self.read_configs(f'configs.txt/github/{category}.txt')
                if cat_configs:
                    all_configs[category] = cat_configs
        
        if all_configs:
            all_dir = os.path.join(base_path, "ALL")
            os.makedirs(all_dir, exist_ok=True)
            
            for tier in self.tiers:
                if tier == "ALL":
                    continue
                
                balanced_configs = self.build_balanced_tier(all_configs, tier, source_name, base_path, timestamp)
                
                if not balanced_configs:
                    continue
                
                filename = os.path.join(all_dir, f"{tier}.txt")
                title = f"{source_name.upper()} - Balanced Tier {tier} - ALL"
                self.write_config_file(filename, title, balanced_configs, len(balanced_configs), timestamp)
            
            all_flat_configs = []
            for cat_configs in all_configs.values():
                all_flat_configs.extend(cat_configs)
            unique_all = self.deduplicate(all_flat_configs)
            total_all_count = len(unique_all)
            
            all_filename = os.path.join(all_dir, "ALL.txt")
            title = f"{source_name.upper()} - ALL - ALL"
            self.write_config_file(all_filename, title, unique_all, total_all_count, timestamp)
    
    def combine(self):
        os.makedirs('configs.txt/combined', exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        all_combined_dict = {}
        all_combined_list = []
        
        for category in self.categories:
            telegram_configs = self.read_configs(f'configs.txt/telegram/{category}.txt')
            github_configs = self.read_configs(f'configs.txt/github/{category}.txt')
            
            combined_configs = telegram_configs + github_configs
            unique_configs = self.deduplicate(combined_configs)
            
            if unique_configs:
                filename = f"configs.txt/combined/{category}.txt"
                title = f"Combined {category.upper()} Configurations"
                self.write_config_file(filename, title, unique_configs, len(unique_configs), timestamp, len(telegram_configs), len(github_configs))
                all_combined_dict[category] = unique_configs
                all_combined_list.extend(unique_configs)
        
        if all_combined_list:
            all_unique = self.deduplicate(all_combined_list)
            filename = "configs.txt/combined/all.txt"
            title = "All Combined Configurations"
            self.write_config_file(filename, title, all_unique, len(all_unique), timestamp)
        
        all_telegram = self.read_configs('configs.txt/telegram/all.txt')
        all_github = self.read_configs('configs.txt/github/all.txt')
        
        total_telegram = len(all_telegram)
        total_github = len(all_github)
        total_combined = len(self.deduplicate(all_combined_list))
        
        print("=" * 60)
        print("CONFIG COMBINER")
        print("=" * 60)
        print(f"Telegram configs: {total_telegram}")
        print(f"GitHub configs: {total_github}")
        print(f"Combined unique configs: {total_combined}")
        print("\n📁 Files created in configs.txt/combined/:")
        
        for category in self.categories:
            filepath = f'configs.txt/combined/{category}.txt'
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = [line for line in f if line.strip() and not line.startswith('#')]
                print(f"  {category}.txt: {len(lines)} configs")
        
        all_filepath = 'configs.txt/combined/all.txt'
        if os.path.exists(all_filepath):
            with open(all_filepath, 'r', encoding='utf-8') as f:
                lines = [line for line in f if line.strip() and not line.startswith('#')]
            print(f"  all.txt: {len(lines)} configs")
        
        print("=" * 60)
        
        self.generate_tiered_outputs(all_combined_dict, "combined", "configs.txt/combined", timestamp)
        self.generate_tiered_outputs({}, "telegram", "configs.txt/telegram", timestamp)
        self.generate_tiered_outputs({}, "github", "configs.txt/github", timestamp)
        
        for source in ["combined", "telegram", "github"]:
            base_dir = f"configs.txt/{source}"
            for category in self.categories:
                category_root = os.path.join(base_dir, f"{category}.txt")
                if os.path.exists(category_root) and os.path.isfile(category_root):
                    os.remove(category_root)
            all_root = os.path.join(base_dir, "all.txt")
            if os.path.exists(all_root) and os.path.isfile(all_root):
                os.remove(all_root)
        
        print("\n" + "=" * 60)
        print("TIERED STRUCTURE GENERATED")
        print("=" * 60)
        
        for source in ["combined", "telegram", "github"]:
            print(f"\n📁 {source.upper()}/:")
            base_dir = f"configs.txt/{source}"
            
            for category in self.categories:
                cat_dir = os.path.join(base_dir, category)
                if os.path.exists(cat_dir) and os.path.isdir(cat_dir):
                    print(f"  📁 {category}/:")
                    for tier in self.tiers:
                        tier_file = os.path.join(cat_dir, f"{tier}.txt")
                        if os.path.exists(tier_file):
                            with open(tier_file, 'r', encoding='utf-8') as f:
                                lines = [line for line in f if line.strip() and not line.startswith('#')]
                            print(f"      {tier}.txt: {len(lines)} configs")
                    all_file = os.path.join(cat_dir, "ALL.txt")
                    if os.path.exists(all_file):
                        with open(all_file, 'r', encoding='utf-8') as f:
                            lines = [line for line in f if line.strip() and not line.startswith('#')]
                        print(f"      ALL.txt: {len(lines)} configs")
            
            all_dir = os.path.join(base_dir, "ALL")
            if os.path.exists(all_dir) and os.path.isdir(all_dir):
                print(f"  📁 ALL/:")
                for tier in self.tiers:
                    if tier == "ALL":
                        continue
                    tier_file = os.path.join(all_dir, f"{tier}.txt")
                    if os.path.exists(tier_file):
                        with open(tier_file, 'r', encoding='utf-8') as f:
                            lines = [line for line in f if line.strip() and not line.startswith('#')]
                        print(f"      {tier}.txt: {len(lines)} configs")
                all_file = os.path.join(all_dir, "ALL.txt")
                if os.path.exists(all_file):
                    with open(all_file, 'r', encoding='utf-8') as f:
                        lines = [line for line in f if line.strip() and not line.startswith('#')]
                    print(f"      ALL.txt: {len(lines)} configs")
        
        print("\n" + "=" * 60)
        return all_combined_list

def main():
    combiner = ConfigCombiner()
    combiner.combine()

if __name__ == "__main__":
    main()
