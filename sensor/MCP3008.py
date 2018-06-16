from RPi import GPIO
from spidev import SpiDev
import time


# # 3) Testapplicatie
# def read_trimmer(device=0):
#     """Read a value from CH0 on MCP3008 slave <device> and print it to console.
#     :param device: SPI slave (SS/CE/CS: 0 or 1 for standard RPi 3)
#     """
#     spi = SpiDev()
#     spi.open(0, 0)
#     spi.max_speed_hz = 100000
#     cb = [0x01, 0x80, 0x00]
#     bytes_in = spi.xfer2(cb)
#     B9B8 = (bytes_in[1] & 0x03) << 8
#     byte = B9B8 | bytes_in[2]
#     return byte


# 4) Converting values
def value_to_volts(value):
    """Convert a 10-bit measurement to an analog voltage
    :param value: ADC measurement (0-1023)
    :return: Analog voltage (0 - 3.3)
    """
    returnValue = value / 1023 * 3.3

    return returnValue


def value_to_percent(value):
    """Convert a 10-bit measurement to a percentage
    :param value: ADC measurement (0-1023)
    :return: Percentage with 1 decimal (0.0 - 100.0)
    """
    returnValue = value / 1023 * 100.0

    return round(returnValue, 1)


def value_to_kmh(value):
    returnValue = (value / 1023 * 3.3 - 0.4) / \
        0.0171467764060357 - 1.12
    return returnValue

# 5) Class for the ADC


class MCP3008:
    """Class representing an MCP3008 ADC"""

    def __init__(self, bus=0, device=0):
        """
        Initialize SPI device for MCP3008
        :param bus: SPI bus (usually 0)
        :param device: SPI slave (SS/CS/CE)
        """
        self.spi = SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 100000

    def read_channel(self, ch):
        """
        Perform measurement on an ADC channel
        :param ch: ADC channel (0-7)
        :return: 10-bit integer measurement (0-1023)
        """

        digit = int("1" + bin(ch)[2:] + "0000")
        cb = [0x01, digit, 0x00]
        for i in range(len(cb)):
            print(cb)
        bytes_in = self.spi.xfer2(cb)
        B9B8 = (bytes_in[1] & 0x03) << 8
        byte = B9B8 | bytes_in[2]
        return byte


# def main():
#     GPIO.setmode(GPIO.BCM)
#     try:
#         while True:
#             mcp = MCP3008()
#             print(mcp.read_channel(0))
#             time.sleep(0.5)
#             print(value_to_volts(mcp.read_channel(0)))
#         # print(read_trimmer())

#     except KeyboardInterrupt:
#         pass
#     finally:
#         # get rid of warning when no GPIO pins set up
#         GPIO.setwarnings(False)
#         GPIO.cleanup()


if __name__ == '__main__':
    main()
