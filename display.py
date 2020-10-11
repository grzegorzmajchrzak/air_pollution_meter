#!/usr/bin/python3

import time
import traceback

from PIL import Image, ImageDraw, ImageFont

from lib import epd2in13, airly

WHITE = 255
BLACK = 0


def draw_data(draw, pm25, label, y, factor=1.0):
    small = int(18 * factor)
    big = int(64 * factor)
    fontBig = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', big)
    fontSmall = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', small)
    draw.text((0, y), label, font=fontSmall, fill=BLACK)
    draw.text((0, y + small), pm25, font=fontBig, fill=BLACK)
    draw.text((5 + len(pm25) * big / 2, y + big), '%', font=fontSmall, fill=BLACK)


def draw_in_line(draw, label, y, font_size):
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', font_size)
    draw.text((0, y), label, font=font, fill=BLACK)


def draw_footer(draw):
    font12 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 12)
    draw.text((10, epd2in13.EPD_HEIGHT - 24), time.strftime('%Y.%m.%d %H:%M'), font=font12, fill=BLACK)


def draw_aqi(inside, outside, luczyce):
    epd = epd2in13.EPD()
    epd.init(epd.FULL_UPDATE)

    image = Image.new('1', (epd2in13.EPD_WIDTH, epd2in13.EPD_HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)
    draw_data(draw, inside, 'INSIDE', 0)
    draw.line([(0, 90), (epd2in13.EPD_WIDTH, 90)], fill=BLACK, width=1)
    draw_data(draw, outside, 'OUTSIDE', 95)
    draw_footer(draw)
    draw.line([(0, 180), (epd2in13.EPD_WIDTH, 180)], fill=BLACK, width=1)

    draw_in_line(draw, 'Łuczyce: {}% '.format(luczyce), 185, 14)

    epd.displayPartial(epd.getbuffer(image))


#    MAIN      #
try:
    max_inside = airly.get_pollution_local()
    max_outside = airly.get_pollution_slomczynskiego()
    max_luczyce = airly.get_pollution_luczyce()

    draw_aqi(str(max_inside), str(max_outside), str(max_luczyce))
except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()
