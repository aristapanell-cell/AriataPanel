import os
import hashlib
from datetime import datetime

class ConfigCombiner:
    def __init__(self):
        self.categories = [
            'vmess', 'vless', 'trojan', 'ss',
            'hysteria2', 'hysteria', 'tuic',
            'wireguard', 'other'
        ]
        
        self.tiers = [50, 100, 150, 200, 250, 300, 400, 500, "ALL"]
        self.tier_cache = {}
    
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
            config_hash = hashlib.md5(config.encode()).hexdigest()
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
            h = hashlib.md5(c.encode()).hexdigest()
            if h not in seen:
                seen.add(h)
                result.append(c)
        
        tier_cache[cache_key] = result
        return result
    
    def generate_tiered_outputs(self, configs_list, source_name, base_path, timestamp):
        for category in self.categories:
            category_configs = []
            category_key = f"{source_name}_{category}"
            
            if source_name == "combined":
                category_configs = configs_list.get(category, [])
            elif source_name == "telegram":
                category_configs = self.read_configs(f'configs/telegram/{category}.txt')
            elif source_name == "github":
                category_configs = self.read_configs(f'configs/github/{category}.txt')
            
            if not category_configs:
                continue
            
            unique_configs = self.deduplicate(category_configs)
            cat_dir = os.path.join(base_path, category)
            os.makedirs(cat_dir, exist_ok=True)
            
            tier_cache = {}
            
            for i, tier in enumerate(self.tiers):
                selected = self.build_tier_with_overlap(unique_configs, i, tier, tier_cache)
                
                if not selected:
                    continue
                
                filename = os.path.join(cat_dir, f"{tier}.txt")
                title = f"{source_name.upper()} - Tier {tier} - {category.upper()}"
                self.write_config_file(filename, title, selected, len(selected), timestamp)
        
        all_configs = []
        if source_name == "combined":
            for category in self.categories:
                all_configs.extend(configs_list.get(category, []))
        elif source_name == "telegram":
            all_configs = self.read_configs('configs/telegram/all.txt')
        elif source_name == "github":
            all_configs = self.read_configs('configs/github/all.txt')
        
        if all_configs:
            unique_all = self.deduplicate(all_configs)
            all_dir = os.path.join(base_path, "ALL")
            os.makedirs(all_dir, exist_ok=True)
            
            tier_cache_all = {}
            
            for i, tier in enumerate(self.tiers):
                selected = self.build_tier_with_overlap(unique_all, i, tier, tier_cache_all)
                
                if not selected:
                    continue
                
                filename = os.path.join(all_dir, f"{tier}.txt")
                title = f"{source_name.upper()} - Tier {tier} - ALL"
                self.write_config_file(filename, title, selected, len(selected), timestamp)
    
    def combine(self):
        os.makedirs('configs/combined', exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        all_combined_dict = {}
        all_combined_list = []
        
        for category in self.categories:
            telegram_configs = self.read_configs(f'configs/telegram/{category}.txt')
            github_configs = self.read_configs(f'configs/github/{category}.txt')
            
            combined_configs = telegram_configs + github_configs
            unique_configs = self.deduplicate(combined_configs)
            
            if unique_configs:
                filename = f"configs/combined/{category}.txt"
                title = f"Combined {category.upper()} Configurations"
                self.write_config_file(filename, title, unique_configs, len(unique_configs), timestamp, len(telegram_configs), len(github_configs))
                all_combined_dict[category] = unique_configs
                all_combined_list.extend(unique_configs)
        
        if all_combined_list:
            all_unique = self.deduplicate(all_combined_list)
            filename = "configs/combined/all.txt"
            title = "All Combined Configurations"
            self.write_config_file(filename, title, all_unique, len(all_unique), timestamp)
        
        all_telegram = self.read_configs('configs/telegram/all.txt')
        all_github = self.read_configs('configs/github/all.txt')
        
        total_telegram = len(all_telegram)
        total_github = len(all_github)
        total_combined = len(self.deduplicate(all_combined_list))
        
        print("=" * 60)
        print("CONFIG COMBINER")
        print("=" * 60)
        print(f"Telegram configs: {total_telegram}")
        print(f"GitHub configs: {total_github}")
        print(f"Combined unique configs: {total_combined}")
        print("\n📁 Files created in configs/combined/:")
        
        for category in self.categories:
            if os.path.exists(f'configs/combined/{category}.txt'):
                with open(f'configs/combined/{category}.txt', 'r', encoding='utf-8') as f:
                    lines = [line for line in f if line.strip() and not line.startswith('#')]
                print(f"  {category}.txt: {len(lines)} configs")
        
        if os.path.exists('configs/combined/all.txt'):
            with open('configs/combined/all.txt', 'r', encoding='utf-8') as f:
                lines = [line for line in f if line.strip() and not line.startswith('#')]
            print(f"  all.txt: {len(lines)} configs")
        
        print("=" * 60)
        
        self.generate_tiered_outputs(all_combined_dict, "combined", "configs/combined", timestamp)
        self.generate_tiered_outputs({}, "telegram", "configs/telegram", timestamp)
        self.generate_tiered_outputs({}, "github", "configs/github", timestamp)
        
        print("\n" + "=" * 60)
        print("TIERED STRUCTURE GENERATED")
        print("=" * 60)
        
        for source in ["combined", "telegram", "github"]:
            print(f"\n📁 {source.upper()}/:")
            base_dir = f"configs/{source}"
            
            for category in self.categories:
                cat_dir = os.path.join(base_dir, category)
                if os.path.exists(cat_dir):
                    print(f"  📁 {category}/:")
                    for tier in self.tiers:
                        tier_file = os.path.join(cat_dir, f"{tier}.txt")
                        if os.path.exists(tier_file):
                            with open(tier_file, 'r', encoding='utf-8') as f:
                                lines = [line for line in f if line.strip() and not line.startswith('#')]
                            print(f"      {tier}.txt: {len(lines)} configs")
            
            all_dir = os.path.join(base_dir, "ALL")
            if os.path.exists(all_dir):
                print(f"  📁 ALL/:")
                for tier in self.tiers:
                    tier_file = os.path.join(all_dir, f"{tier}.txt")
                    if os.path.exists(tier_file):
                        with open(tier_file, 'r', encoding='utf-8') as f:
                            lines = [line for line in f if line.strip() and not line.startswith('#')]
                        print(f"      {tier}.txt: {len(lines)} configs")
        
        print("\n" + "=" * 60)
        return all_combined_list

def main():
    combiner = ConfigCombiner()
    combiner.combine()

if __name__ == "__main__":
    main()
