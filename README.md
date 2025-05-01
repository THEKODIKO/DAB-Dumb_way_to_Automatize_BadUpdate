# DAB V0 - A Dumb way to Automatize Bad update exploit. 

![DAB](https://github.com/THEKODIKO/DAB-Dumb_way_to_Automatize_BadUpdate/blob/2bcbe75b81156ed0d29ba17e6454188d1008a259/assets/DAB_mascot.png "DAB")

**Summary**: Have you ever felt that you have too much time to sit down in front of a screen and turn on your Xbox 360, run the rock band blitz game, only to realize it crashed then you do it again till only your skeleton is left ☠️? If your ans is no, then hey! I feel the same. Hence I created this repo to automate all that!

### Features:
- Runs automatically upon xbox's power on.
- It gives audio feedback, so you know at what stage the exploit is.
- It keep trying until it succeeds.
- Plays a tone upon success and enjoy! (in progress)
- No need to even connect to any screen (video output) while the system is trying to run the exploit. (headless)


## Items Required : 

 1. Raspberry pi pico (2 pcs.) [for ref. https://www.digikey.com/en/products/detail/raspberry-pi/SC0915/13624793]
 2. IR Transmitter (1 pcs.) [for ref. https://www.digikey.com/en/products/detail/everlight-electronics-co-ltd/IR333-A/2675571]
 3. Some wires 
 4. 220uf Electrolytic Capacitors  (2 pcs.) [for ref. https://www.digikey.com/en/products/detail/rubycon/25YXJ220M6-3X11/3563124]
 5. 3.5 mm Audio Jack (aux port) breakout board (1 pcs.) [for ref. https://www.digikey.in/en/products/detail/kycon-inc/STX-3000/9975995]
 6. Buzzer
 7. Push Button
 8. LDR sensor (Dark resistance: 1-20 Mohm).
 9. 3.3K ohm resistor.
 10. Green LED. (will be used in future versions for signifying hack done)
 11. Aux Cable (1 pcs.)
 12. Micro USB to Standard USB cable (1 pcs.) [also called Micro USB to USB type A cable]
 13. Soldering Iron/Solder wire

## Skills Required:

 - Basic soldering skills (if you just practice for joining wires by soldering them together for few times, you should be good to go. But if you still feel uncomfortable, getting help is a good idea.)
 - Basic computer skills (if you're already here, then don't worry)

## Notes:

 - If you don't want to solder then you still have an option; Jumper Wires and Breakout Boards, you could just buy 2 rp pico H (the one with headers pre soldered) and breakout boards for Audio Jack and the IR transmitter then connect them by jumper wires. But if you can somehow manage to solder everything then you'll thank yourself a lot later, as jumper wires are very likely to get loose after a while.

## Software Installation:
- Santroller [get the latest release: https://github.com/Santroller/Santroller/releases/]
- Circuitpython [get the latest release: https://circuitpython.org/board/raspberry_pi_pico/]
## Hardware Installation:
### The main raspberry pi pico (all the components will be connected to this pico)
- Connect a 220uF capacitor to the power rail of the pico. (+ve -> VSYS and -ve -> GND)
- Connect another 220uF capacitor to the aux port input. (+ve -> GP26 and -ve -> GND)
- follow the following schematic:
![the main rp pico schematic](https://github.com/THEKODIKO/DAB-Dumb_way_to_Automatize_BadUpdate/blob/9ef4fc86da7cf174522e9c2a99d1b0a916c47d0f/assets/main-rp-pico-schematic.jpg "the main rp pico schematic")


## Software Setup:
**Note**: Since you have 2 Raspberry pi picos, one of them will server as a santroller and the other will contain the circuitpython code. Also it doesn't matter which raspberry pi pico is what.
### Santroller (the controller emulating Raspberry pi pico ):
- Video link (full setup, also check the description): https://youtu.be/sRtnlW2Wy2o
- Start Button config (missed in the video)
![start button config](https://github.com/THEKODIKO/DAB-Dumb_way_to_Automatize_BadUpdate/blob/9ef4fc86da7cf174522e9c2a99d1b0a916c47d0f/assets/start_btn_config.jpg "start button config")
- Pinout (Pulled Down) (Raspberry pi pico):
	- A -> 16
	- B -> 17
	- X -> 12
	- Y -> 13
	- LB -> 19
	- RB -> 18
	- D-pad Lft -> 21
	- D-pad Ryt -> 20
	- D-pad Up -> 14
	- D-pad Down -> 15
	- Xbox Btn (guide btn) -> 22
	- Start Btn -> 11
### Circuitpython (2nd Raspberry pi pico): 
- Disconnect the Pico from the computer.
- Press/Hold the BOOTSEL btn.
- Now re-connect the Pico.
- Now a new drive will appear in File Explorer.
![RPI-RP2](https://github.com/THEKODIKO/DAB-Dumb_way_to_Automatize_BadUpdate/blob/aa2319266f253f76fae2c06939434fb5cbf1ae86/assets/img_1.jpg "RPI-RP2")
- Copy/Paste the 'flash_nuke.uf2' [this file is included when you download the release]
- The Pico will automatically disconnect and after few seconds re-connect. Then Copy/Paste the circuitpython (.uf2) file to the pico volume you downloaded in the installation section.
- Again the pico will disconnect and re-connect, Now copy paste the .py files of the release to the pico volume.

# You're Done! Congratulations🎉🎉
- Now shut down your Xbox 360 (don't disconnect the power though); connect the raspberry pi pico which is the santroller to your Xbox and Now the Xbox must turn on. (see the expected behavior: )
- Forgot which pico is the santroller? try both them for few seconds and see which works and mark it.
- If it doesn't, don't worry it happens to the best of us, check the troubleshooting section below. 

##  Troubleshooting
Under work...

# Credits
**Author**:  
- Github: THEKODIKO
- Reddit: u/Zarnilopho

**I stand on the shoulders of the giants.**
**Giants**: 
- Thanks InvoxiPlayGames (github)
- Thanks grimdoomer (github)
- Thanks to u/baapo and everyone on my reddit post.(https://www.reddit.com/r/360hacks/comments/1jinlha/just_made_the_badupdate_exploit_automatic_dumb_way/)
