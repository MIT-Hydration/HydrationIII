//Required include files
#include <stdio.h>
#include <string>
#include <iostream>
#include "pubSysCls.h"

using namespace sFnd;

#define CHANGE_NUMBER_SPACE	2000	//The change to the numberspace after homing (cnts)
#define TIME_TILL_TIMEOUT	50000	//The timeout used for homing(ms) -- low from bottom
#define ACC_LIM_RPM_PER_SEC	300
#define VEL_LIM_RPM			30
#define CNTS_PER_MM			400
#define RPM_PER_MM_PER_SECOND			30

SysManager myMgr;							//Create System Manager myMgr

// Send message and wait for newline
char msgUser(const char *msg) {
	std::cout << msg;
	char input;
	input = getchar();
	return input;
}


/* GET FUNCTIONS
------------------------
get_position - in meters
get_rop - rate of penetration (velocity in m/s)
get_torque -
get_torque_error
get_pos_error
*/

double get_position(INode &theNode){
	theNode.Motion.PosnMeasured.Refresh();
	double myPosn = (theNode.Motion.PosnMeasured.Value()) / CNTS_PER_MM * 1000;
	return myPosn;
}

double get_rop(INode &theNode){
	theNode.Motion.VelMeasured.Refresh();
	double myVel = theNode.Motion.VelMeasured.Value() / RPM_PER_MM_PER_SECOND * 1000; // divided by 30k to get m/s
	return myVel;
}

double get_torque(INode &theNode){
	theNode.Motion.TrqMeasured.Refresh();
	double myTorque = theNode.Motion.TrqMeasured.Value();
	return myTorque;
}


double get_torque_error(INode &theNode){
	theNode.Motion.TrqCommanded.Refresh();
	double myTrqError = theNode.Motion.TrqCommanded.Value() - get_torque(theNode);
	return myTrqError;
}

double get_pos_error(INode &theNode){
	theNode.Motion.PosnTracking.Refresh();
	double myPosnErr = theNode.Motion.PosnTracking.Value();
	return myPosnErr;
}




int homing(bool softHoming, INode &theNode){
	/*
  Parameters
  -------------
  softHoming: if true, will move in the positive direction until a key is pressed (simulating a "hard stop" event)
              if false, will move in the positive direction until a hard stop occurs, at which point the motor controller will complete homing automatically. note that for this to happen, the Hard Stop option must be selected in the Clearview under Homing Setup

  Outputs
  -------------
  return 1: homed successfully
        -1: did not home
  */
  msgUser("Homing starting. Press Enter to proceed with homing.");
  theNode.Motion.Homing.Initiate();
  if (softHoming) {
    msgUser("Press key to set home.");
    double posn_measured = theNode.Motion.PosnMeasured;
    theNode.Motion.AddToPosition(-posn_measured);
    theNode.Motion.Homing.SignalComplete();
  }
  else {
	double timeout = myMgr.TimeStampMsec() + TIME_TILL_TIMEOUT;	//define a timeout in case the node is unable to enable
																	//This will loop checking on the Real time values of the node's Ready status
    while (!theNode.Motion.Homing.WasHomed()) {
      if (myMgr.TimeStampMsec() > timeout) {
        printf("Node did not complete homing:  \n\t -Ensure Homing settings have been defined through ClearView. \n\t -Check for alerts/Shutdowns \n\t -Ensure timeout is longer than the longest possible homing move.\n");
        //msgUser("Press any key to continue."); //pause so the user can see the error message; waits for user to press a key
        return -1;
      }
    }
  }

  printf("Stopping Node\n");
  theNode.Motion.PosnMeasured.Refresh();		//Refresh our current measured position
  printf("Node completed homing, current position: \t%8.0f \n", theNode.Motion.PosnMeasured.Value());
  //theNode.EnableReq(false);
  theNode.Motion.NodeStop(STOP_TYPE_ABRUPT);
  msgUser("Press key to continue...");
  return 1;
}

int setSpeed(double speed, INode &theNode){
	/*
	Parameters
	-------------
	speed: run to this speed

	Outputs
	-------------
	return 1: set speed successfully
	-1: did not set speed
	 */
	theNode.Motion.MoveWentDone();						//Clear the rising edge Move done register
	theNode.AccUnit(INode::RPM_PER_SEC);				//Set the units for Acceleration to RPM/SEC
	theNode.VelUnit(INode::RPM);						//Set the units for Velocity to RPM
	theNode.Motion.AccLimit = ACC_LIM_RPM_PER_SEC;		//Set Acceleration Limit (RPM/Sec)
	theNode.Motion.VelLimit = VEL_LIM_RPM;				//Set Velocity Limit (RPM)
	theNode.Motion.MoveVelStart(speed);
	printf("Speed set\n");
	return 1;
}





int main(int argc, char* argv[]) {
  /*
  -------------------------------
  CONNECTION CODE STARTS HERE
  -------------------------------
  */
	size_t portCount = 0;
	std::vector<std::string> comHubPorts;

	//Create the SysManager object. This object will coordinate actions among various ports
	// and within nodes. In this example we use this object to setup and open our port.

	//This will try to open the port. If there is an error/exception during the port opening,
	//the code will jump to the catch loop where detailed information regarding the error will be displayed;
	//otherwise the catch loop is skipped over
	try {

		SysManager::FindComHubPorts(comHubPorts);
		printf("Found %d SC Hubs\n", comHubPorts.size());

		for (portCount = 0; portCount < comHubPorts.size() && portCount < NET_CONTROLLER_MAX; portCount++) {

			myMgr.ComHubPort(portCount, comHubPorts[portCount].c_str()); 	//define the first SC Hub port (port 0) to be associated
											// with COM portnum (as seen in device manager)
		}

		if (portCount > 0) {
			//printf("\n I will now open port \t%i \n \n", portnum);
			myMgr.PortsOpen(portCount);				//Open the port

			for (size_t i = 0; i < portCount; i++) {
				IPort &myPort = myMgr.Ports(i);

				printf(" Port[%d]: state=%d, nodes=%d\n",
					myPort.NetNumber(), myPort.OpenState(), myPort.NodeCount());
			}
		}
		else {
			printf("Unable to locate SC hub port\n");

			msgUser("Press any key to continue."); //pause so the user can see the error message; waits for user to press a key

			return -1;  //This terminates the main program
		}


		//Once the code gets past this point, it can be assumed that the Port has been opened without issue
		//Now we can get a reference to our port object which we will use to access the node

		for (size_t iPort = 0; iPort < portCount; iPort++) {
			// Get a reference to the port, to make accessing it easier
			IPort &myPort = myMgr.Ports(iPort);

			for (unsigned iNode = 0; iNode < myPort.NodeCount(); iNode++) {

				//////////////////////////////////////////////////////////////////////////////////////////////////////////
				//Here we identify the first Node, enable and home the node, then adjust the position reference
				//////////////////////////////////////////////////////////////////////////////////////////////////////////

						// Create a shortcut reference for the first node
				INode &theNode = myPort.Nodes(iNode);

				//theNode.EnableReq(false);				//Ensure Node is disabled before starting

				printf("   Node[%d]: type=%d\n", iNode, theNode.Info.NodeType());
				printf("            userID: %s\n", theNode.Info.UserID.Value());
				printf("        FW version: %s\n", theNode.Info.FirmwareVersion.Value());
				printf("          Serial #: %d\n", theNode.Info.SerialNumber.Value());
				printf("             Model: %s\n", theNode.Info.Model.Value());

				//The following statements will attempt to enable the node.  First,
				// any shutdowns or NodeStops are cleared, finally the node in enabled
				theNode.Status.AlertsClear();					//Clear Alerts on node
				theNode.Motion.NodeStopClear();	//Clear Nodestops on Node
				theNode.EnableReq(true);					//Enable node

				double timeout = myMgr.TimeStampMsec() + TIME_TILL_TIMEOUT;	//define a timeout in case the node is unable to enable
																			//This will loop checking on the Real time values of the node's Ready status
				while (!theNode.Motion.IsReady()) {
					if (myMgr.TimeStampMsec() > timeout) {
						printf("Error: Timed out waiting for Node %d to enable\n", iNode);
						msgUser("Press any key to continue."); //pause so the user can see the error message; waits for user to press a key
						return -2;
					}
				}
        /*
        -------------------------------
        CONNECTION CODE ENDS HERE
        -------------------------------
        */
        /*
        -------------------------------
        YOUR CODE STARTS HERE
        -------------------------------
        As this is part of the "for iNode" loop, code here will be run individually for every connected motor.
        If you want to run code for a single motor, you might want to perform a simple if statement, checking that theNode.Info.UserID.Value() matches the ID of the motor you want to run.
        */
		homing(true, theNode);
		double speed = 0;
		char input = 'a';
		while (input != 'e') {
			printf("Available instructions:\nu: Will change RPM by +10, up to a maximum of 100\nd: Will change RPM by -10, to a minimum of -100\ns: Will stop the motor\nn: Will print stats (speed, pos, torque)\ne: End program gracefully\n");
			input = msgUser("Enter command: \n");
			if (input == 'u') {
				if (speed < 100) {
					speed += 10;
					if (speed == 0) {
						speed += 10;
					}
					setSpeed(speed, theNode);
				}
				else {
					printf("RPM ceiling reached.\n");
				}
			}
			else if (input == 'd'){
				if (speed > -100) {
					speed -= 10;
					if (speed == 0) {
						speed -= 10;
					}
					setSpeed(speed, theNode);
				}
				else {
					printf("RPM floor reached.\n");
				}
			}
			else if (input == 's'){
				speed = 0; //Not passed to setSpeed but registered in the variable nonetheless
				theNode.Motion.NodeStop(STOP_TYPE_RAMP_AT_DECEL);
			}
			else if (input == 'n'){
				printf("Set speed: ");
				printf("%f", speed);
				printf("\n");
				printf("Position: ");
				printf("%f", get_position(theNode));
				printf("\n");
				printf("Rate of penetration: ");
				printf("%f", get_rop(theNode));
				printf("\n");
				printf("Torque: ");
				printf("%f", get_torque(theNode));
				printf("\n");
				printf("Torque error: ");
				printf("%f", get_torque_error(theNode));
				printf("\n");
				printf("Position error: ");
				printf("%f", get_pos_error(theNode));
				printf("\n");
			}
			else if (input != 'e') {
				printf("Invalid input\n");
			}
			if (input != 'e'){
				msgUser("Press enter to continue\n");
				printf("------------");
			}
		}
        /*
        -------------------------------
        YOUR CODE ENDS HERE
        -------------------------------
        However, you can run code further down, if you like.
        */
      }
    }
  }
  catch (mnErr& theErr) {
		//This statement will print the address of the error, the error code (defined by the mnErr class),
		//as well as the corresponding error message.
		printf("Caught error: addr=%d, err=0x%08x\nmsg=%s\n", theErr.TheAddr, theErr.ErrorCode, theErr.ErrorMsg);
		msgUser("Press any key to continue."); //pause so the user can see the error message; waits for user to press a key

		return 0;  //This terminates the main program
	}
  myMgr.PortsClose();
  msgUser("Press any key to end."); //pause so the user can see the error message; waits for user to press a key
  return 0;			//End program
}
