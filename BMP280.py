import machine
import ubinascii
import webrepl
from umqtt.simple import MQTTClient
from time import sleep
import BME280
from machine import Pin, SoftI2C

i2c=SoftI2C(scl=Pin(4), sda=Pin(5))

bme = BME280.BME280(i2c=i2c,address=119)


mqtt_server ='10.6.0.26'


topic_sub ='TEST2'


port      =1883



topic_pub ='team_1'

client_id ="team_1"

counter =0
last_message=0

client = None

def connect():
    import network
 

    ssid = "****" #check
    password =  "***" #check

    print("Start connecting")
       
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        print(station.ifconfig())
        return 1
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    tp=(station.ifconfig())
    print("My IP is ="+tp[0])
 

def mqtt_connect():
  global client_id, mqtt_server, topic_sub
  global client
  client = MQTTClient(client_id, mqtt_server,port)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to: %s MQTT broker, Port: %s' % (mqtt_server,  port))
  print('subscribed to Topic :%s ' % (topic_sub))


def sub_cb():
    print("call back")

def reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def send():

    global client  

    #value = bme.temperature        
   
    while True:
        tem = float(bme.temperature)
        hum = float(bme.humidity)
        p = float(bme.pressure)
       
        msg1 = 'IOTJS={\"S_name\":\"Team1_1_temp\",\"S_value\": %.1f }' % tem    
        msg2 = 'IOTJS={\"S_name\":\"Team1_1_hum\",\"S_value\": %.1f }' % hum        
        msg3 = 'IOTJS={\"S_name\":\"Team1_1_pre\",\"S_value\": %.1f }' % p
           
        client.publish(topic_pub, msg1)
        client.publish(topic_pub, msg2)
        client.publish(topic_pub, msg3)        
        print(msg1,msg2,msg3)
        sleep(0.5)    


print(" WLAN start connecting ")
connect()
print(" MQTT start connecting ")
mqtt_connect()
print(" MQTT start sending message")
send()
print(" Team_1 send")