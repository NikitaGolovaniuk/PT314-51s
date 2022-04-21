# **All about notebook Acer Predator Triton 300 SE**
#### Model number: PT314-51s

> ###  HOW TO BIND PREDATOR BUTTON
#### Problem: X11 accept only 1 byte info as keycode so
#### its restricted to 0-255 values and if you want to 
#### bind key with keycode above 255 then you should use 
#### translator/router. According to this [page](https://ubuntuforums.org/showthread.php?t=2182054)
#### We will use evrouter from AUR.
1. go to aur and grab last PKGBUILD from comments https://aur.archlinux.org/packages/evrouter or take my PKGBUILD_EVROUTER and remove _EVROUTER
2. Install it manually by commands:
```
cd YOUR_DIR_WITH_PKGBUILD
makepkg -si
```
3. Now you have evrouter installed. Now you should set rules
I missed this step but it could be neccesary for you

Add a rule to allow users to read /dev/input/event*
```
echo 'KERNEL=="event*", NAME="input/%k", GROUP="input" | sudo tee /etc/udev/rules.d/80-evrouter.rules

sudo addgroup input

sudo usermod -aG input ${USER}

sudo reboot
```

4. type evtest in terminal and find your keycode and keyboard name.
Mine output:
/dev/input/event3:	AT Translated Set 2 keyboard
So i pressed '3' and checked keycode of needed button it was 425

5. Create a evrouter file config (${HOME}/.evrouterrc):
```
Format:
"Name of your event" "event link" none key/Number_your_key "XKey/Name_your_key"
Mine:
"AT Translated Set 2 keyboard" "/dev/input/event3" none key/425 "XKey/XF86Community"
```
<details><summary>A dropdown list of names</summary>

    XF86AudioRecord
    XF86AudioRewind
    XF86AudioStop
    XF86Away
    XF86Back
    XF86Book
    XF86BrightnessAdjust
    XF86CD
    XF86Calculator
    XF86Calendar
    XF86Clear
    XF86ClearGrab
    XF86Close
    XF86Community
    XF86ContrastAdjust
    XF86Copy
    XF86Cut
    XF86DOS
    XF86Display
    XF86Documents
    XF86Eject
    XF86Excel
    XF86Explorer
    XF86Favorites
    XF86Finance
    XF86Forward
    XF86Game
    XF86Go
    XF86History
    XF86HomePage
    XF86HotLinks
    XF86Launch0
    XF86Launch1
    XF86Launch2
    XF86Launch3
    XF86Launch4
    XF86Launch5
    XF86Launch6
    XF86Launch7
    XF86Launch8
    XF86Launch9
    XF86LaunchA
    XF86LaunchB
    XF86LaunchC
    XF86LaunchD
    XF86LaunchE
    XF86LaunchF
    XF86LightBulb
    XF86LogOff
    XF86Mail
    XF86MailForward
    XF86Market
    XF86Meeting
    XF86Memo
    XF86MenuKB
    XF86MenuPB
    XF86Messenger
    XF86Music
    XF86MyComputer
    XF86MySites
    XF86New
    XF86News
    XF86Next_VMode
    XF86Prev_VMode
    XF86OfficeHome
    XF86Open
    XF86OpenURL
    XF86Option
    XF86Paste
    XF86Phone
    XF86Pictures
    XF86PowerDown
    XF86PowerOff
    XF86Next_VMode
    XF86Prev_VMode
    XF86Q
    XF86Refresh
    XF86Reload
    XF86Reply
    XF86RockerDown
    XF86RockerEnter
    XF86RockerUp
    XF86RotateWindows
    XF86RotationKB
    XF86RotationPB
    XF86Save
    XF86ScreenSaver
    XF86ScrollClick
    XF86ScrollDown
    XF86ScrollUp
    XF86Search
    XF86Send
    XF86Shop
    XF86Sleep
    XF86Spell
    XF86SplitScreen
    XF86Standby
    XF86Start
    XF86Stop
    XF86Support
    XF86Switch_VT_1
    XF86Switch_VT_10
    XF86Switch_VT_11
    XF86Switch_VT_12
    XF86Switch_VT_2
    XF86Switch_VT_3
    XF86Switch_VT_4
    XF86Switch_VT_5
    XF86Switch_VT_6
    XF86Switch_VT_7
    XF86Switch_VT_8
    XF86Switch_VT_9
    XF86TaskPane
    XF86Terminal
    XF86ToDoList
    XF86Tools
    XF86Travel
    XF86Ungrab
    XF86User1KB
    XF86User2KB
    XF86UserPB
    XF86VendorHome
    XF86Video
    XF86WWW
    XF86WakeUp
    XF86WebCam
    XF86WheelButton
    XF86Word
    XF86XF86BackForward
    XF86Xfer
    XF86ZoomIn
    XF86ZoomOut
    XF86iTouch
    XF86AddFavoriteXF86ApplicationLeft
    XF86ApplicationRight
    XF86AudioMedia
    XF86AudioMute
    XF86AudioNext
    XF86AudioPause
    XF86AudioPlay
    XF86AudioPrev
    XF86AudioLowerVolume
    XF86AudioRaiseVolume
</details>



    

6. Look the keys free with xmodmap, eg:
```
    xmodmap -pke | egrep "=$"
```
7. Create a xmodmap file config (${HOME}/.xmodmap):
```
    Format:
    keycode Number_key_free = Name_your_key
    Mine:
    keycode 97 = XF86Community
```
8. Connect all things
```
    xmodmap ~/.xmodmap
    evrouter /dev/input/event3
```
9. Type xev and test your key
10. If all is good. Add those strings to autostart in your DM like i3wm etc.
```
    modmap ~/.xmodmap
    evrouter /dev/input/event3
```

Biggest thanks to hizo for his big job!
