import sensor, image, time, math, pyb
from pyb import Pin
uart = pyb.uart(1 , 9600)

#-------defining Leds for indication-------#
red_led     = pyb.LED(1)
green_led   = pyb.LED(2)
blue_led    = pyb.LED(3)


#-------defining thresholds for each color-------#
red_thresholds      = [(0, 100, 12, 127, 3, 30)]
green_thresholds    = [(0, 100, -128, -30, -20, 50)]
yellow_thresholds   = [(20, 90, -20, 26, 55, 75)]
black_thresholds    = [(0, 17, -20, 20, -20, 20)]

grayscale_threshold = [(0,60)] #To detect black color in grayscale mode

#-------getting templates for letter detection-------#
templateH   = image.Image("/h.pgm")
templateH2  = image.Image("/h2.pgm")
templateH3  = image.Image("/h3.pgm")
templateH4  = image.Image("/h4.pgm")
templateS   = image.Image("/s.pgm")
templateS2  = image.Image("/s2.pgm")
templateS3  = image.Image("/s3.pgm")
templateU   = image.Image("/U.pgm")
templateU2  = image.Image("/U2.pgm")
templateU3  = image.Image("/u3.pgm")
templateU4  = image.Image("/u4.pgm")
templateU5  = image.Image("/u5.pgm")

#-------setting pins for communication with arduino-------#
p0 = Pin('P6', Pin.OUT_PP) #in case of U or Green to stop the robot for 5s
p1 = Pin('P7', Pin.OUT_PP) #in case of Red or Yellow to drop 1 rk
p2 = Pin('P8', Pin.OUT_PP) #in case of S to drop 2 rks
# p3 =  3 #in case of H to drop 3 rks

#-------setting all variables to starting values-------#
led_color = str()

red_led.off()
green_led.off()
blue_led.off()

red     = False
green   = False
yellow  = False
black = False

letters = False
color = True

start_time = 0 #in case the robot sees black tile and needs to reset the sensor back to RGB
current_time = 0
elapsed_time = 0

rescue_kits_num = 0  #(H = 3rk; S = 2rk, U = 0rk)
                     #(R = 1rk; Y = 1rk; G = 0rk)
victim_counter  = 0                               #There are 4 states for VC (Victim_Counter):
                                                     ##VC = 0 which means that we're
#-------defining functions-------#                    #ready to detect a victim.
def sg():  #set sensor to Grayscale                  ##VC = 1 which means that a victim
    sensor.reset()                                    #was just detected and now we deploy
    sensor.set_pixformat(sensor.GRAYSCALE)            #rescue kits.
    sensor.set_framesize(sensor.QQQVGA)              ##VC = -1 which means that we didn't move
    sensor.skip_frames(time = 1000)                   #on from the current victim yet, so that
    sensor.set_auto_gain(False)                       #we don't detect the same victim twice.
    sensor.set_auto_whitebal(False)                  ##VC = 2 which is a transitional state
                                                      #between (-1) and (0).
def sc(): #set sensor to Color
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QQVGA)
    sensor.skip_frames(time = 1000)
    sensor.set_auto_gain(False)
    sensor.set_auto_whitebal(False)

def signal(pin_num): #singal to the arduino and then turn off
    p0.high()
    time.sleep(0.25)
    p0.low()

    if pin_num != 'p0':
        pin_num.high()
        time.sleep(0.25)
        pin_num.low()

def serial_send(n):
    uart.write(n)

def led_indicate(led_color): #to blink the led indication

    led_start_time = time.ticks_ms()
    print("indication started")
    print("start time: ", led_start_time)

    while (True):
        print("first loop entered")
        led_current_time = time.ticks_ms()
        led_elapsed_time = time.ticks_diff(led_current_time, led_start_time)

        if led_elapsed_time <= 5000:
            print('led time:', led_elapsed_time)

            if led_color == 'R':
                red_led.on()
                print("on")
                time.sleep(0.2)
                red_led.off()
                print("off")
                time.sleep(0.1)
            elif led_color == 'G':
                green_led.on()
                time.sleep(0.2)
                green_led.off()
                time.sleep(0.1)
            elif led_color == 'Y':
                red_led.on()
                green_led.on()
                time.sleep(0.2)
                red_led.off()
                green_led.off()
                time.sleep(0.1)
        else:
            break

def led_off():
    red_led.off()
    green_led.off()
    blue_led.off()


                                            #_______________START_______________#

#-------color detection until there's black-------#
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

while (True):
    clock.tick()
    print("lol")
    while (color == True):
        img = sensor.snapshot()

        for blob in img.find_blobs(red_thresholds, pixels_threshold=200, area_threshold=1000):
            red = True
            green = False
            yellow = False
            black = False

            if victim_counter == 0:
                victim_counter = 1

            img.draw_rectangle(blob.rect(), color=(255,0,0))

        for blob in img.find_blobs(green_thresholds, pixels_threshold=200, area_threshold=1000):
            red = False
            green = True
            yellow = False
            black = False

            if victim_counter == 0:
                victim_counter = 1

            img.draw_rectangle(blob.rect(), color=(0,255,0))

        for blob in img.find_blobs(yellow_thresholds, pixels_threshold=200, area_threshold=1000):
            red = False
            green = False
            yellow = True
            black = False

            if victim_counter == 0:
                victim_counter = 1

            img.draw_rectangle(blob.rect(), color=(255,255,0))

        #-------Indicating colors and deploying rescue kits-------#
        if victim_counter == 1:
            if red and blob.rect()[0] > 30 and blob.rect()[0] < 100:
                print("red")
                led_off()

                rescue_kits_num = 1
                signal(p2)

                led_indicate("R")
                led_off()

                victim_counter  = -1

            elif green and blob.rect()[0] > 30 and blob.rect()[0] < 100:
                print("green")
                led_off()

                rescue_kits_num = 0
                signal(p0)

                led_indicate("G")
                led_off()

                victim_counter  = -1

            elif yellow and blob.rect()[0] > 30 and blob.rect()[0] < 100:
                print("yellow")
                led_off()

                rescue_kits_num = 1
                signal(p1)

                led_indicate("Y")
                led_off()

                victim_counter  = -1

        elif victim_counter == -1:
            led_off()

            if not red and not yellow and not green:
                victim_counter = 2
                print("vc = 2")
            else:
                red = False
                green = False
                yellow = False
                print("still detecting")

        elif victim_counter == 2:
            led_off()
            victim_counter = 0


        #-------Detecting black color to change color mode-------#
        for blob in img.find_blobs(black_thresholds, pixels_threshold=200, area_threshold=1000):
            if victim_counter == 0:
                red = False
                green = False
                yellow = False

                if victim_counter == 0:
                    victim_counter = 1

                sg()

                black = True
                letters = True
                color = False

                start_time = time.ticks_ms()
                break


    #___________________________________________________________

    #-------Letter detection until rescue kit is deployed-------#

    while (letters == True):
        img = sensor.snapshot()

        current_time = time.ticks_ms()
        elapsed_time = time.ticks_diff(current_time, start_time)

        MatchH = img.find_template(templateH, 0.75, search=image.SEARCH_EX)
        MatchH2 = img.find_template(templateH2, 0.75, search=image.SEARCH_EX)
        MatchH3 = img.find_template(templateH3, 0.75, search=image.SEARCH_EX)

        MatchS = img.find_template(templateS, 0.6, search=image.SEARCH_EX)
        MatchS2 = img.find_template(templateS2, 0.6, search=image.SEARCH_EX)
        MatchS3 = img.find_template(templateS3, 0.6, search=image.SEARCH_EX)

        MatchU = img.find_template(templateU, 0.7, search=image.SEARCH_EX)
        MatchU2 = img.find_template(templateU, 0.7, search=image.SEARCH_EX)
        MatchU3 = img.find_template(templateU2, 0.7, search=image.SEARCH_EX)
        MatchU4 = img.find_template(templateU3, 0.7, search=image.SEARCH_EX)      
        MatchU5 = img.find_template(templateU4, 0.7, search=image.SEARCH_EX)


        if victim_counter == 1:

            if MatchH or MatchH2 or MatchH3:
                led_off()

                rescue_kits_num = 3
                signal(p2)

                led_indicate("R")
                led_off()

                print("H")

                if MatchH:
                    img.draw_rectangle(MatchH)
                elif MatchH2:
                    img.draw_rectangle(MatchH2)
                elif MatchH3:
                    img.draw_rectangle(MatchH3)

                victim_counter = -1
                print("vc = ", victim_counter)

            elif MatchS or MatchS2 or MatchS3:
                led_off()

                rescue_kits_num = 2
                signal(p1)

                led_indicate("Y")
                led_off()

                print("S")

                if MatchS:
                    img.draw_rectangle(MatchS)
                elif MatchS2:
                    img.draw_rectangle(MatchS2)
                elif MatchS3:
                    img.draw_rectangle(MatchS3)


                victim_counter = -1
                print("vc = ", victim_counter)

            elif MatchU or MatchU2 or MatchU3 or MatchU4 or MatchU5:
                led_off()

                rescue_kits_num = 0
                signal(p0)

                led_indicate("G")
                led_off()

                print("U")

                if MatchU:
                    img.draw_rectangle(MatchU)
                elif MatchU2:
                    img.draw_rectangle(MatchU2)
                elif MatchU3:
                    img.draw_rectangle(MatchU3)
                elif MatchU4:
                    img.draw_rectangle(MatchU)
                elif MatchU5:
                    img.draw_rectangle(MatchU)


                victim_counter = -1
                print("vc = ", victim_counter)

            else:                        #in order to revert back to RGB if detected black color was the tile
                if elapsed_time >= 5000:
                    led_off()

                    print("stop")



                    victim_counter = 2

                else:
                    print("time check started")
                    print("time = ", elapsed_time)

                    red_led.off()
                    green_led.on()
                    blue_led.on()

        elif victim_counter == -1:
            for blob in img.find_blobs(grayscale_threshold, pixels_threshold=200, area_threshold=1000):
                black = True

            if black == False:
                led_off()

                victim_counter = 2
            else:
                black = False

        elif victim_counter == 2:
            sc()
            color = True
            letters = False

            victim_counter = 0
            break


