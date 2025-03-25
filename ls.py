import os
import sys
import colorama
from colorama import Fore, Style
import locale
from translations import get_translation

colorama.init()

def get_file_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

def get_dir_size(path, lang="en"):
    total_size = 0
    
    try:
        items = os.listdir(path)
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                total_size += os.stat(full_path).st_size
            elif os.path.isdir(full_path):
                total_size += get_dir_size(full_path, lang)
    except PermissionError:
        return 0
    except Exception as e:
        print(f"{Fore.RED}{get_translation('size_error', lang, error=str(e))}{Style.RESET_ALL}")
        return 0
    
    return total_size

def list_dir(path=".", show_size=False, lang="en"):
    if not show_size:
        try:
            items = os.listdir(path)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            max_name_length = max(len(item) for item in items) if items else 0
            
            for item in items:
                full_path = os.path.join(path, item)
                is_dir = os.path.isdir(full_path)
                color = Fore.MAGENTA if is_dir else Fore.GREEN
                item_type = get_translation("DIR" if is_dir else "FILE", lang)
                print(f"{color}{item:<{max_name_length}}{Style.RESET_ALL}  [{item_type}]")
            
            return 0
        
        except PermissionError:
            print(f"{Fore.RED}{get_translation('dir_error', lang)}{Style.RESET_ALL}")
            return 0
        except Exception as e:
            print(f"{Fore.RED}{get_translation('generic_error', lang, error=str(e))}{Style.RESET_ALL}")
            return 0
    
    try:
        items = os.listdir(path)
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        max_name_length = max(len(item) for item in items) if items else 0
        all_size = 0
        
        for item in items:
            full_path = os.path.join(path, item)
            stats = os.stat(full_path)
            is_dir = os.path.isdir(full_path)
            color = Fore.MAGENTA if is_dir else Fore.GREEN
            item_type = get_translation("DIR" if is_dir else "FILE", lang)
            size = get_dir_size(full_path, lang) if is_dir else stats.st_size
            all_size += size
            
            print(f"{get_file_size(size):>8}  {color}{item:<{max_name_length}}{Style.RESET_ALL}  [{item_type}]")
        
        return all_size
    
    except PermissionError:
        print(f"{Fore.RED}{get_translation('dir_error', lang)}{Style.RESET_ALL}")
        return 0
    except Exception as e:
        print(f"{Fore.RED}{get_translation('generic_error', lang, error=str(e))}{Style.RESET_ALL}")
        return 0

def main():
    system_lang = locale.getlocale()[0][:2].lower() if locale.getlocale()[0] else "en"
    if system_lang not in ["ru", "en"]:
        system_lang = "en"
    
    show_size = "-s" in sys.argv
    path = "."
    
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg != "-s" and not arg.startswith("-"):
                path = arg
                break
    
    all_size = list_dir(path, show_size, system_lang)
    
    total_files = len([x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    total_dirs = len([x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))])
    
    if show_size:
        print(f"\n{Fore.CYAN}{get_translation('total_with_size', system_lang, dirs=total_dirs, files=total_files, size=get_file_size(all_size))}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.CYAN}{get_translation('total', system_lang, dirs=total_dirs, files=total_files)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()