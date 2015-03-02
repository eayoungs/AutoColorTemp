import math
from colormath.color_objects import xyYColor

def _temp_to_white(t):
    """Convert color temperature to sRGB white point tuple."""
    # Use equation from:
    #   http://en.wikipedia.org/wiki/Planckian_locus#Approximation
    xc = 0.0
    if 1667.0 <= t and t <= 4000.0:
        xc = -0.2661239*(math.pow(10.0, 9.0)/math.pow(t, 3.0)) - 0.2343580*(math.pow(10.0, 6.0)/math.pow(t, 2.0)) + 0.8776956*(math.pow(10.0, 3.0)/float(t)) + 0.179910
    elif 4000 < t and t <= 25000.0:
        xc = -3.0258469*(math.pow(10.0, 9.0)/math.pow(t, 3.0)) + 2.1070379*(math.pow(10.0, 6.0)/math.pow(t, 2.0)) + 0.2226347*(math.pow(10.0, 3.0)/float(t)) + 0.240390
    else:
        raise ValueError('Temperature must be between 1667K and 25000K.')
    yc = 0.0
    if 1667.0 <= t and t <= 2222.0:
        yc = -1.1063814*math.pow(xc, 3.0) - 1.34811020*math.pow(xc, 2.0) + 2.18555832*xc - 0.20219683
    elif 2222.0 < t and t <= 4000.0:
        yc = -0.9549476*math.pow(xc, 3.0) - 1.37418593*math.pow(xc, 2.0) + 2.09137015*xc - 0.16748867
    elif 4000.0 < t and t <= 25000.0:
        yc =  3.0817580*math.pow(xc, 3.0) - 5.87338670*math.pow(xc, 2.0) + 3.75112997*xc - 0.37001483
    # Covert from full bright xyY color space to RGB (sRGB default) for white point at specified temp.
    white = xyYColor(xc, yc, 1.0).convert_to('rgb').get_value_tuple()
    # Return values normalized to 0-1.0 range.
    return (white[0] / 255.0, white[1] / 255.0, white[2] / 255.0)


def adjust_white_point(self, white):
        """Change the white point of the monitor to the specified value (tuple of 
        RGB floats, 0-1.0)."""
        # Set gamma ramp parameters.
        redMin = c_float(0.0)
        redMax = c_float(white[0])
        redGamma = c_float(self.gamma[0])
        greenMin = c_float(0.0)
        greenMax = c_float(white[1])
        greenGamma = c_float(self.gamma[1])
        blueMin = c_float(0.0)
        blueMax = c_float(white[2])
        blueGamma = c_float(self.gamma[2])
        # Update gamma ramp.
        result = quartz.CGSetDisplayTransferByFormula(self.display,
            redMin, redMax, redGamma,
            greenMin, greenMax, greenGamma,
            blueMin, blueMax, blueGamma)
        if result != 0:
            raise RuntimeError('Error calling CGSetDisplayTransferByFormula with error code: {0}'.format(result))


rgbTuple = _temp_to_white(1900)
print rgbTuple