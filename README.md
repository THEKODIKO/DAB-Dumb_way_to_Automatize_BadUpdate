# DAB - A Dumb way to Automatize Bad update exploit.

## Items Required : 

 1. Raspberry pi pico (1 pcs.) [for ref. https://www.digikey.com/en/products/detail/raspberry-pi/SC0915/13624793]
 2. Raspberry pi pico H (1 pcs.) [for ref. https://www.digikey.com/en/products/detail/raspberry-pi/SC0917/16608257]
 3. IR Transmitter (1 pcs.) [for ref. https://www.digikey.com/en/products/detail/everlight-electronics-co-ltd/IR333-A/2675571]
 4. Some wires 
 5. 220uf Electrolytic Capacitors  (2 pcs.) [for ref. https://www.digikey.com/en/products/detail/rubycon/25YXJ220M6-3X11/3563124]
 6. 3.5 mm Audio Jack (aux port) breakout board (1 pcs.) [for ref. https://www.digikey.in/en/products/detail/kycon-inc/STX-3000/9975995]
 7. Aux Cable (1 pcs.)
 8. Micro USB to Standard USB cable (1 pcs.) [also called Micro USB to USB type A cable]
 9. Soldering Iron/Solder wire

## Skills Required:

 - Basic soldering skills (if you just practice for joining wires by soldering them together for few times, you should be good to go. But if you still feel uncomfortable, getting help is a good idea.)
 - Basic computer skills (if you're already here, then don't worry)

## Notes:

 - If you don't want to solder then you still have an option; Jumper Wires and Breakout Boards, you could just buy 2 rp pico H (the one with headers pre soldered) and breakout boards for Audio Jack and the IR transmitter then connect them by jumper wires. But if you can somehow manage to solder everything then you'll thank yourself a lot later, as jumper wires are very likely to get loose after a while.

## Software Installation:
- Santroller [get the latest release: https://github.com/Santroller/Santroller/releases/]
- Circuitpython [get the latest release: https://circuitpython.org/board/raspberry_pi_pico/]
## Hardware Installation:
- See video -> []

## Software Setup:
**Note**: Since you have 2 Raspberry pi picos, one of them will server as a santroller and the other will contain the circuitpython code. Also it doesn't matter which raspberry pi pico is what.
### Santroller (1st Raspberry pi pico ):
- Video link (full setup): 
- Pinout (Raspberry pi pico):
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
	- Xbox Btn -> 22
### Circuitpython (2nd Raspberry pi pico): 
- Disconnect the Pico from the computer.
- Press/Hold the BOOTSEL btn.
- Now re-connect the Pico.
- Now a new drive will appear in File Explorer. [image: https://drive.google.com/file/d/1GN7dG9lE5OkKltLHeDHoa1IMckQbaWBi/view?usp=sharing]
![RPI-RP2](https://drive.google.com/file/d/1GN7dG9lE5OkKltLHeDHoa1IMckQbaWBi/view?usp=sharing)
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
**Repo Creator**:  
- Github: THEKODIKO
- Reddit: u/Zarnilopho

**I stand on the shoulders of the giants.**
**Giants**: 
- Thanks InvoxiPlayGames (github)
- Thanks grimdoomer (github)
- Thanks to u/baapo and everyone on my reddit post.(https://www.reddit.com/r/360hacks/comments/1jinlha/just_made_the_badupdate_exploit_automatic_dumb_way/)
