import urllib.request
import ssl

# 取消SSL认证
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://data.stats.gov.cn/"

