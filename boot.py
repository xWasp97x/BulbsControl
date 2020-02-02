import esp
import wifi_manager
from updater import Updater
from machine import Timer
from time import sleep
esp.osdebug(None)


wifi = wifi_manager.WifiManager('/config/wifi.txt', '/config/networks.txt')
wifi_timer = Timer(-1)
wifi_timer.init(period=wifi.check_delay*1000, mode=Timer.PERIODIC, callback=lambda t: wifi.check_connection())

updater = Updater('/config/updater.txt')
updater_timer = Timer(-1)
updater_timer.init(period=updater.check_delay*1000, mode=Timer.PERIODIC, callback=lambda t: updater.fetch_update())
