import cv2
from deepface import DeepFace
import json

print("imported packages")

# settings
drawBorderFrame = True
drawEmotion = True
drawPercentage = True
drawFrame = True
textColor = (0, 0, 255)
boxColor = (0, 0, 255)

try:
    with open('settings.json', 'r') as f:
        settings = json.loads(f.read())

        if settings.get('text-color') != None:
            h = settings.get('text-color')[1:]
            textColor = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))[::-1]

        if settings.get('box-color') != None:
            h = settings.get('box-color')[1:]
            boxColor = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))[::-1]

        drawBorderFrame = settings['render-box']
        drawEmotion = settings['render-text']
        drawFrame = settings['render-frames']
        drawPercentage = settings['render-percentage']
except:
    print('error loading settings from settings.json')

# capturing video
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    raise IOError('unale to open webcam')
print('opened webcam')

while True:
    # get frame from capture
    ret, frame = capture.read()

    pretty = ''

    try:
        # detecting the emotion
        predictions = DeepFace.analyze(frame, actions=['race'])
        # print(predictions)

        pretty = f"{predictions['dominant_race']}"
        if drawPercentage:
            pretty += f" {round(predictions['race'][predictions['dominant_race']])}%"
        print(pretty)

        #  drawing frame
        if drawBorderFrame and drawFrame:
            x = predictions['region']['x']
            y = predictions['region']['y']
            w = predictions['region']['w']
            h = predictions['region']['h']
            cv2.rectangle(frame, (x, y), (x+w, y+h), boxColor, 2)

    except:
        print('could not find face')

    # drawing emotion
    if drawEmotion and drawFrame:
        font = cv2.FONT_HERSHEY_PLAIN
        _ = cv2.putText(frame, pretty, (0, 25), font,
                        2, textColor, 2, cv2.LINE_4)

    # displaying frame
    if drawFrame:
        cv2.imshow('emotion-detection', frame)
        # quit if user hits q on keyboard
        if cv2.waitKey(2) & 0xff == ord('q'):
            break

capture.release()
cv2.destroyAllWindows()
