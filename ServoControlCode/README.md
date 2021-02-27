
# Setup
*Tested on Ubuntu 20.04.2 LTS on a Dell XPS15*

**Setting up hub drivers**
1. Unpack Linux_Software.tar
2. Navigate into Linux_Software, and unpack the hubDriverPkg and sFoundationPkg tars
3. **IMPORTANT:** Check that the sFoundationPkg folder contains the "sFoundation" folder - for some reason, I had to extract it individually otherwise it wouldn't show up.
4. Download & install Eclipse for C++ - the latest version works fine
5. Run `sudo usermod -aG dialout {user acct}`
6. Ensure the `sestatus` command outputs `disabled`
7. Navigate to the `hubDriverPkg/ExarKernelDriver/` folder
8. Run `sudo apt-get install linux-headers-$(uname -r)`
9. Run `make`
10. Run `insmod ./xr_usb_serial_common.ko` 
11. Run `sudo ./install_drvr` 
12. Plug in SC-HUB via USB
13. Run `ls /dev/ttyXRUSB*` to test that the hub has been successfully recognized. If it hasn't, see the two READMEs in `Linux_Software/hubDriverPkg/ExarKernelDriver/` and `Linux_Software` for further instructions and debugging.

**Installing sFoundation shared C++ Library**

14. Start up Eclipse. Create a new workspace, with Linux_Software acting as the root of your project folder.

15. Using the Project Explorer on the left, click on the sFoundation folder (under sFoundationPkg).

16. Click on the arrow next to the Build menu option (the hammer icon in the top bar)

17. Select Release

18. Build by clicking on the hammer icon.

19. In Terminal, navigate to the sFoundation directory

20. Run `sudo cp MNuserDriver20.xml /usr/lib`

21. Navigate to the Release directory (`cd Release`), which should have been created after the previous build.

22. Run `sudo cp libsFoundation20.so /usr/lib`

23. Navigate to `/usr/lib`, run `ldconfig -n .`

24. At this point, if you run `ls /usr/lib`, you should see `libsFoundation20.so.1` in light blue letters. If it's highlighted in red, then something has gone wrong. Refer to the README in the root directory (`Linux_Software`), and more specifically [this website](https://tldp.org/HOWTO/Program-Library-HOWTO/shared-libraries.html)

**Building and running interface**

25. Try building `SDK Examples/HelloWorld` by clicking on the arrow next to the Build Icon, selecting `Debug_With_LinuxGCC` and then pressing the Build Icon. If you encounter no `pthread` related errors, skip to step 27. If you encounter errors relating to the sFoundation library, then something went wrong during the installation of the shared library. If it gives you errors regarding pthread, read step 26.

26. Right click the `Hello World` folder. Select `Properties`. Under `Configuration`, select `[Multiple Configurations..]`.  Select `Debug_with_LinuxGCC` and `Release_with_LinuxGCC`. Under `Tool Settings` tab, select `GCC C++ Linker/Miscellaneous`. In `Linker flags`, type `-pthread`. Click on Apply and Close (bottom right). Try and build `HelloWorld` as I described in the first sentence of this step.

27. If `HelloWorld` builds, great! Navigate to `SDK_Examples/Example-Homing`. Open `Example-Homing.cpp`, and replace all the code (delete & copy-paste) in there with the code from `run.cpp` (found in this repo). The reason for this is because after hours of trying, I have (for now) given up on trying to make my own project folders in Linux_Software.

28. With the hub plugged in, build your new `Example-Homing.cpp` with `Debug_with_LinuxGCC`. 

29. Through the Eclipse Project Explorer window, navigate to the newly generated `Example-Homing/Debug_with_LinuxGCC` folder

30. Right click on the `Example-Homing - [x84_64/le]`executable, and select `Run As/Local C/C++ Application`. If you have any problems with ports/the hub, terminate the program and unplug and replug the USB.

31. Follow the instructions on the Eclipse console


# Usage
In it's current form, the program runs using  a simplistic UI, where you enter commands in the form of letters to control the drill. At the beginning of the program, the interface guides you through "soft-homing" the drill. If you wish, you can turn on hard homing.

---------
**Soft homing**
Motor turns until user presses a key. Wherever it stops is considered "home"

**Hard homing**
Motor turns until it encounters significant resistance. Untested (tried holding the motor in place, did not work - perhaps I am not strong enough?) If you wish to turn hard homing ON, change 
`homing(true, theNode);` 
to
`homing(false, theNode);`

----

The commands are as follows:

`u`: Increase RPM by 10 in the upwards direction (i.e. from 0 go to 10, or from -20 go to 10)
`d`: Increase RPM by 10 in the downards direction (i.e. from -10 go to -20, or from 20 go to 10)
`n`: Provide statistics such as torque, torque error, position, speed, etc.
`s`: Stop the motor
`e`: End the program gracefully (**run this if you don't want port errors the next time you start the program**)

Note: The program has only been tested for a hub connected to 1 drill so far.



# Development
I've tried to make `run.cpp` as easy as I can for you to use. If you get bored of using my simplistic interface and want to actually get started writing your own control code, scroll down in the code to the section which says `YOUR CODE STARTS HERE`. You can use functions I wrote to make things like homing and changing speed a lot easier. The functions are

`get_position(node)` - position in meters
`get_rop(node)` - velocity in m/s
`get_torque(node)` - percentage of maximum torque
`get_torque_error(node)`
`get_pos_error(node)` - position error in meters (difference from commanded and actual)
`homing(softHoming[boolean], node)` - homes motor, hard if softHoming is set to false, soft otherwise 
`setSpeed(speed[double], node)` - sets speed of motor. 0 is stationary, 10 is 10 rpm upwards, -10 is 10 rpm downwards.

The code in it's current form will iterate over each node connected to the hub.

In the near future, this will be ported to Python. This is a temporary abstraction layer so that we can begin playing around with the motors using code.


# Included in this directory
*(this is moreso for me, to note done things to include in here in case I forget)*
* Linux_Software.tar - contains library code
* sFoundation Windows Guide - can be viewed on a Windows machine, extremely helpful library reference guide. AFAIK there is no version of this that is viewable on Linux, which sucks. 100% worth running a VM or second Windows laptop just to view this guide if you're writing code, however.
* run.cpp 
