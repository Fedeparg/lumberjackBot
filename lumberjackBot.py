import pyautogui
import struct
import Quartz.CoreGraphics as CG
import time


class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, region=None):
        """region should be a CGRect, something like:

        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)

        The default region is CG.CGRectInfinite (captures the full screen)
        """

        if region is None:
            region = CG.CGRectInfinite
        # else:
            # TODO: Odd widths cause the image to warp. This is likely
            # caused by offset calculation in ScreenPixel.pixel, and
            # could could modified to allow odd-widths
            # if region.size.width % 2 > 0:
            #     emsg = "Capture region width should be even (was %s)" % (
            #         region.size.width)
            #     raise ValueError(emsg)

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
        data_format = 'BBBB'

        # Calculate offset, based on
        # http://www.markj.net/iphone-uiimage-pixel-color/
        offset = 4 * ((self.width*int(round(y))) + int(round(x)))

        # Unpack data from string into Python'y integers
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)

        # Return BGRA as RGBA
        return (r, g, b, a)


class lumberjackBot():

    def __init__(self, playX, playY, treeX, treeY, branchX, branchY):
        self.playX = playX
        self.playY = playY
        self.treeX = treeX
        self.treeY = treeY
        self.branchX = branchX
        self.branchY = branchY
        # Know if branch is right or left of the tree
        if self.branchX/2 > self.treeX/2:
            self.right_branch = True
        else:
            self.right_branch = False
        self.movement_buffer = ['right']

        self.pixel = ScreenPixel()
        # We just need to check for 1 pixel where the branch is
        self.region = CG.CGRectMake(branchX/2, branchY/2, 1, 1)

    def move(self, direction):
        self.movement_buffer.append(direction)
        speed = 0.0305  # 2 frames aprox.

        # Always double movement because there is a gap between branches
        if self.movement_buffer[0] == 'left':
            print('left')
            pyautogui.typewrite(['left', 'left'], speed)
        elif self.movement_buffer[0] == 'right':
            print('right')
            pyautogui.typewrite(['right', 'right'], speed)
        self.movement_buffer = self.movement_buffer[1:]

    def play(self):
        while True:
            self.pixel.capture(region=self.region)
            pixel_color = self.pixel.pixel(0, 0)

            # Only check for blue > 200 to check for branch vs sky
            if self.right_branch:
                if pixel_color[2] < 200:
                    self.move('left')
                else:
                    self.move('right')
            else:
                if pixel_color[2] < 200:
                    self.move('right')
                else:
                    self.move('left')


def lowest_branch(branches):
    bottom_most = None
    # Search for the lowest branch
    for branch in branches:
        if bottom_most is None:
            bottom_most = branch
        elif branch[1] >= bottom_most[1]:
            bottom_most = branch
    return bottom_most[:2]


if __name__ == '__main__':
    print(f'Running in 3 seconds. To stop the program drag the mouse to the top-left corner of your screen.')
    time.sleep(3)
    playX, playY = pyautogui.locateCenterOnScreen(
        'imgs/play.png', confidence=0.9)
    # Any resolution divided by 2 is to take into account retina display and defualt
    # screen scale that Apple uses
    playX, playY = round(playX/2), round(playY/2)
    pyautogui.moveTo(playX, playY)
    # Start the game by pressing play button. Does not work with replay.
    pyautogui.click()
    time.sleep(0.5)     # Wait for screen refresh
    branches = pyautogui.locateAllOnScreen('imgs/branch.png', confidence=0.9)
    branchX, branchY = lowest_branch(branches)
    pyautogui.moveTo(branchX/2, branchY/2)
    treeX, treeY = pyautogui.locateCenterOnScreen(
        'imgs/tree.png', confidence=0.9)
    print(f'Im playing...')
    lumberjack = lumberjackBot(playX, playY, treeX, treeY, branchX, branchY)
    lumberjack.play()   # Game start
