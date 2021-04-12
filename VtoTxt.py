import cv2  # 利用opencv读取图像
# import numpy as np
# 利用matplotlib显示图像
# import matplotlib.pyplot as plt
import os
import time
import sys

#改变视频码率
def modify_video_frame_rate(videoPath,destFps):
    dir_name = os.path.dirname(videoPath)
    basename = os.path.basename(videoPath)
    video_name = basename[:basename.rfind('.')]
    video_name = video_name + "moify_fps_rate"
    resultVideoPath = f'./{video_name}.mp4'

    videoCapture = cv2.VideoCapture(videoPath)

    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    if fps != destFps:
        frameSize = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        #这里的VideoWriter_fourcc需要多测试，如果编码器不对则会提示报错，根据报错信息修改编码器即可
        videoWriter = cv2.VideoWriter(resultVideoPath,cv2.VideoWriter_fourcc('m','p','4','v'),destFps,frameSize)

        i = 0;
        while True:
            success,frame = videoCapture.read()
            if success:
                i+=1
                videoWriter.write(frame)
            else:
                return resultVideoPath
      
def ImgToTxt(img):
    img = cv2.imread(img)  # 读取图像
    # 显示图像
    height, width = img.shape[:2]
    rage = 1 / (height / int(sys.argv[4]))
    size = (int(width * rage), int(height * rage))
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 将图片转换为灰度图
    ret, img_gray = cv2.threshold(img_gray, int(sys.argv[3]), 255, cv2.THRESH_BINARY)
    high = len(img_gray)
    weith = len(img_gray[0])
    # 需要几列或者几行相加
    # 35行
    txtImg = [[0] * weith] * high
    print("\n"*80)
    for i in range(int(high)):
        printTxt = ""
        for j in range(int(weith)):
            if img_gray[i][j] == 255:
                printTxt = printTxt + "1 "
            else:
                printTxt = printTxt + "@ "
        print(printTxt)
    #os.system("cls")
    
def videoToText(VPath):
    video_full_path=modify_video_frame_rate(VPath,int(sys.argv[5]))
    cap = cv2.VideoCapture(video_full_path)
    frame_count = cap.get(cv2.CAP_PROP_FPS)
    #1帧持续的时间为：
    NeedTime = (1/frame_count)
    #print(cap.isOpened())
    success = True
    #print(frame_count)
    print(sys.argv[1])
    while success:
        success, frame = cap.read()
        # params.append(cv.CV_IMWRITE_PXM_BINARY)
        # cv2.imshow("111", frame)
        start = time.time()
        if success:
            res = cv2.imwrite("video.jpg", frame)
            if res:
                ImgToTxt("./video.jpg")
        end = time.time()
        UseTime = end-start
        WaitTime = NeedTime - UseTime
        if WaitTime>0:
            time.sleep(WaitTime)
    cap.release()

'''cv2.imshow("111", img_gray)
plt.imshow(img_gray)
plt.axis('off')
plt.show()'''
# 参数说明
'''python VToTxt.py v haha.mp4 185 45 10
VToTxt.py:程序名称
v：视频  i：图像
haha.mp4：文件名
185：阈值
45：生成TXT的高度
10：帧速率，仅在v选项下才有用
'''
if __name__ == '__main__':
    if sys.argv[1] == 'i':
        if len(sys.argv)!=5:
            print("检查参数")
        ImgToTxt(sys.argv[2])
    elif sys.argv[1] == 'v':
        if len(sys.argv)!=6:
            print("检查参数")
        videoToText(sys.argv[2])

