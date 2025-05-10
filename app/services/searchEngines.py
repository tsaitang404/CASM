import re
from pyquery import PyQuery as pq
import time
from urllib.parse import quote, urljoin, urlparse
from app import utils
from app.config import Config

logger = utils.get_logger()


class BaiduSearch(object):
    def __init__(self, keyword=None, page_num=6):
        self.search_url = "https://www.baidu.com/s?rn=100&pn={page}&wd={keyword}"
        self.num_pattern = re.compile(r'百度为您找到相关结果约?([\d,]*)个')
        self.first_html = ""
        self.keyword = keyword
        self.page_num = page_num
        self.pq_query = "#content_left h3.t a"
        self.headers = {"Accept-Language": "zh-cn"}
        self.search_result_num = 0
        self.default_interval = 3

    def result_num(self):
        url = self.search_url.format(page=0, keyword=quote(self.keyword))
        html = utils.http_req(url, headers=self.headers).text
        self.first_html = html
        result = re.findall(self.num_pattern, html)
        if not result:
            logger.warning("Unable to get baidu search results， {}".format(self.keyword))
            return 0

        num = int("".join(result[0].split(",")))
        self.search_result_num = num
        return num

    def match_urls(self, html):
        result = re.findall(self.num_pattern, html)
        if not result:
            raise Exception("获取百度结果异常")

        dom = pq(html)
        result_items = dom(self.pq_query).items()
        urls_result = [item.attr("href") for item in result_items]
        urls = set()
        for u in urls_result:
            try:
                if not re.match(r'^https?:/{2}\w.+$', u):
                    logger.info("url {} is invalid".format(u))
                    continue
                resp = utils.http_req(u, "head")
                real_url = resp.headers.get('Location')
                if real_url:
                    urls.add(real_url)
            except Exception as e:
                logger.exception(e)
        return list(urls)

    def run(self):
        self.result_num()
        logger.info("baidu search {} results found for keyword {}".format(self.search_result_num, self.keyword))
        urls = []

        # 没有找到直接return
        if self.search_result_num == 0:
            return urls

        for page in range(1, min(int(self.search_result_num / 10) + 2, self.page_num + 1)):
            if page == 1:
                _urls = self.match_urls(self.first_html)
                urls.extend(_urls)
                logger.info("baidu firsturl result {}".format(len(_urls)))
            else:
                time.sleep(self.default_interval)
                url = self.search_url.format(page=(page - 1) * 10, keyword=quote(self.keyword))
                html = utils.http_req(url, headers=self.headers).text
                _urls = self.match_urls(html)
                logger.info("baidu search url {}, result {}".format(url, len(_urls)))
                urls.extend(_urls)
        return urls


class BingSearch(object):
    def __init__(self, keyword=None, page_num=6):
        self.search_url = "https://cn.bing.com/search?q={keyword}&qs=n&form=QBRE&sp=-1&first={page}"
        # 增加多种匹配模式以适应不同的Bing响应格式
        self.num_pattern = re.compile(r'<span class="sb_count">([^<]+)</span>')
        self.num_pattern_alt1 = re.compile(r'<span[^>]*>([0-9,]+ 条结果)<\/span>')
        self.num_pattern_alt2 = re.compile(r'([0-9,]+ 个结果)')
        self.pq_query = "#b_results > li h2 > a"
        self.keyword = keyword
        self.page_num = page_num
        # 增强请求头以更好地模拟真实浏览器
        self.headers = {
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"
        }
        self.default_interval = 5  # 增加间隔时间
        self.search_result_num = 0
        self.first_html = ""
        self.retry_count = 3  # 添加重试计数

    def result_num(self):
        url = self.search_url.format(page=1, keyword=quote(self.keyword))
        
        # 添加重试逻辑
        for attempt in range(self.retry_count):
            try:
                # 使用HTTP代理(如果配置了)
                if hasattr(Config, 'HTTP_PROXY') and Config.HTTP_PROXY:
                    proxies = {"http": Config.HTTP_PROXY, "https": Config.HTTP_PROXY}
                    html = utils.http_req(url, headers=self.headers, proxies=proxies).text
                else:
                    html = utils.http_req(url, headers=self.headers).text
                
                self.first_html = html
                
                # 尝试多种正则表达式匹配
                result = re.findall(self.num_pattern, html)
                
                if result:
                    # 第一种情况
                    result_num = re.findall(r"共 ([\d,]*) 条", result[0])
                    if result_num:
                        num = int("".join(result_num[0].split(",")))
                        self.search_result_num = num
                        return num
                    
                    # 第二种情况
                    result_num_2 = re.findall(r" ([\d,]*) 个结果", result[0])
                    if result_num_2:
                        num = int("".join(result_num_2[0].split(",")))
                        self.search_result_num = num
                        return num
                
                # 尝试替代的正则表达式模式
                alt_result = re.findall(self.num_pattern_alt1, html)
                if alt_result:
                    num_str = re.sub(r'[^\d]', '', alt_result[0])
                    if num_str:
                        self.search_result_num = int(num_str)
                        return self.search_result_num
                
                alt_result2 = re.findall(self.num_pattern_alt2, html)
                if alt_result2:
                    num_str = re.sub(r'[^\d]', '', alt_result2[0])
                    if num_str:
                        self.search_result_num = int(num_str)
                        return self.search_result_num
                
                # 如果所有正则匹配都失败，但我们至少找到了一些结果链接，返回一个估计值
                if "搜索</title>" in html:
                    dom = pq(html)
                    result_items = list(dom(self.pq_query).items())
                    if result_items:
                        self.search_result_num = len(result_items) * 10  # 估计值
                        logger.info(f"估计 Bing 搜索结果数量: {self.search_result_num}")
                        return self.search_result_num
                
                # 如果是最后一次尝试，记录警告
                if attempt == self.retry_count - 1:
                    logger.warning(f"Unable to get bing search results for {self.keyword}, tried {attempt+1} times")
                    # 保存HTML以供调试
                    with open(f'/tmp/bing_search_debug_{int(time.time())}.html', 'w') as f:
                        f.write(html)
                    return 0
                
                # 如果不是最后一次尝试，等待后重试
                time.sleep(2 * (attempt + 1))
            
            except Exception as e:
                if attempt == self.retry_count - 1:
                    logger.exception(f"Bing search error: {str(e)}")
                    return 0
                time.sleep(2 * (attempt + 1))
        
        return 0

    def match_urls(self, html):
        try:
            dom = pq(html)
            result_items = dom(self.pq_query).items()
            urls_result = [item.attr("href") for item in result_items if item.attr("href")]
            urls = set()
            for u in urls_result:
                if not u:
                    continue
                urls.add(u)
            return list(urls)
        except Exception as e:
            logger.warning(f"解析Bing搜索结果出错: {str(e)}")
            return []

    def run(self):
        self.result_num()
        logger.info("bing search {} results found for keyword {}".format(self.search_result_num, self.keyword))
        urls = []

        # 没有找到直接return
        if self.search_result_num == 0:
            return urls

        for page in range(1, min(int(self.search_result_num / 10) + 2, self.page_num + 1)):
            if page == 1:
                _urls = self.match_urls(self.first_html)
                urls.extend(_urls)
                logger.info("bing search first url result {}".format(len(_urls)))
            else:
                time.sleep(self.default_interval)
                url = self.search_url.format(page=(page - 1) * 10, keyword=quote(self.keyword))
                try:
                    # 使用HTTP代理(如果配置了)
                    if hasattr(Config, 'HTTP_PROXY') and Config.HTTP_PROXY:
                        proxies = {"http": Config.HTTP_PROXY, "https": Config.HTTP_PROXY}
                        html = utils.http_req(url, headers=self.headers, proxies=proxies).text
                    else:
                        html = utils.http_req(url, headers=self.headers).text
                    
                    _urls = self.match_urls(html)
                    logger.info("bing search url {}, result {}".format(url, len(_urls)))
                    urls.extend(_urls)
                except Exception as e:
                    logger.warning(f"无法获取Bing搜索结果页面 {page}: {str(e)}")
        
        return urls


def baidu_search(domain, page_num=6):
    keyword = "site:{}".format(domain)
    b = BaiduSearch(keyword, page_num)
    urls = b.run()
    urls = [u for u in urls if domain in urlparse(u).netloc]
    return utils.rm_similar_url(urls)


def bing_search(domain, page_num=5):
    urls = []
    keyword = "site:{}".format(domain)
    b = BingSearch(keyword, page_num)
    urls.extend(b.run())
    if b.search_result_num > 1000 and len(urls) > 25:
        keywords = ["admin", "管理|后台", "登陆|密码", "login", "manage", "dashboard", "api",
                    "console"]
        for k in keywords:
            keyword = "site:{} {}".format(domain, k)
            try:
                time.sleep(15)
                b = BingSearch(keyword, page_num=1)
                urls.extend(b.run())
            except Exception as e:
                logger.warning(e)
    urls = [u for u in urls if domain in urlparse(u).netloc]
    return utils.rm_similar_url(urls)


class SearchEngines(object):
    # *** 调用搜索引擎查找URL
    def __init__(self, base_domain):
        self.engines = [bing_search, baidu_search]
        self.base_domain = base_domain

    def run(self):
        urls = []
        for engine in self.engines:
            try:
                urls.extend(engine(self.base_domain))
                urls = utils.rm_similar_url(urls)
            except Exception as e:
                logger.exception(e)

        return urls


def search_engines(base_domain):
    s = SearchEngines(base_domain)
    return s.run()


if __name__ == '__main__':
    for x in baidu_search("qq.com", 6):
        print(x)
