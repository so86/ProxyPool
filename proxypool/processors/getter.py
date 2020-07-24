from loguru import logger
from proxypool.storages.redis import RedisClient
from proxypool.setting import PROXY_NUMBER_MAX
from proxypool.crawlers import __all__ as crawlers_cls
import re
from proxypool.schemas.proxy import Proxy


class Getter(object):
    """
    getter of proxypool
    """

    def __init__(self):
        """
        init db and crawlers
        """
        self.redis = RedisClient()
        self.crawlers_cls = crawlers_cls
        self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]

    def is_full(self):
        """
        if proxypool if full
        return: bool
        """
        return self.redis.count() >= PROXY_NUMBER_MAX

    @logger.catch
    def run(self):
        """
        run crawlers to get proxy
        :return:
        """
        if self.is_full():
            return
        proxyfile = "staticproxy.txt"
        with open(proxyfile, 'r') as fh:
            proxylines = fh.readlines()
        logger.info(f'read {proxyfile}')
        for line in proxylines:
            if line.strip() != "" and not line.startswith("#"):
                line = line.replace("\r\n", "").replace("\n", "")
                pattern = re.compile(r'((?P<username>\S*?)\:(?P<password>\S*?)@)?(?P<ip>[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})\:(?P<port>\d*)')
                match = re.search(pattern, line)
                if match:
                    username = match.groupdict()['username']
                    password = match.groupdict()['password']
                    ip = match.groupdict()['ip']
                    port = match.groupdict()['port']
                    proxy = Proxy(host=ip, port=port, username=username, password=password)
                    logger.info("getproxy " + proxy.string())
                    self.redis.add(proxy)

        for crawler in self.crawlers:
            logger.info(f'crawler {crawler} to get proxy')
            for proxy in crawler.crawl():
                print(proxy.string())
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
