import os
import yaml
import sys

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CELERY_BROKER_URL = "amqp://casm:casm%40RabbitMQ@127.0.0.1:5672/casm"

    MONGO_DB = 'casm'
    MONGO_URL = 'mongodb://127.0.0.1:27017/'

    TMP_PATH = os.path.join(basedir, 'tmp')
    if not os.path.exists(TMP_PATH):
        os.mkdir(TMP_PATH)
    MASSDNS_BIN = os.path.join(basedir, 'tools/massdns')
    SCREENSHOT_JS = os.path.join(basedir, 'tools/screenshot.js')
    SCREENSHOT_DIR = os.path.join(basedir, 'tmp_screenshot')
    SCREENSHOT_FAIL_IMG = os.path.join(basedir, 'dicts/noscreenshot.jpg')
    DRIVER_JS = os.path.join(basedir, 'tools/driver.js')

    DOMAIN_DICT_TEST = os.path.join(basedir, 'dicts/domain_dict_test.txt')
    DOMAIN_DICT_2W = os.path.join(basedir, 'dicts/domain_2w.txt')
    DNS_SERVER = os.path.join(basedir, 'dicts/dnsserver.txt')

    CDN_JSON_PATH = os.path.join(basedir, 'dicts/cdn_info.json')

    # WebInfoHunter 规则文件
    WIH_RULE_PATH = os.path.join(basedir, "dicts/wih_rules.yml")

    black_domain_path = os.path.join(basedir, 'dicts/blackdomain.txt')
    black_hexie_path = os.path.join(basedir, 'dicts/blackhexie.txt')
    black_asset_site = os.path.join(basedir, 'dicts/black_asset_site.txt')
    altdns_dict_path = os.path.join(basedir, 'dicts/altdnsdict.txt')

    web_app_rule = os.path.join(basedir, 'dicts/webapp.json')
    dns_query_plugin_path = os.path.join(basedir, 'services/dns_query_plugin')

    TOP_1000 = "1,3-4,6-7,9,13,17,19-26,30,32-33,37,42-43,49,53,68-70,79-85,88-90,99-100,106,109-111,113,119,125,135,139,143-144,146,161,163,179,199,211-212,222,254-256,259,264,280,301,306,311,340,366,389,406-407,416-417,425,427,443-445,458,464-465,481,497,500,512-515,524,541,543-546,548,554-555,563,587,593,616-617,623,625,631,636,646,648,666-668,683,687,691,700,705,711,714,720,722,726,749,765,777,783,787,800-801,808,843,873,880,888,898,900-903,911-912,981,987,990,992-993,995,999-1002,1007,1009-1011,1021-1100,1102,1104-1108,1110-1114,1117,1119,1121-1124,1126,1130-1132,1137-1138,1141,1145,1147-1149,1151-1152,1154,1163-1166,1169,1174-1175,1183,1185-1187,1192,1194,1198-1199,1201,1213,1216-1218,1233-1234,1236,1244,1247-1248,1259,1271-1272,1277,1287,1296,1300-1301,1309-1311,1322,1328,1334,1337,1352,1417,1433-1434,1443,1455,1461,1494,1500-1501,1503,1521,1524,1533,1556,1580,1583,1594,1600,1641,1658,1666-1667,1687-1688,1700,1717-1721,1723,1755,1761,1782-1783,1801,1805,1812,1839-1840,1862-1864,1875,1900,1914,1935,1947,1971-1972,1974,1984,1998-2010,2013,2020-2022,2030,2033-2035,2038,2040-2043,2045-2049,2065,2068,2099-2100,2103,2105-2107,2111,2119,2121,2126,2135,2144,2160-2161,2170,2179,2181,2190-2191,2196,2200,2222,2233,2251,2260,2288,2301,2323,2366,2375,2379,2381-2383,2393-2394,2399,2401,2443,2492,2500,2522,2525,2557,2601-2602,2604-2605,2607-2608,2638,2701-2702,2710,2717-2718,2725,2800,2809,2811,2869,2875,2888,2909-2910,2920,2967-2968,2998,3000-3001,3003,3005-3007,3011,3013,3017,3030-3031,3052,3071,3077,3128,3168,3211,3221,3260-3261,3268-3269,3283,3300-3301,3306,3322-3325,3333,3351,3367,3369-3372,3389-3390,3404,3476,3493,3517,3520,3527,3546,3551,3580,3659,3689-3690,3703,3737,3766,3772-3773,3784,3800-3801,3809,3814,3826-3828,3851,3869,3871,3878,3880,3888-3889,3905,3914,3918,3920,3945,3971,3986,3995,3998,4000-4006,4045,4111,4125-4126,4129,4224,4242,4279,4321,4343,4369,4443-4446,4449,4550,4560,4567,4662,4848,4899-4900,4998,5000-5004,5006,5009,5030,5033,5050-5051,5054,5060-5061,5080,5087,5100-5102,5111,5120,5151,5190,5200,5214,5221-5222,5225-5226,5269,5280,5298,5355,5357,5387,5405,5414,5431-5432,5440,5500,5510,5544,5550,5555,5560,5566,5601,5631-5633,5666,5672,5678-5679,5718,5722,5730,5800-5802,5810-5811,5815,5822,5825,5850,5859,5862,5877,5900-5904,5906-5907,5910-5911,5915,5922,5925,5950,5952,5959-5963,5987-5989,5998-6007,6009,6025,6059,6080,6093,6100-6101,6106,6112,6123,6129,6156,6161,6182,6346,6379,6389,6443,6502,6510,6543,6547,6565-6567,6580,6646,6666-6669,6689,6692,6699,6779,6788-6789,6792,6839,6881,6901,6969,7000-7008,7019,7025,7070,7100,7103,7106,7180,7182,7200-7201,7337,7402,7435,7443,7474,7496,7512,7625,7627,7676,7680,7687,7741,7777-7778,7800,7911,7920-7921,7937-7938,7999-8002,8007-8011,8016,8020-8022,8025,8030-8033,8040-8042,8045,8050,8060,8069-8070,8080-8091,8093,8099-8100,8123-8124,8161,8180-8181,8188,8192-8194,8200,8222,8254,8290-8292,8300,8333,8383,8400,8402,8443,8480-8481,8500,8600,8649,8651-8652,8654,8701,8744,8800,8873,8888-8889,8898-8899,8983,8989,8994,9000-9003,9009-9011,9040,9043,9050,9071,9080-9083,9090-9092,9094-9095,9099-9103,9110-9111,9200,9207,9220,9222,9290,9293,9300,9389,9391-9392,9415,9418,9443,9485,9500,9502-9503,9535,9575,9593-9595,9618,9666,9876-9878,9898,9900,9917,9929,9943-9944,9968,9987-9988,9994-10004,10009-10010,10012,10020,10024-10025,10030,10033,10050-10051,10080-10082,10101,10180,10215,10243,10250-10252,10255-10256,10566,10616-10617,10621,10626,10628-10629,10666,10778,11000-11001,11080,11110-11111,11211,11443,11967,12000,12174,12234,12265,12306,12345,12669,12750,12801-12804,12999,13456,13562,13722,13782-13783,14000,14238,14441-14442,15000,15002-15004,15660,15672,15742,16000-16001,16010,16012,16016,16018,16020,16030,16080,16113,16666,16992-16993,17877,17988,18040,18080,18089,18101,18988,19101,19283,19315,19350,19780,19801,19842,19888,19890,20000,20005-20006,20031,20221-20222,20828,20880,21000,21443,21571,22939,23502,24444,24800,25672,25734-25735,26214,27000,27017-27018,27352-27353,27355-27356,27715,28201,30000,30718,30951,31038,31337,32768-32785,33354,33899,34451,34528,34571-34573,35500,36359,37257,37310,38243,38292,38914,39297,40193,40654,40911,41084,41414,41511,42424,42510,43761,44176,44442-44443,44501,44838,45100,46675,48080,49152-49161,49163,49165-49167,49175-49176,49400,49664-49667,49670,49692,49697,49999-50003,50006,50010,50020,50070,50075,50090-50091,50095,50100,50105,50300,50389,50470,50475,50500,50636,50800,51103,51493,52673,52822,52848,52869,54045,54321,54328,54345,54485,54488,55055-55056,55555,55600,56341,56737-56738,57294,57797,58080,58316,60000,60010,60020,60030,60443,61532,61616,61900,62078,63331,64623,64680,65000,65129,65389,65512,6677,8484,8360,7080,41516,8880,8881,3505,1980,8003,8004,8006,8012,7890,86,8280,8028,9060,38501,38888,28017,8053,889,9085"

    # 这里有大概250个端口
    TOP_100 = "1000,10000,10001,10030,1024,10250,10255,10256,10443,1080,1099,110,111,11211,123,12300,1234,12345,12578,13000,135,137,138,139,14000,143,1433,1434,1443,15000,15001,15002,1515,1521,16030,18001,18080,18081,1883,1988,2000,20000,20121,2049,2080,2081,2082,2083,2086,2087,20880,2096,21,2181,22,2222,22222,2323,25,2525,25672,26,27017,3000,30000,30001,30002,30003,30005,3001,30017,3002,3003,30080,3050,3306,3307,3333,3389,33890,3390,3446,3542,3689,389,4000,40001,4007,4040,443,4430,4433,444,4443,4444,445,465,4848,5000,5001,5002,5003,5005,50050,5006,50060,5007,50070,50075,50090,5050,5060,5222,5357,5432,554,5555,55555,5601,5671,5672,5673,5678,5801,587,5985,5986,6000,6060,6066,6080,6379,6380,6443,6446,6588,666,6665,6666,6699,6780,6868,7000,7001,7002,7003,7005,7010,7019,7070,7071,7080,7180,7443,7547,777,7776,7777,80,800,8000,8001,8002,8003,8005,8006,8008,8009,801,8010,8020,8025,8030,8031,8032,8060,8069,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8098,8099,81,8123,8150,8161,8162,8166,8180,8181,8191,82,8288,83,84,8443,8480,85,8686,873,8765,88,880,8800,8848,888,8880,8883,8887,8888,8889,8890,8899,8983,8989,8999,9000,9001,9002,9003,9080,9083,9090,9091,9099,9100,9109,9171,9172,9191,9200,9201,9202,9300,9301,9302,9443,9527,9529,9864,9870,9876,9944,999,9998,9999,8100"

    # 常见16个WEB端口
    TOP_10 = "80,443,8443,8080,8081,8888,8089,5000,5001,8085,800,81,9000,88,8001,8090"

    FOFA_KEY = ""
    FOFA_URL = "https://fofa.info"
    FOFA_MAX_PAGE = 5      # 最大查询页数
    FOFA_PAGE_SIZE = 2000  # 每页2000条

    AUTH = False
    API_KEY = ""
    
    BLACK_IPS = []

    GEOIP_ASN = ""
    GEOIP_CITY = ""

    FILE_LEAK_TOP_2k = os.path.join(basedir, 'dicts/file_top_2000.txt')
    FILE_LEAK_TOP_200 = os.path.join(basedir, 'dicts/file_top_200.txt')

    DOMAIN_MAX_LEN = 25  # 不包括下发的目标域名长度，

    DINGDING_SECRET = ""
    DINGDING_ACCESS_TOKEN = ""

    FEISHU_WEBHOOK = ""
    FEISHU_SECRET = ""

    WX_WORK_WEBHOOK = ""

    EMAIL_HOST = ""
    EMAIL_PORT = ""
    EMAIL_USERNAME = ""
    EMAIL_PASSWORD = ""
    EMAIL_TO = ""

    GITHUB_TOKEN = ""
    GITHUB_HASH_FILE = os.path.join(TMP_PATH, 'github.hash')

    # 域名爆破并发数
    DOMAIN_BRUTE_CONCURRENT = 300
    # 组合生成的域名爆破并发数
    ALT_DNS_CONCURRENT = 1500
    FORBIDDEN_DOMAINS = []
    # 代理地址
    PROXY_URL = ""

    QUERY_PLUGIN_CONFIG = dict()

    WEB_HOOK_URL = ""
    WEB_HOOK_TOKEN = ""


try:
    with open(os.path.join(basedir, 'config.yaml')) as f:
        y = yaml.load(f, Loader=yaml.SafeLoader)

    Config.MONGO_URL = y["MONGO"]["URI"]
    Config.MONGO_DB = y["MONGO"]["DB"]

    Config.CELERY_BROKER_URL = y["CELERY"]["BROKER_URL"]

    # *** Fofa 配置 ***
    Config.FOFA_KEY = y["FOFA"]["KEY"]
    if y["FOFA"].get("URL"):
        Config.FOFA_URL = y["FOFA"]["URL"]

    if y["FOFA"].get("MAX_PAGE"):
        Config.FOFA_MAX_PAGE = y["FOFA"]["MAX_PAGE"]

    if y["FOFA"].get("PAGE_SIZE"):
        Config.FOFA_PAGE_SIZE = y["FOFA"]["PAGE_SIZE"]

    # *** GEOIP 配置 ***
    Config.GEOIP_CITY = y["GEOIP"]["CITY"]
    Config.GEOIP_ASN = y["GEOIP"]["ASN"]

    Config.AUTH = y["CASM"]["AUTH"]
    Config.API_KEY = y["CASM"]["API_KEY"]
    Config.BLACK_IPS = y["CASM"]["BLACK_IPS"]

    # *** TOP 10 端口设置 ***
    if y["CASM"].get("PORT_TOP_10"):
        Config.TOP_10 = y["CASM"]["PORT_TOP_10"]

    # *** 文件泄漏字典 ***
    if y["CASM"].get("FILE_LEAK_DICT"):
        file_leak_dict = y["CASM"]["FILE_LEAK_DICT"]
        if os.path.isfile(file_leak_dict):
            Config.FILE_LEAK_TOP_2k = file_leak_dict
        else:
            print("Warning {} is not file".format(file_leak_dict))

    # *** 域名爆破字典 ***
    if y["CASM"].get("DOMAIN_DICT"):
        domain_dict = y["CASM"]["DOMAIN_DICT"]
        if os.path.isfile(domain_dict):
            Config.DOMAIN_DICT_2W = domain_dict
        else:
            print("Warning {} is not file".format(domain_dict))

    # *** 钉钉配置 ***
    if y.get("DINGDING"):
        if y["DINGDING"].get("SECRET"):
            Config.DINGDING_SECRET = y["DINGDING"]["SECRET"]

        if y["DINGDING"].get("ACCESS_TOKEN"):
            Config.DINGDING_ACCESS_TOKEN = y["DINGDING"]["ACCESS_TOKEN"]

    # *** 邮箱配置 ***
    if y.get("EMAIL"):
        if y["EMAIL"].get("HOST"):
            Config.EMAIL_HOST = y["EMAIL"]["HOST"]

        if y["EMAIL"].get("PORT"):
            Config.EMAIL_PORT = int(y["EMAIL"]["PORT"])

        if y["EMAIL"].get("USERNAME"):
            Config.EMAIL_USERNAME = y["EMAIL"]["USERNAME"]

        if y["EMAIL"].get("PASSWORD"):
            Config.EMAIL_PASSWORD = y["EMAIL"]["PASSWORD"]

        if y["EMAIL"].get("TO"):
            Config.EMAIL_TO = y["EMAIL"]["TO"]

    # *** GITHUB TOKEN 配置 ***
    if y.get("GITHUB"):
        if y["GITHUB"].get("TOKEN"):
            Config.GITHUB_TOKEN = y["GITHUB"]["TOKEN"]

    # *** 域名爆破并发数 ***
    domain_concurrent = y["CASM"].get("DOMAIN_BRUTE_CONCURRENT")
    if domain_concurrent:
        int(domain_concurrent)
        Config.DOMAIN_BRUTE_CONCURRENT = domain_concurrent

    # *** 组合生成的域名爆破并发数 ***
    alt_dns_concurrent = y["CASM"].get("ALT_DNS_CONCURRENT")
    if alt_dns_concurrent:
        int(alt_dns_concurrent)
        Config.ALT_DNS_CONCURRENT = alt_dns_concurrent

    # *** 代理配置 ***
    if y.get("PROXY"):
        if y["PROXY"].get("HTTP_URL"):
            Config.PROXY_URL = y["PROXY"]["HTTP_URL"]

    # *** 域名查询插件配置 ***
    if y.get("QUERY_PLUGIN"):
        query_plugin_conf = y["QUERY_PLUGIN"]
        if isinstance(query_plugin_conf, dict):
            Config.QUERY_PLUGIN_CONFIG = query_plugin_conf

    # *** WEBHOOK 配置文件 ***
    if y.get("WEBHOOK"):
        if y["WEBHOOK"].get("URL"):
            Config.WEB_HOOK_URL = y["WEBHOOK"]["URL"]
        if y["WEBHOOK"].get("TOKEN"):
            Config.WEB_HOOK_TOKEN = y["WEBHOOK"]["TOKEN"]

    # *** 飞书消息推送配置 ***
    if y.get("FEISHU"):
        if y["FEISHU"].get("WEBHOOK_URL"):
            Config.FEISHU_WEBHOOK = y["FEISHU"]["WEBHOOK_URL"]
        if y["FEISHU"].get("SECRET"):
            Config.FEISHU_SECRET = y["FEISHU"]["SECRET"]

    # *** 企业微信推送配置 ***
    if y.get("WXWORK"):
        if y["WXWORK"].get("WEBHOOK_URL"):
            Config.WX_WORK_WEBHOOK = y["WXWORK"]["WEBHOOK_URL"]

except Exception as e:
    print("Parse config.yaml error {}".format(e))
    sys.exit(-1)
