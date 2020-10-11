#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import traceback

from PIL import Image, ImageDraw, ImageFont

from lib import epd2in13, airly

WHITE = 255
BLACK = 0


def draw_data(draw, pm25, label, x, factor=1.0):
    small = int(18 * factor)
    big = int(64 * factor)
    fontBig = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', big)
    fontSmall = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', small)
    draw.text((x, 0), label, font=fontSmall, fill=BLACK)
    draw.text((x, small), pm25, font=fontBig, fill=BLACK)


def draw_in_line(draw, label, y, font_size):
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', font_size)
    draw.text((0, y), label, font=font, fill=BLACK)


def draw_footer(draw):
    font12 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 16)
    draw.text((10, epd2in13.EPD_WIDTH - 20), time.strftime('%Y.%m.%d %H:%M'), font=font12, fill=BLACK)


def draw_aqi(inside, outside):
    epd = epd2in13.EPD()
    epd.init(epd.FULL_UPDATE)

    image = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), WHITE)
    draw = ImageDraw.Draw(image)
    draw_data(draw, inside, 'INSIDE [%]', 0, 1.2)

    draw_data(draw, outside, 'OUTSIDE [%]', 120, 1.2)
    draw_footer(draw)
    # draw.line([(0, 180), (epd2in13.EPD_WIDTH, 180)], fill=BLACK, width=1)

    epd.displayPartial(epd.getbuffer(image))


#    MAIN      #
try:
    max_inside = airly.get_pollution_local()
    max_outside = airly.get_pollution_slomczynskiego()

    draw_aqi(str(max_inside), str(max_outside))
except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()
