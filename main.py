import network, time, urequests
from machine import Pin, ADC
from utime import sleep, sleep_ms
from dht import DHT22

sensor_dht = DHT22(Pin(12))
ldr_pin = ADC(Pin(33))
lluvia_pin = ADC(Pin(32))
higo_pin = ADC(Pin(35))
co2_pin = ADC(Pin(34))
asc712_pin = ADC(Pin(39))


sensibilidad = 0.185  # Puede variar según el modelo del sensor Corriente


def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True


if conectaWifi ("Wokwi-GUEST", ""):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    
    url="https://api.thingspeak.com/update?api_key=A4WJWKP0P4K8G9RH"
    # ir a la siguiente URL para la visualización  https://thingspeak.com/channels/2171544
    while True:

        sensor_dht.measure()
        tem = sensor_dht.temperature()
        hum = sensor_dht.humidity()

        ldr_value = ldr_pin.read()    
        light = (ldr_value / 4095) * 100

        lluvia_value = lluvia_pin.read()    
        lluvia= (lluvia_value / 4095) * 100
        
        higo_value = higo_pin.read()    
        higo= (higo_value / 4095) * 100

        co2_value = co2_pin.read()    
        co2= (co2_value / 4095) * 100
        
        asc712_value = asc712_pin.read()
        voltaje = (asc712_value/ 1023) * 3.3 
        corriente = (voltaje - 2.5)/sensibilidad
        i=corriente -3
        v=voltaje + 8.5
        
        print("Tem:{:.2f}°c, Hum:{:.2f}% Luz:{:.2f}% Lluvia:{:.2f}% Higo:{:.2f}% Co2:{:.2f}%, I:{:.2f}A V:{:.2f}v" .format(tem, hum,light, lluvia,  higo, co2,i,v ))
        
        respuesta = urequests.get(url+"&field1="+str(tem)+"&field2="+str(hum)+"&field3="+str(light)+"&field4="
                                  +str(lluvia)+"&field5="+str(higo) +"&field6="+str(co2)+"&field7="+str(i)+"&field8="+str(v))
        print(respuesta.text)
        print(respuesta.status_code)
        respuesta.close ()
        time.sleep(4)

 
else:
       print ("Imposible conectar")
       miRed.active (False)

