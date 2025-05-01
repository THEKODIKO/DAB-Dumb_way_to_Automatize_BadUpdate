# Todo:
# - test/fix audio
# - Somehow check for xbox power status without photoresistor
# - add support for json config file
# -
# - add auto sign out from profile
# - make it one rp pico
# - music feedback

import os
import json
import time
import array
import board
import pulseio
import analogio
import digitalio


settings= {}


if "config.json" in os.listdir():
    with open("config.json", "r") as file:
        settings= json.load(file)
else:
    with open("config.json", "w") as file:
        settings= {'REBOOT_TIMEOUT': 20, 'RED_LGHT_VAL': [48000, 60000], 'YELLOW_LGHT_VAL': [18000, 30000], 'RBB_INDEX': 2}
        json.dump(settings, file)


def save_settings():
    with open("config.json", "w") as file:
        json.dump(settings, file)
    time.sleep(0.01) # to prevent rapid calling of this func


print(settings)

hack_complete= False


# The on signal for xbox 360 (it uses philips RC6 protocol but we'll just use the raw method)
# these values were empirically found. (watch: https://www.youtube.com/watch?v=TIbp7DzfOBM)
on_signal= array.array('H', [2642, 795, 518, 389, 480, 400, 466, 819, 494, 820, 1386, 793, 491, 349, 516, 388, 482, 400, 466, 374, 466, 400, 466, 400, 490, 404, 466, 399, 467, 373, 465, 387, 928, 451, 468, 372, 467, 386, 482, 400, 461, 371, 528, 398, 493, 348, 464, 843, 892, 821, 462, 390, 532, 400, 465, 375, 466, 401, 465, 401, 911, 375, 517, 796, 516, 403, 464, 65535, 2724, 793, 468, 372, 517, 387, 482, 793, 520, 794, 1357, 840, 499, 375, 466, 374, 516, 386, 483, 400, 438, 394, 501, 373, 519, 348, 491, 384, 484, 400, 466, 374, 910, 389, 533, 400, 466, 374, 464, 835, 925, 389, 530, 349, 514, 772, 940, 846, 466, 374, 465, 401, 913, 400, 517, 795, 490, 395, 918, 789, 471, 387, 534, 65535, 106])

btns_pins= {
    "power": board.GP2, # the IR led connects here!
    "aux": board.A0,
    "pwr_det": board.A1,
    "mode": board.GP6, # should be pulled up
    "buzzer": board.GP3,
    "HD_led": board.GP7, # HD => Hack Done
    
    "controller": {
        "xbox": board.GP22,         # 22
        "start": board.GP11,        # 11
        
        "a": board.GP16,            # 16
        "b": board.GP17,            # 17
        "x": board.GP12,            # 12
        "y": board.GP13,            # 13
        
        "rb": board.GP18,           # 18
        "lb": board.GP19,           # 19
         
        "d_r": board.GP20,          # 20
        "d_l": board.GP21,          # 21
        "d_u": board.GP14,          # 14
        "d_d": board.GP15,          # 15
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

pins["pwr_det"]=  analogio.AnalogIn(board.A1)

pins["buzzer"]= digitalio.DigitalInOut(btns_pins["buzzer"])
pins["buzzer"].direction = digitalio.Direction.OUTPUT


pins["HD_led"]= digitalio.DigitalInOut(btns_pins["HD_led"])
pins["HD_led"].direction = digitalio.Direction.OUTPUT

pins["HD_led"].value= False

pins["power"]= pulseio.PulseOut(btns_pins['power'], frequency=38000, duty_cycle=2**15)

_count= range(10)

total_hangs= 0


AVG_LVL= 0

for i in range(50):
    AVG_LVL+= pins["aux"].value

AVG_LVL= AVG_LVL/50




def toggle_power():
    print("TOGGLING POWER")
    # thanks a lot to adafruit for this code. (https://www.youtube.com/watch?v=TIbp7DzfOBM)
    pins["power"].send(on_signal)
    


def confirm_hacked():
    
    press("b")
    
    time.sleep(10)
    
    no= 0

    for i in (1,2,3,4,5,6):
        time.sleep(.25)
        _= pins["pwr_det"].value

        press("start")
        time.sleep(.25)
        _= _-pins["pwr_det"].value
        
        if abs(_) > 1500: no+=1

    
    return (no/6)>0.5


# setting the yellow led trigger point

def set_pwr_led_level():
    _= pins["pwr_det"].value
    toggle_power()
    time.sleep(5)
    if pins["pwr_det"].value > _:
        _= pins["pwr_det"].value
        
        if (_-5000)<0:
            settings["YELLOW_LGHT_VAL"]= [0, _+5000]
        else:
            settings["YELLOW_LGHT_VAL"]= [_-5000, _+5000]
        
        time.sleep(5)
        toggle_power()
    else:
        time.sleep(5)
        toggle_power()
        set_pwr_led_level()


if settings.get("MEASURE_PWR_LED_LEVEL"):
    set_pwr_led_level()
    save_settings()




def get_led_clr():
    if settings["RED_LGHT_VAL"][0] <= pins["pwr_det"].value <= settings["RED_LGHT_VAL"][1]:
        return "RED"
    elif settings["YELLOW_LGHT_VAL"][0] <= pins["pwr_det"].value <= settings["YELLOW_LGHT_VAL"][1]:
        return "YELLOW"
    else:	return "OFF"



def get_avg_vol(samples= 100):
    _= 0
    
    for _ in range(samples):
        _+= abs(pins["aux"].value-AVG_LVL)
        time.sleep(0.01)
    
    return (_/samples)>1.3





def check_if_hanged():
    print("Checking Sound...")
    # if get_avg_vol() already detects vol then just return false.
    if get_avg_vol(): return False
    
    time.sleep(5)

    press('xbox')

    time.sleep(5)

    press('d_r')

    time.sleep(1)

    for i in range(4):
        press('d_d')

        time.sleep(1)

    press('a')

    time.sleep(1.3)

    press('y')

    time.sleep(10)


    d= not get_avg_vol()
    
    press('d_d')

    time.sleep(1)
    
    for i in range(2):
        press('d_r')
        time.sleep(1)
    
    press('a')

    time.sleep(1)

    press('xbox')
    
    print("SOUND STOPPED:", d)
    
    return d # true -> hanged



def power_on():
    while 1:
        _= pins["pwr_det"].value
        
        toggle_power()
        print("POWER ONING...")
        
        time.sleep(5)
    
        if (pins["pwr_det"].value - _) >= settings.get("PWR_LIGHT_SENSITIVITY", 1000):
            print("POWER ON DONE")
            return True
    
def power_off():
    while 1:
        _= pins["pwr_det"].value
    
        toggle_power()
        print("POWER OFFING...")
        
        time.sleep(5)
        
        if (pins["pwr_det"].value - _) <= -1*settings.get("PWR_LIGHT_SENSITIVITY", 1000):
            print("POWER OFF DONE")
            return True


def complete_hack():
    global hack_complete
    press("buzzer", 5000)
    pins["HD_led"].value= True
    hack_complete= True

def press(btn, timeout= 50, invert= False):
    """
    btn: a key from the dict 'pins'.
    timeout: holding time for the btn.
    invert: if True then the true and false will be reversed.
    """
    global pins
    
    #print("pressing", btn)
    
    if not invert:
        pins[btn].value= True
        sleep_ms(timeout)
        pins[btn].value= False
    else:
        pins[btn].value= False
        sleep_ms(timeout)
        pins[btn].value= True
    

def confirm_hang(attempts):
    a_no= 0
    
    for i in range(attempts):
        a_no+= int(check_if_hanged()) # bool -> int => 1/0
        
        # timeout before another try to prevent key skips or
        # hangs by giving inputs too fast.
        time.sleep(7) 
    
    return (a_no/attempts) >= 0.6 


def start_game():
    press("buzzer", 1000)

    press("xbox")
    time.sleep(5)
    press("lb", 100)
    time.sleep(1)

    for i in range(3):
        press("d_d")
        sleep_ms(800)

    press("a")

    time.sleep(2)
    
    for i in range(settings["RBB_INDEX"]-1):
        press("d_r")
        sleep_ms(800)

    press("a")
    
    time.sleep(35)
    
    press("a")



def reboot():
    print("Rebooting...")
                
    press("buzzer", 500)
    sleep_ms(500)
    press("buzzer", 500)
    sleep_ms(500)
    press("buzzer", 500)
    power_off()
    time.sleep(12)
    power_on()
    time.sleep(30)
    start_game()



def main():
    global hack_complete
    
    power_on()
    time.sleep(30)
    start_game()

    bef_time= time.time()
    last_sound_check= 0
    last_hack_check= 0

    while not hack_complete:
        
        if ((time.time() - bef_time)/60) > settings["REBOOT_TIMEOUT"]:
            bef_time= time.time()
            #reboot()
            print("20 mins done!!!")

        
        elif (time.time() > last_sound_check):
            print(time.time(), last_sound_check)
            last_sound_check= time.time() + 60 # check after 30 secs
            
            if check_if_hanged():
                
                print("No sound!")
                _= 0
                time.sleep(1)
                _+= bool(check_if_hanged())
                time.sleep(1)
                _+= bool(check_if_hanged())
                time.sleep(1)
                _+= bool(check_if_hanged())
                
                if (_/3)>0.5:
                    reboot()
                else:
                    print("rebooting avoided!")
        
        if (time.time() > last_hack_check):
            last_hack_check= time.time() + 30
            
            if confirm_hacked():
                hack_complete= True
                press("buzzer", 5000)
                print("HACK DONE!!!")
            
            
        
        time.sleep(0.1)




# Running the setup!
main()





