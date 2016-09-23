from tkinter import *
import string

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

####################################
# customize these functions
####################################

def init(data):
    data.level = 0
    data.curNum = None
    pass

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if event.keysym == "Return":
        if data.curNum != None:
            data.level = int(data.curNum)
            data.curNum = None
    elif event.keysym in string.digits:
        if data.curNum == None:
            data.curNum = event.keysym
        else:
            data.curNum += event.keysym

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawFractal(canvas, data)
    drawLevel(canvas, data)
    pass

def drawLevel(canvas, data):
    level = str(data.level)
    canvas.create_text(data.width//2, data.height//6, 
        text = "Current Level: " + level, fill = "white", 
        font = "Helvetica 26 bold")

def drawFractal(canvas, data):
    if data.level == 0: 
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")
        return
    level = data.level
    width = data.width
    height = data.height
    colorStepSize = 255 / level
    widthStepSize = width / level
    heightStepSize = height / level
    drawGradient(canvas, level, width, height, colorStepSize, widthStepSize, 
        heightStepSize)

def drawGradient(canvas, level, w, h, dC, dX, dY, c = 0, x = 0, y = 0):
    if level == 0: return
    else:
        x0 = x // 1
        y0 = y // 1
        c0 = int(c)
        gray = rgbString(c0, c0, c0)
        canvas.create_rectangle(x0, y0, w, h, fill = gray, outline = gray)
        drawGradient(canvas, level - 1, w, h, dC, dX, dY, c + dC, x + dX, 
            y + dY)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)