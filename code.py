# Todo:
# - test/fix audio
# - Add support photoresistive sensor to check xbox power status.
# - make json editor
# - 
# - add auto sign out from profile
# - make it one rp pico
# - music feedback


import time
import array
import board
import pulseio
import analogio
import digitalio
# from machine import Pin, ADC

hack_complete= False

RB_blitz_index= 2

# The on signal for xbox 360 (it uses philips RC6 protocol but we'll just use the raw method)
# these values were empirically found. (watch: https://www.youtube.com/watch?v=TIbp7DzfOBM)
on_signal= array.array('H', [2642, 795, 518, 389, 480, 400, 466, 819, 494, 820, 1386, 793, 491, 349, 516, 388, 482, 400, 466, 374, 466, 400, 466, 400, 490, 404, 466, 399, 467, 373, 465, 387, 928, 451, 468, 372, 467, 386, 482, 400, 461, 371, 528, 398, 493, 348, 464, 843, 892, 821, 462, 390, 532, 400, 465, 375, 466, 401, 465, 401, 911, 375, 517, 796, 516, 403, 464, 65535, 2724, 793, 468, 372, 517, 387, 482, 793, 520, 794, 1357, 840, 499, 375, 466, 374, 516, 386, 483, 400, 438, 394, 501, 373, 519, 348, 491, 384, 484, 400, 466, 374, 910, 389, 533, 400, 466, 374, 464, 835, 925, 389, 530, 349, 514, 772, 940, 846, 466, 374, 465, 401, 913, 400, 517, 795, 490, 395, 918, 789, 471, 387, 534, 65535, 106])

btns_pins= {
    "power": board.GP2, # the IR led connects here!
    "aux": board.A0,
    "mode": board.GP6, # should be pulled up
    "buzzer": board.GP3,
    
    "controller": {
        "xbox": board.GP22, # 22
        
        "a": board.GP16, # 16
        "b": board.GP17, # 17
        "x": board.GP12, # 12
        "y": board.GP13, # 13
        
        "rb": board.GP18, # 18
        "lb": board.GP19, # 19
         
        "d_r": board.GP20, # 20
        "d_l": board.GP21, # 21
        "d_u": board.GP14, # 14
        "d_d": board.GP15, # 15
    }
}

pins= {}




def sleep_ms(timeout):
    time.sleep(timeout/1000)




for btn in btns_pins["controller"]:
    
    if btns_pins["controller"][btn]==None: continue # if the pin is not connected/defined then skip
    
    pins[btn]= digitalio.DigitalInOut(btns_pins["controller"][btn])
    pins[btn].direction = digitalio.Direction.OUTPUT
    pins[btn].value= False



pins["aux"]=  analogio.AnalogIn(board.A0)

pins["buzzer"]= digitalio.DigitalInOut(btns_pins["buzzer"])
pins["buzzer"].direction = digitalio.Direction.OUTPUT

pins["power"]= pulseio.PulseOut(btns_pins['power'], frequency=38000, duty_cycle=2**15)

_count= range(10)


def toggle_power():
    # thanks a lot to adafruit for this code. (https://www.youtube.com/watch?v=TIbp7DzfOBM)
    pins["power"].send(on_signal)

def complete_hack():
    global hack_complete
    press("buzzer", 5000)
    hack_complete= True

def press(btn, timeout= 50, invert= False):
    """
    btn: a key from the dict 'pins'.
    timeout: holding time for the btn.
    invert: if True then the true and false will be reversed.
    """
    global pins
    
    if not invert:
        pins[btn].value= True
        sleep_ms(timeout)
        pins[btn].value= False
    else:
        pins[btn].value= False
        sleep_ms(timeout)
        pins[btn].value= True
    


def sound_detected():
    avg= 0
    
    for i in _count:
        avg= avg + round(pins["aux"].value/65535, 4)
        sleep_ms(50)
    
    avg= avg/10
        
    if (avg * 10000) > 10:
        return True
    else:
        return False


def check_sound(freq= 6):
    a= 0
    for i in range(freq):
        press("xbox")
        sleep_ms(40) 
        a= a+int(sound_detected())
        print(a)
        time.sleep(1.5) # secs
    
    a= a/freq
    
    return (a>0.45)


def start_game():
    press("buzzer", 1000)

    press("xbox")
    time.sleep(2)
    press("lb")
    time.sleep(1)

    for i in range(3):
        press("d_d")
        sleep_ms(800)

    press("a")

    time.sleep(2)
    
    for i in range(RB_blitz_index-1):
        press("d_r")
        sleep_ms(800)

    press("a")
    
    time.sleep(35)
    
    press("a")


def confirm_hang(reboot= True):
    
    
    for _ in range(15):
        
        press("buzzer", 100)
        
        if sound_detected(): return
        
        time.sleep(1)
    
    # to close freemyxe dialogs    
    press("a")
    time.sleep(3)
    press("a")
    time.sleep(10) # let it get to the home screen (if the hack was completed else all key inputs will be ignored by xbox)
    if check_sound():
        complete_hack()
        return
    else:
        press("buzzer", 500)
        sleep_ms(500)
        press("buzzer", 500)
        sleep_ms(500)
        press("buzzer", 500)
        toggle_power()
        time.sleep(10)
        toggle_power()
        time.sleep(30)
        start_game()
        return




def main():
    toggle_power()

    time.sleep(30)


    start_game()


    while not hack_complete:
        if not sound_detected():
            confirm_hang()
        
        time.sleep(5)



# Running the setup!
main() 
