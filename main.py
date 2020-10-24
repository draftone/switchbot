from bluepy import btle
from switchbot import SwitchbotScanDelegate

scanner = btle.Scanner().withDelegate(SwitchbotScanDelegate())

devices = scanner.scan(5.0)
for device in devices:
    print('address : %s' % device.addr)

print(scanner.delegate.sensorValue['temperature'])
