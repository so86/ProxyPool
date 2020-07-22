from attr import attrs, attr


@attrs
class Proxy(object):
    """
    proxy schema
    """
    host = attr(type=str, default=None)
    port = attr(type=int, default=None)
    username = attr(type=str, default=None)
    password = attr(type=str, default=None)

    def __str__(self):
        """
        to string, for print
        :return:
        """
        if self.username is not None:
            return f'{self.username}:{self.password}@{self.host}:{self.port}'
        return f'{self.host}:{self.port}'
    
    def string(self):
        """
        to string
        :return: <host>:<port>
        """
        return self.__str__()


if __name__ == '__main__':
    proxy = Proxy(host='8.8.8.8', port=8888)
    print('proxy', proxy)
    print('proxy', proxy.string())

    proxy = Proxy(host='8.8.8.8', port=8888, username='u', password='pass')
    print('proxy', proxy.string())
