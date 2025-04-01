# Todo:
# - add all the buttons support
# - add auto sign out from profile
# - IR control
# - make it one rp pico
# - music feedback


import utime
from machine import Pin, ADC

hack_complete= False

RB_blitz_index= 2

btns_pins= {
    "power": 2,
    "aux": 14,
    "mode": 4,
    "buzzer": 32,
    
    "controller": {
        "xbox": 16,
        
        "a": 23,
        "b": 17,
        "x": None,
        "y": None,
        
        "rb": 21,
        "lb": 13,
        
        "d_r": 22,
        "d_l": 18,
        "d_u": None,
        "d_d": 12,
    }
}

pins= {}

for btn in btns_pins["controller"]:
    if btns_pins["controller"][btn]==None: continue
    pins[btn]= Pin(btns_pins["controller"][btn], Pin.OUT)
    pins[btn].off()

pins["aux"]=  ADC(Pin(btns_pins["aux"]))
pins["buzzer"]=  Pin(btns_pins["buzzer"], Pin.OUT)
pins["power"]=  Pin(btns_pins["power"], Pin.OUT)

pins["power"].on()

_count= range(10)


def toggle_power():
    press("power", 70, invert= True)

def complete_hack():
    global hack_complete
    press("buzzer", 5000)
    hack_complete= True

def press(btn, timeout= 50, invert= False):
    """
    btn: a key from the dict 'pins'.
    timeout: holding time for the btn.
    """
    global pins
    
    if not invert:
        pins[btn].on()
        utime.sleep_ms(timeout)
        pins[btn].off()
    else:
        pins[btn].off()
        utime.sleep_ms(timeout)
        pins[btn].on()
    


def sound_detected():
    avg= 0
    
    for i in _count:
        avg= avg + round(pins["aux"].read_u16()/65535, 4)
        utime.sleep_ms(50)
    
    avg= avg/10
        
    if (avg * 10000) > 10:
        return True
    else:
        return False


def check_sound(freq= 6):
    a= 0
    for i in range(freq):
        press("xbox")
        utime.sleep_ms(40)
        a= a+int(sound_detected())
        print(a)
        utime.sleep_ms(1500)
    
    a= a/freq
    
    return (a>0.45)


def start_game():
    pins["buzzer"].on()
    utime.sleep(1)
    pins["buzzer"].off()

    press("xbox")
    utime.sleep_ms(2000)
    press("lb")
    utime.sleep_ms(1000)

    for i in range(3):
        press("d_d")
        utime.sleep_ms(800)

    press("a")

    utime.sleep_ms(2000)
    
    for i in range(RB_blitz_index-1):
        press("d_r")
        utime.sleep_ms(800)

    press("a")
    
    utime.sleep(35)
    
    press("a")


def confirm_hang(reboot= True):
    
    
    for i in range(15):
        
        press("buzzer", 100)
        
        if sound_detected(): return
        
        utime.sleep(1)
    
    # to close freemyxe dialogs    
    press("a")
    utime.sleep(3)
    press("a")
    utime.sleep(10) # let it get to the home screen (if the hack was completed else all key inputs will be ignored by xbox)
    if check_sound():
        complete_hack()
        return
    else:
        press("buzzer", 500)
        utime.sleep(0.5)
        press("buzzer", 500)
        utime.sleep(0.5)
        press("buzzer", 500)
        toggle_power()
        utime.sleep(10)
        toggle_power()
        utime.sleep(30)
        start_game()
        return



toggle_power()

utime.sleep(30)


start_game()


while not hack_complete:
    if not sound_detected():
        confirm_hang()
    
    utime.sleep(5)



