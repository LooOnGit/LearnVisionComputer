
# cat frame anh tu video
import cv2
# Function to extract frames
def FrameCapture(path):
    vidObj = cv2.VideoCapture(path)
    count = 0
    success = 1
    while success:
        success, image = vidObj.read()
        if count % 10 == 0:
            cv2.imwrite("dataset\\frame%d.jpg" % (count/10), image)
        count += 1
# Driver Code
if __name__ == '__main__': # can khi chay bang GPU
    # Calling the function
    FrameCapture("video.mp4")
