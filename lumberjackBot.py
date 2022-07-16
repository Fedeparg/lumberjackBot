from typing import Iterator
import pyautogui
from PIL import ImageGrab
import struct
import Quartz.CoreGraphics as CG
import time

class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """
 
    def capture(self, region = None):
        """region should be a CGRect, something like:
 
        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)
 
        The default region is CG.CGRectInfinite (captures the full screen)
        """
 
        if region is None:
            region = CG.CGRectInfinite
        else:
            # TODO: Odd widths cause the image to warp. This is likely
            # caused by offset calculation in ScreenPixel.pixel, and
            # could could modified to allow odd-widths
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)
 
        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)
 
        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)
 
        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)
 
        # Get width/height of image
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)
 
    def pixel(self, x, y):
        """Get pixel value at given (x,y) screen coordinates
 
        Must call capture first.
        """
 
        # Pixel data is unsigned char (8bit unsigned integer),
        # and there are for (blue,green,red,alpha)
        data_format = "BBBB"
 
        # Calculate offset, based on
        # http://www.markj.net/iphone-uiimage-pixel-color/
        offset = 4 * ((self.width*int(round(y))) + int(round(x)))
 
        # Unpack data from string into Python'y integers
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)
 
        # Return BGRA as RGBA
        return (r, g, b, a)
class lumberjackBot():

    def __init__(self, playX, playY, treeX, treeY, x, y):
        self.playX = playX
        self.playY = playY
        self.treeX = treeX
        self.treeY = treeY
        # Those attributes has been placed here in order to save calcs:
        self.x = x    # Left side branch X location
        self.y = y   # Left side branch Y location
        if self.x/2 > self.treeX/2:
            self.right = True
        else:
            self.right = False
        self.movement_buffer = ['right']

        self.pixel = ScreenPixel()
        self.region = CG.CGRectMake(x/2, y/2, 2, 2)

    def move(self, direction):
        self.movement_buffer.append(direction)
        speed = 0
        if self.movement_buffer[0] == "left":
            print('left')
            pyautogui.typewrite(['left', 'left'], speed)
        elif self.movement_buffer[0]  == "right":
            print('right')
            pyautogui.typewrite(['right', 'right'], speed)
        self.movement_buffer = self.movement_buffer[1:]
        time.sleep(0.06)

    def get_pixel(self, x, y):    # Modify class atribute
        # screen = windll.user32.GetDC(0)
        # rgb = windll.gdi32.GetPixel(screen, x, y)
        #rgb = pyautogui.pixel(x, y)
        rgb = ImageGrab.grab().getpixel((x, y))
        # return self.get_color(rgb)
        return rgb

    def play(self):
        while True:
            self.pixel.capture(region=self.region)
            pixel_color = self.pixel.pixel(0, 0)
            #pixel_color = self.get_pixel(self.x, self.y)
            if self.right:
                if pixel_color[2] < 200:
                    # print("right")
                    self.move("left")
                else:
                    # print("left")
                    self.move("right")
            else:
                if pixel_color[2] < 200:
                    # print("left")
                    self.move("right")
                else:
                    # print("right")
                    self.move("left")
            #print(pixel_color, self.x, self.y, self.movement_buffer)


def bottom_most_branch(branches: Iterator):
    bottom_most = None
    # Search for the branch most right and lower
    for branch in branches:
        if bottom_most is None:
            bottom_most = branch
        elif branch[1] >= bottom_most[1]:
                bottom_most = branch
    return bottom_most[:2]


if __name__ == "__main__":
    print("Running in 3 seconds, minimize this windows. To stop the program drag the mouse to the top-left corner of your screen.")
    time.sleep(3)
    playX, playY = pyautogui.locateCenterOnScreen('play.png', confidence=0.9)
    playX, playY = round(playX/2), round(playY/2)
    pyautogui.moveTo(playX, playY)
    pyautogui.click()   # Start the game by pressing play button
    time.sleep(0.5)     # Wait for screen refresh
    branches = pyautogui.locateAllOnScreen('branch.png', confidence=0.9)
    x, y = bottom_most_branch(branches)
    #x, y = x/2, y/2
    pyautogui.moveTo(x/2, y/2 + 5)
    treeX, treeY = playX - 6, playY - 177  # Tree position
    #treeX, treeY = treeX/2, treeY/2
    #time.sleep(0.3)
    treeX, treeY = pyautogui.locateCenterOnScreen('tree.png', confidence=0.9)
    print(f"Arbol: {treeX/2}, {treeY/2}")
    print("Im playing...")
    lumberjack = lumberjackBot(playX, playY, treeX, treeY, x, y)
    lumberjack.play()   # Game start
