import cv2

def outlineRectangle(rect, image, color):
    '''Wrapper around the cv2.rectangle() to get compatible interface'''
    if rect is None:
        return
    x, y, w, h = rect
    #color is a bgr triplet or a grayscale value
    cv2.rectangle(image, (x,y), (x+w,y+h), color)


def copyRect(src, dest, srcRect, destRect, interpolation=cv2.INTER_LINEAR):
    xs, ys, ws, hs = srcRect
    xd, yd, wd, hd = destRect
    dest[yd:yd+hd, xd:xd+wd] = cv2.resize(src[ys:ys+hs, xs:xs+ws], (wd,hd), interpolation=interpolation)


def swapRects(src, dest, rects, interpolation=cv2.INTER_LINEAR):

    if dest is not src:
        #make destinationsame as src
        dest[:] = src

    numRects = len(rects)
    if numRects < 2:
        return
    #keep a temp array of the last rectange
    x, y, w, h = rects[numRects -1]
    tempArray = src[y:y+h, x:x+w].copy()

    i = numRects - 2
    while i >= 0:
        copyRect(src, dest, rects[i], rects[i+1], interpolation=interpolation)
        i -= 1
    #copying the temp array (last rect) to the first rect
    #tempArray starts from (0,0) and goes to (w,h)
    copyRect(tempArray, dest, (0, 0, w, h), rects[0], interpolation=interpolation)


    



