#!/usr/bin/env python3
# coding: utf-8

################################################################################
# 温湿度センサ SENSIRION SHT30 と QST QMP6988 から温度と湿度、気圧を取得します。
#
#                                               Copyright (c) 2024 Wataru KUNINO
################################################################################

sht31 = 0x44                                        # sht31 = 0x44 又は 0x45
qmp6988_adr = 0x70                                  # qmp6988 = 0x70 又は 0x56

wbgt_ver = 3                                        # WBGTバージョン 3または4
wbgt_wide = True                                    # 筆者の独自拡張Wide版

import smbus
from time import sleep                              # 時間取得を組み込む
import datetime
from lib_qmp6988.piqmp6988 import piqmp6988 as QMP6988  # QMP6988用モジュール

def word2uint(d1,d2):
    i = d1
    i <<= 8
    i += d2
    return i


# SHT30 SHT31 設定
sht31_i2c = smbus.SMBus(1)
sht31_i2c.write_byte_data(sht31,0x30,0x6D)          # Heater ON=0x6D (OFF=0x66)
wind_max_c = 3.00                                   # 強風時の温度低下
wind_max_m = 10                                     # 強風時の風速 m/s

# QMP6988 設定
config = {
    'address' :     qmp6988_adr,
    'temperature' : QMP6988.Oversampling.X4.value,
    'pressure' :    QMP6988.Oversampling.X32.value,
    'filter' :      QMP6988.Filter.COEFFECT_32.value,
    'mode' :        QMP6988.Powermode.NORMAL.value}
qmp6988 = QMP6988.PiQmp6988(config)

while sht31_i2c:
    # 気圧センサ QMP6988 からデータ取得
    value = qmp6988.read()
    temp2 = value.get('temperature')
    press = value.get('pressure')

    # 湿度センサ SHT30 からデータ取得
    temp1 = None
    hum = None
    sht31_i2c.write_byte_data(sht31,0x24,0x00)
    sleep(0.018)
    data = sht31_i2c.read_i2c_block_data(sht31,0x00,6)
    if len(data) >= 5:
        temp1 = float(word2uint(data[0],data[1])) / 65535. * 175. - 45.
        hum  = float(word2uint(data[3],data[4])) / 65535. * 100.
        wind_c = temp1 - temp2
        if wind_c > wind_max_c:
            wind_max_c = wind_c
        wind = (1. - wind_c / wind_max_c) * wind_max_m
        date = datetime.datetime.today()            # 日付を取得
        date = date.strftime('%Y/%m/%d %H:%M')      # 日付を文字列に変更
        print(date + ", ", end='')
        print("Temp. = (%.2f ℃, %.2f ℃), wind = %.3f" % (temp1,temp2,wind))
    sleep(1)

''' ----------------------------------------------------------------------------
参考文献1
  QMP6988 データシート
  https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/datasheet/unit/enviii/QMP6988%20Datasheet.pdf
  QMP6988 デバイスドライバ piqmp6988-1.0.1
  https://pypi.org/project/piqmp6988/

参考文献2
  温湿度センサ SENSIRION SHT31 から温度と湿度を取得します。
  https://github.com/bokunimowakaru/RaspberryPi/blob/master/gpio/raspi_sht31.py
                                                Copyright (c) 2021 Wataru KUNINO
---------------------------------------------------------------------------- '''
