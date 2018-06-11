# -*-coding=utf-8-*-

from qiniu import Auth, put_file

# 注意保密
access_key = 'TT3fdeipi7cBeD1gkS7pERrE4jnBOBHGxAN26WQc'
secret_key = 'RtwzwEUNQy7cFPMKadkZhlHG8x3Fu-uPIWi-1Rq_'

# 上传空间
bucket_name = 'raspberry'

# 外链域名
domain = 'p8gmgpo3k.bkt.clouddn.com'


q = Auth(access_key, secret_key)

def store(localFilePath,remoteFileName):
    # 生成上传token
    token = q.upload_token(bucket_name, remoteFileName, 3600)
    ret,info = put_file(token,remoteFileName,localFilePath)
    if info.status_code == 200:
        return UploadResult(True,ret['key'])
    else:
        return UploadResult(False,exception = info.exception)

class UploadResult(object):

    def __init__(self, ret, filename='', exception=''):
        self.ret = ret
        self.filename = filename
        self.exception = exception


def assemblePicUrl(picname):
    return 'http://'+domain+'/'+picname
