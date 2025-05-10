import os
import requests
import yaml
import re
requests.packages.urllib3.disable_warnings()

def get_config():
    # 获取项目根目录的配置文件
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(project_root, "app", "config.yaml")
    
    if not os.path.exists(config_file):
        config_file = os.path.join(project_root, "app", "config.yaml.example")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # 检查MongoDB配置
    if not config.get('MONGO', {}).get('URI'):
        print("[-] MongoDB URI not found in config file")
        sys.exit(1)
        
    return config

def update_data(token):
    # 获取配置
    config = get_config()
    mongo_uri = config['MONGO']['URI']  # 获取MongoDB URI
    # 获取API地址
    api_host = config.get('API', {}).get('HOST', '127.0.0.1')
    api_port = config.get('API', {}).get('PORT', 5003)
    api_ssl = config.get('API', {}).get('SSL', True)
    
    # 构建API URL
    protocol = 'https' if api_ssl else 'http'
    api_base_url = f"{protocol}://{api_host}:{api_port}"

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建指纹数据文件的相对路径 
    finger_file = os.path.join(current_dir, "指纹数据.json")
    
    push_config = yaml.safe_load(open(finger_file, "r", encoding="utf-8").read())
    for i in push_config:
        name = i['name']
        rule = i['rule']
        payload = {
            "name": name,
            "human_rule": rule
        }
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Token": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36"
        }
        response = requests.post(f"{api_base_url}/api/fingerprint/", json=payload, headers=headers,timeout=20, verify=False)
        if response.status_code==200:
            print(f"[+] 指纹:'{name}'\t规则:{rule}")
        else:
            print(f"[-] 指纹:'{name}'\t上传失败")

def do_login():
    # 获取配置
    config = get_config()
    api_host = config.get('API', {}).get('HOST', '127.0.0.1')
    api_port = config.get('API', {}).get('PORT', 5003)
    api_ssl = config.get('API', {}).get('SSL', True)
    
    # 获取默认用户名密码
    default_username = config.get('CASM', {}).get('USERNAME', 'admin')
    default_password = config.get('CASM', {}).get('PASSWORD', 'casm@pass')
    
    protocol = 'https' if api_ssl else 'http'
    login_url = f"{protocol}://{api_host}:{api_port}/api/user/login"

    burp0_headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36"
    }
    burp0_json = {
        "password": default_password,
        "username": default_username
    }

    try:
        res = requests.post(login_url, headers=burp0_headers, json=burp0_json, timeout=20, verify=False)
        if res.status_code == 200 and res.json()['code'] == 200:
            print("[+] Login Success!")
            token = res.json()['data']['token']
            update_data(token)
        else:
            print(f"[-] Login Failed! Status:{res.status_code}, Response:{res.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"[-] Connection Error: {str(e)}")
        print("[*] Please check if the API server is running and accessible")
    except Exception as e:
        print(f"[-] Error: {str(e)}")

if __name__ == '__main__':
    do_login()
