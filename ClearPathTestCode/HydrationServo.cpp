#include <Python.h>
#include <stdio.h>		
#include <iostream>
#include "pubSysCls.h"	

using namespace sFnd;

#define CHANGE_NUMBER_SPACE	2000	//The change to the numberspace after homing (cnts)
#define TIME_TILL_TIMEOUT	50000	//The timeout used for homing(ms) -- low from bottom
#define ACC_LIM_RPM_PER_SEC	300
#define VEL_LIM_RPM			30
#define CNTS_PER_MM			400
#define RPM_PER_MM_PER_SECOND			30

SysManager myMgr;	//Create System Manager myMgr
INode *pTheNode ;       // Pointer to the Node

double _get_position(){
  INode &theNode = *(pTheNode);
  theNode.Motion.PosnMeasured.Refresh();
  double myPosn = (theNode.Motion.PosnMeasured.Value()) / (CNTS_PER_MM * 1000);
  return myPosn;
}

int _set_drill_speed(double speed){
	/*
	Parameters
	-------------
	speed: run to this speed
	Outputs
	-------------
	return 1: set speed successfully
	-1: did not set speed
	 */
  INode &theNode = *(pTheNode);
  theNode.Motion.MoveWentDone(); //Clear the rising edge Move done register
  theNode.AccUnit(INode::RPM_PER_SEC);	//Set the units for Acceleration to RPM/SEC
  theNode.VelUnit(INode::RPM);		//Set the units for Velocity to RPM
  theNode.Motion.AccLimit = ACC_LIM_RPM_PER_SEC; //Set Acceleration Limit (RPM/Sec)
  theNode.Motion.VelLimit = VEL_LIM_RPM;	 //Set Velocity Limit (RPM)
  theNode.Motion.MoveVelStart(speed);
  printf("Speed set to %lf m/s\n", speed);
  return 1;
}


static PyObject *get_drill_position(PyObject *self, PyObject *args) {
  return PyFloat_FromDouble(_get_position());
}


static PyObject *set_drill_speed(PyObject *self, PyObject *args) {
  double speed;
  if (!PyArg_ParseTuple(args, "d", &speed)) {
    return NULL;
  }

  int set_speed = _set_drill_speed(speed);
  if (set_speed > 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}

static PyMethodDef HydrationServo_methods[] = {
    {"get_drill_position", get_drill_position, METH_VARARGS, "Returns drill position"},
    {"set_drill_speed", set_drill_speed, 
	    METH_VARARGS, "Sets drill speed"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef HydrationServo_definition = {
    PyModuleDef_HEAD_INIT,
    "HydrationServo",
    "A Python module to control Hydration Clear Path Servos",
    -1,
    HydrationServo_methods
};


// Send message and wait for newline
char msgUser(const char *msg) {
	std::cout << msg;
	char input;
	input = getchar();
	return input;
}


int connect_clearpath(void) {
   /*
  -------------------------------
  CONNECTION CODE STARTS HERE
  -------------------------------
  */
	size_t portCount = 0;
	std::vector<std::string> comHubPorts;
	pTheNode = NULL;

	//Create the SysManager object. This object will coordinate actions among various ports
	// and within nodes. In this example we use this object to setup and open our port.

	//This will try to open the port. If there is an error/exception during the port opening,
	//the code will jump to the catch loop where detailed information regarding the error will be displayed;
	//otherwise the catch loop is skipped over
	try {

		SysManager::FindComHubPorts(comHubPorts);
		printf("Found %ld SC Hubs\n", comHubPorts.size());

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
				pTheNode = &theNode; // store address to the first node

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
			}
		}
	
        /*
        -------------------------------
        CONNECTION CODE ENDS HERE
        -------------------------------*/
	}
	catch (mnErr& theErr) {
		//This statement will print the address of the error, the error code (defined by the mnErr class),
		//as well as the corresponding error message.
		printf("Caught error: addr=%d, err=0x%08x\nmsg=%s\n", theErr.TheAddr, theErr.ErrorCode, theErr.ErrorMsg);
		msgUser("Press any key to continue."); //pause so the user can see the error message; waits for user to press a key

		return 0;  //This terminates the main program
	}
  return 0;			//End program			
}

PyMODINIT_FUNC PyInit_HydrationServo(void) {
  Py_Initialize();
  PyObject *m = PyModule_Create(&HydrationServo_definition);

  connect_clearpath();

  return m;
}
