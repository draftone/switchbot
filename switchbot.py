import binascii
from bluepy.btle import Scanner, DefaultDelegate

macaddr_l = ['fd:8d:5f:1c:f5:c6', 'aa']

class ScanDelegate( DefaultDelegate ):
    def __init__( self ):
        DefaultDelegate.__init__( self )
        self.sensorValue = None

    def handleDiscovery( self, dev, isNewDev, isNewData ):
        for mac in macaddr_l:
            if dev.addr == mac:
                for ( adtype, desc, value ) in dev.getScanData():
                    if ( adtype == 22 ):
                        print('address : %s' % dev.addr)
                        servicedata = binascii.unhexlify( value[4:] )

                        battery = servicedata[2] & 0b01111111
                        isTemperatureAboveFreezing = servicedata[4] & 0b10000000
                        temperature = ( servicedata[3] & 0b00001111 ) / 10 + ( servicedata[4] & 0b01111111 )
                        if not isTemperatureAboveFreezing:
                            temperature = -temperature
                        humidity = servicedata[5] & 0b01111111

                        isEncrypted            = ( servicedata[0] & 0b10000000 ) >> 7
                        isDualStateMode        = ( servicedata[1] & 0b10000000 ) >> 7
                        isStatusOff            = ( servicedata[1] & 0b01000000 ) >> 6
                        isTemperatureHighAlert = ( servicedata[3] & 0b10000000 ) >> 7
                        isTemperatureLowAlert  = ( servicedata[3] & 0b01000000 ) >> 6
                        isHumidityHighAlert    = ( servicedata[3] & 0b00100000 ) >> 5
                        isHumidityLowAlert     = ( servicedata[3] & 0b00010000 ) >> 4
                        isTemperatureUnitF     = ( servicedata[5] & 0b10000000 ) >> 7
                        self.sensorValue = {
                            'battery:': battery
                        }

                        print( '----' )
                        print( 'battery: '     + str( battery ) )
                        print( 'temperature: ' + str( temperature ) )
                        print( 'humidity: '    + str( humidity ) )
                        print( '' )
                        print( 'isEncrypted: '            + str( bool( isEncrypted ) ) )
                        print( 'isDualStateMode: '        + str( bool( isDualStateMode ) ) )
                        print( 'isStatusOff: '            + str( bool( isStatusOff ) ) )
                        print( 'isTemperatureHighAlert: ' + str( bool( isTemperatureHighAlert ) ) )
                        print( 'isTemperatureLowAlert: '  + str( bool( isTemperatureLowAlert ) ) )
                        print( 'isHumidityHighAlert: '    + str( bool( isHumidityHighAlert ) ) )
                        print( 'isHumidityLowAlert: '     + str( bool( isHumidityLowAlert ) ) )
                        print( 'isTemperatureUnitF: '     + str( bool( isTemperatureUnitF ) ) )
                        print( '----' )

scanner = Scanner().withDelegate( ScanDelegate() )
devices = scanner.scan( 5.0 )

for device in devices:
    print('address : %s' %device.addr)
    print('connectable : %s' %device.connectable)
    print('battery : %s' % device.sensorValue['battery'])
