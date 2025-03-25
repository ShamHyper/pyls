import os
import sys
import colorama
from colorama import Fore, Style

colorama.init()

def get_file_size(size):
    """Преобразование размера файла в читаемый вид (KB, MB, GB)"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

def get_dir_size(path):
    """Рекурсивный подсчет размера директории"""
    total_size = 0
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                total_size += os.stat(full_path).st_size
            elif os.path.isdir(full_path):
                total_size += get_dir_size(full_path)
    except PermissionError:
        pass
    except Exception as e:
        print(f"{Fore.RED}Ошибка при подсчете размера: {str(e)}{Style.RESET_ALL}")
    return total_size

def list_dir(path="."):
    """Основная функция для вывода списка файлов и папок"""
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
            item_type = "DIR" if is_dir else "FILE"
            
            size = get_dir_size(full_path) if is_dir else stats.st_size
            all_size += size
            
            print(f"{get_file_size(size):>8}  {color}{item:<{max_name_length}}{Style.RESET_ALL}  [{item_type}]")
        return all_size
    except PermissionError:
        print(f"{Fore.RED}Ошибка: Нет доступа к директории{Style.RESET_ALL}")
        return 0
    except Exception as e:
        print(f"{Fore.RED}Ошибка: {str(e)}{Style.RESET_ALL}")
        return 0

def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "."
    
    all_size = list_dir(path)
    
    total_files = len([x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
    total_dirs = len([x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))])
    print(f"\n{Fore.CYAN}Всего: {total_dirs} папок, {total_files} файлов{Style.RESET_ALL}. Общий вес директории: {get_file_size(all_size)}")

if __name__ == "__main__":
    main()