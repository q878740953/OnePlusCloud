# 作者：      此昵称不存在
# 创建时间    2020/3/4 21:07
# IDE       PyCharm
import json
import requests
import os


class dow_op_cloud:
    # 用户登录信息处

    def __init__(self):
        self.url = 'https://cloud.h2os.com/gallery/pc/listNormalPhotos'
        self.real_url = 'https://cloud.h2os.com/gallery/pc/getRealPhotoUrls'
        self.cookies = {
            "删除我，粘贴刚刚复制的代码双引号也要删除"

        }

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://cloud.h2os.com',
            'Connection': 'keep-alive',
            'Referer': 'https://cloud.h2os.com/',
            'Cache-Control': 'max-age=0',
        }

    # 获取请求每页照片数据的关键值
    def data(self, cursor, photoIndex):
        data = {
            'size': '100',
            'state': 'active',
            'smallPhotoScaleParams': 'image/resize,m_mfit,h_250,w_250',
            'originalPhotoScaleParams': 'image/resize,m_mfit,h_1300,w_1300',
            'cursor': cursor,
            'photoIndex': photoIndex
        }
        return data

    # 请求数据，获取响应
    def send_request(self, data):
        response = requests.post(self.url, cookies=self.cookies, data=data, headers=self.headers)
        js_data = response.content.decode()
        return js_data

    # 处理数据，得到图片的id值，从而获取真实地址
    def id_addr(self, js_data):
        data_dict = json.loads(js_data)
        next_cursor = data_dict['lastMatchedMoment']
        next_photoIndex = data_dict['realPhotoIndex']
        photo_dict = {}
        for i in data_dict['photos']:
            num = len(data_dict['photos'][i])
            for n in range(num):
                id = [data_dict['photos'][i][n]['id']]
                data = {'ids': '%s' % id}
                photo_real = json.loads(requests.post(self.real_url, headers=self.headers, cookies=self.cookies,
                                                      data=data).content.decode())
                photo_dict[data_dict['photos'][i][n]['title']] = photo_real[id[0]]
        return photo_dict, next_cursor, next_photoIndex

    # 得到地址后，下载到本地
    def save_photo(self, photo_dict):
        for p in photo_dict:
            if os.path.exists(p):
                print("文件已经存在 : " + p)
            else:
                with open(p, 'wb') as f:
                    print('正在下载%s请耐心等待' % p)
                    f.write(requests.get(photo_dict[p]).content)
                    print("下载完成，正在下载下一个")

    def run(self):
        cursor = ''
        photoIndex = ''
        while True:
            data = self.data(cursor, photoIndex)
            js_data = self.send_request(data)
            photo_dict, next_cursor, next_photoIndex = self.id_addr(js_data)
            self.save_photo(photo_dict)
            cursor = next_cursor
            photoIndex = next_cursor


if __name__ == '__main__':
    op = dow_op_cloud()
    op.run()
