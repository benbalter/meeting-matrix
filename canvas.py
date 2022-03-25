try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ModuleNotFoundError as error:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics

import logging
import inflect

logger = logging.getLogger('meeting_matrix')


class Canvas:
    """
    Manages drawing to the matrix
    """

    def __init__(self):
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.gpio_slowdown = 2
        options.hardware_mapping = 'adafruit-hat'
        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()
        self.inflect_engine = inflect.engine()

    def load_font(self, size):
        """
        Returns the font of the specified size
        """
        font = graphics.Font()
        path = f'./rpi-rgb-led-matrix/fonts/{size}.bdf'
        font.LoadFont(path)
        return font

    def clear(self):
        """
        Clears the canvas
        """
        logger.info("Clearing canvas")
        self.matrix.Clear()
        self.canvas.Clear()
        self.swap_canvas()

    def swap_canvas(self):
        """
        Prints the current canvas to the matrix
        """
        logger.info("Swapping canvas")
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def center_point(self, text, font_size):
        """
        Returns the x,y coordinates that centers the text horizontally
        """
        font = self.load_font(font_size)

        width = 0
        for char in text:
            width = width + font.CharacterWidth(ord(char))

        return (self.canvas.width / 2) - (width / 2)

    def print_minutes_remaining(self, event):
        """
        Given an event, prints the number of minutes remaining
        """
        minutes_remaining = event.minutes_remaining()
        minute = self.inflect_engine.plural("minute", minutes_remaining)

        minutes_remaining = str(minutes_remaining)
        self.print_centered(text=minutes_remaining, font_size="9x15", y=15)
        self.print_centered(text=minute, y=25)
        self.swap_canvas()

    def print_centered(self, text="", font_size="6x10", y=10):
        """
        Prints the given string horizontally centered on the matrix
        """
        center = self.center_point(text, font_size)
        self.print_text(text=text, x=center, y=y, font_size=font_size)

    def print_text(self, text="", x=2, y=10, font_size="6x10"):
        """
        Prints the given text to the matrix
        """
        logger.info("Printing %s at %d x %d with font %s",
                    text, x, y, font_size)

        font = self.load_font(font_size)
        blue = graphics.Color(0, 0, 255)
        graphics.DrawText(self.canvas, font, x, y, blue, text)
