import cv2
from time import sleep

# You need to register your App first, and enter you API key/secret.
API_KEY = "fU5mrmK1jmuLFT3EAuZFbOXJQTPtyrbD"
API_SECRET = "u2dMk70WjUPLSqHkZ26drIIK98aAIZvv"
# 网络图片的URL地址,调用demo前请填上内容
# The url of network picture, please fill in the contents before calling demo
face_one = './zhou1.jpg'
# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
face_two = './cai1.jpg'
# 本地图片的地址,调用demo前请填上内容
# Local picture location, please fill in the contents before calling demo
face_three = './lin1.jpg'

face_four = './li1.jpg'

face_search = './image.jpg'
# Import system libraries and define helper functions
# 导入系统库并定义辅助函数

from pprint import pformat

def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))


    
from facepp import API, File

api = API(API_KEY, API_SECRET)

# 创建一个Faceset用来存储FaceToken
# create a Faceset to save FaceToken
ret = api.faceset.create(outer_id='facedetect')
print_result("faceset create", ret)

Face = {}

res = api.detect(image_file=File(face_one))
print_result("person_one", res)
Face['person_one'] = res["faces"][0]["face_token"]

res = api.detect(image_file=File(face_two))
print_result("person_two", res)
Face['person_two'] = res["faces"][0]["face_token"]

res = api.detect(image_file=File(face_three))
print_result("person_three", res)
Face['person_three'] = res["faces"][0]["face_token"]

res = api.detect(image_file=File(face_four))
print_result("person_four", res)
Face['person_four'] = res["faces"][0]["face_token"]

# 将得到的FaceToken存进Faceset里面
# save FaceToken in Faceset
api.faceset.update(outer_id='facedetect', face_tokens=Face.itervalues())

print(" Faceset is already prepared!! ")


#下面进行每隔5帧进行一次图像保存，保存之后进行图像检测。
video_capture = cv2.VideoCapture(0)
c = 1
timeB = 5

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if(c % timeB == 0):
        cv2.imwrite("./image.jpg",frame)
        ret = api.detect(image_file=File(face_search))
        print_result("detect", ret)
        search_result = api.search(face_token=ret["faces"][0]["face_token"], outer_id='facedetect')
        print_result('search', search_result)
        print '=' * 60
        for k, v in Face.iteritems():
            if v == search_result['results'][0]['face_token']:
                print 'The person with highest confidence:', k
    c = c + 1

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
