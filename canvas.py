from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import logging

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
        #options.pixel_mapper_config = 'mirror:h'
        self.matrix = RGBMatrix(options=options)

        self.font = graphics.Font()
        self.font.LoadFont("../rpi-rgb-led-matrix/fonts/7x13.bdf")

    def print_text(self, text):
        """
        Prints the given text to the matrix
        """
        logging.info("Printing %s", text)
        
        blue = graphics.Color(0, 0, 255)
        graphics.DrawText(self.matrix, self.font, 2, 10, blue, text)
