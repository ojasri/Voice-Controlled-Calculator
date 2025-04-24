import cv2
from cvzone.HandTrackingModule import HandDetector

# Button class
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 65), cv2.FONT_HERSHEY_PLAIN,
                    3, (50, 50, 50), 3)

    def checkClick(self, x, y):
        return self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height


# Define button values
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

# Create button objects
buttonList = []
for y in range(4):
    for x in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Equation holder
myEquation = ''
delayCounter = 0

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)   # height
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Draw display box
    cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100), (50, 50, 50), 3)

    # Draw buttons
    for button in buttonList:
        button.draw(img)

    if hands:
        lmList = hands[0]['lmList']
        x, y = lmList[8][0], lmList[8][1]

        # Find distance between index and middle finger
        length, info, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

        if length < 40 and delayCounter == 0:
            for button in buttonList:
                if button.checkClick(x, y):
                    val = button.value
                    if val == '=':
                        try:
                            myEquation = str(eval(myEquation))
                        except:
                            myEquation = "Error"
                    else:
                        myEquation += val
                    delayCounter = 1

    # Delay counter to prevent multiple clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Display the equation
    cv2.putText(img, myEquation, (810, 130), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    cv2.imshow("Virtual Calculator", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
