# -*- coding: utf-8 -*-
from PIL import Image
from campaigns.foundation.const import FoundationConst


def prepare_image_list(kit_filename_list, root_path=None):
    if root_path is not None:
        kit_filename_list = [root_path + kit_filename for kit_filename in kit_filename_list]
    return [Image.open(kit_filename).convert(FoundationConst.RN_RGBA) for kit_filename in kit_filename_list]


def add_kit_to_canvas(canvas, kit, x, y, scale, angle):
    if scale != 1:
        width = kit.width
        height = kit.height
        kit = kit.resize((int(width * scale), int(height * scale)), resample=Image.BILINEAR)
    if angle != 0:
        angle = 360 - angle
        kit = kit.rotate(angle, resample=Image.BILINEAR, expand=True)
    mask = Image.merge("L", (kit.split()[3], ))
    canvas.paste(kit, (x, y), mask)


def regenerate_image_by_feature_list(feature_list, raw_width, raw_height, source_image_list, des_width, des_height):
    canvas = Image.new(FoundationConst.RN_RGBA, (des_width, des_height), (0, 0, 0, 0))
    for feature in feature_list:
        index = int(feature[FoundationConst.RN_INDEX])
        x = int(float(feature[FoundationConst.RN_X]) / float(raw_width) * des_width)
        y = int(float(feature[FoundationConst.RN_Y]) / float(raw_height) * des_height)
        scale = float(feature[FoundationConst.RN_SCALE])
        angle = float(feature[FoundationConst.RN_ANGLE])
        add_kit_to_canvas(canvas, source_image_list[index], x, y, scale, angle)
    return canvas

