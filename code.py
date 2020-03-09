#哈希函数个数k，数组位数m，字符串数量n
#如申请内存256M，数组位数m=2^31约21.5亿，若选取k=7，当漏失率=8.56e-05是，m/n=23，n=0.93亿
#定制scrapy的url去重
from w3lib.util.url import canonicalize_url
from scrapy.dupefilter import RFPDupeFilter
class URLSha1Filter(RFPDupeFilter):
    def __init__(self,path=None):
        self.url_set=set()
        RFPDupeFilter.__init__(self,path)
    
    def request_set(self,request):
        fp=hashlib.sha1()
        fp.update(canonicalize_url(request.url))
        url_sha1=fp.hexdigest()
        if url_sha1 in self.url_set:
            return True
        else:
            self.url_set.add(url_sha1)

#添加bloomfilter
from pybloom import ScalableBloomFilter
class URLBloomFilter(RFPDupeFilter):
    def __init__(self,path=None):
        self.urls_sbf=ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        RFPDupeFilter.__init__(self,path)
    
    def request_set(self,request):
        fp=hashlib.sha1()
        fp.update(canonicalize_url(request.url))
        url_sha1=fp.hexdigest()
        if url_sha1 in self.urls_sbf:
            return True
        else:
            self.urls_sbf.add(url_sha1)
        
