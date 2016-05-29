#! /usr/bin/python  
  
import paho.mqtt.client as mqtt  
import time  
import signal

# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = 'YOUR AIO KEY'
ADAFRUIT_IO_USERNAME = 'YOUR ADAFRUIT USERNAME'     # See https://accounts.adafruit.com
                                                    # to find your username.  
#Global Stuff  
running = True
mcount = 0
# The callback for when the client receives a CONNACK response from the server.  
def on_connect(client, userdata, flags, rc):  
    print("Connected with result code "+str(rc))  
    # Subscribing in on_connect() means that if we lose the connection and  
    # reconnect then subscriptions will be renewed.  
    #client.subscribe("<ADAFRUIT IO USERNAME>/feeds/<feedname>")  
  
# The callback for when a PUBLISH message is received from the server.  
def on_message(client, userdata, msg): 
    global mcount
    mcount += 1
    print mcount, 
    print(msg.topic+": "+str(msg.payload))  

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
	
def sigterm_handler(_signo, _stack_frame):
    global running
    running = False  

print("init signal handler")
signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)
	
client = mqtt.Client()  
client.on_connect = on_connect  
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)  
client.tls_set("adafruit CA certificate keychain file")  
client.connect("io.adafruit.com", 8883, 60)  
  
#Start Loop  
client.loop_start()  
  
try:  
     while running:   
          print 'Doing Something Here'  
          client.publish("<ADAFRUIT IO USERNAME>/feeds/<feedname>", 12)  # we publish a integer value
          print 'Sleeping again'  
          time.sleep(30)  
except:  
     print 'an error occured'  
finally:  
     print 'All Clean up Now'  
     client.loop_stop()
     client.disconnect()	   
