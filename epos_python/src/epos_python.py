#!/usr/bin/env python3

import rospy
import can
import canopen
import std_msgs
import os,sys
from struct import *



def main():

    rospy.init_node('maxon_control', anonymous=True)
    current_time = rospy.Time.now()
    print("initialized maxon motor control node ...")

    network = canopen.Network()

    # Add node with corresponding Object Dictionaries
    node = network.add_node(31, '.../MCDepos_node_1.dcf')

    #connect to network
    #socketcan (this works fine for me ater connecting to socketcan)
    network.connect(bustype='socketcan', channel='can0')
    # network.connect(bustype='ixxat', channel=0, bitrate=250000)	#ixxat (never tried this one)

    #this has to be executed just once, in order to set motor in enabled
    node.sdo.download(0x6040, 0, b'\x06\x00')
    node.sdo.download(0x6040, 0, b'\x0F\x00')
    rospy.sleep(0.03)	                                                        #wait 30ms to get in enabled mode

    #you can put this in a loop or callback to move the motor as you wish
    #node.sdo.download(0x6081,0, b'\xE8\x0A\x00\x00')    #you can set desired velocity if you want
    node.sdo.download(0x607A, 0, b'\xFF\xF3\x00\x00')	#set target position
    node.sdo.download(0x6040, 0, b'\x7F\x00')
    node.sdo.download(0x6040, 0, b'\x0F\x00')

    #read statusword
    statusword = node.sdo[0x6041].raw
    print(statusword)

network.disconnect()
   if __name__ == '__main__':
try:
    main()
    except rospy.ROSInterruptException:
pass
