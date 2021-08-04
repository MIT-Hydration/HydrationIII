#include <Python.h>
#include <stdio.h>		
#include <iostream>
#include "pubSysCls.h"	

using namespace sFnd;

#define INIT_TIMEOUT	1000	//Initialize timeout

#define ACC_LIM_RPM_PER_SEC	300
#define VEL_LIM_RPM			300
#define CNTS_PER_MM			400
#define RPM_PER_MM_PER_SECOND			30
#define THREAD_PITCH (2.0/1000.0) // meters (2 mm pitch)

#define NUM_MOTORS_MAX 4

SysManager myMgr;	//Create System Manager myMgr
INode * pTheNode[NUM_MOTORS_MAX] ;       // Pointer to the Node
unsigned numNodesDetected = -1;

int _motor_status(unsigned long i){ 

    char alertList[256];
    INode &theNode = *(pTheNode[i]); //do i do a copy of stop all motors where the i is == 0  How to make it return an error instead of a number 


    printf("Checking for Alerts: \n");

  

    // make sure our registers are up to date
    theNode.Status.RT.Refresh();
    theNode.Status.Alerts.Refresh();

    printf("---------\n");
    printf(" Checking node %i for Alerts:\n", iNode);

    // Check the status register's "AlertPresent" bit
    // The bit is set true if there are alerts in the alert register
    if (!theNode.Status.RT.Value().cpm.AlertPresent) {
      printf("   Node has no alerts!\n");
    }
    //Check to see if the node experienced torque saturation
    if (theNode.Status.HadTorqueSaturation()) {
      printf("      Node has experienced torque saturation since last checking\n");
    }
    // get an alert register reference, check the alert register directly for alerts
    if (theNode.Status.Alerts.Value().isInAlert()) {
      // get a copy of the alert register bits and a text description of all bits set
      theNode.Status.Alerts.Value().StateStr(alertList, 256);
      printf("   Node has alerts! Alerts:\n%s\n", alertList);

      // can access specific alerts using the method below
      if (theNode.Status.Alerts.Value().cpm.Common.EStopped) {
        printf("      Node is e-stopped: Clearing E-Stop\n");
        theNode.Motion.NodeStopClear();
      }
      if (theNode.Status.Alerts.Value().cpm.TrackingShutdown) {
        printf("      Node exceeded Tracking error limit\n");
      }

      

      // Check for more alerts and Clear Alerts
      theNode.Status.Alerts.Refresh();
      if (theNode.Status.Alerts.Value().isInAlert()) {
        theNode.Status.Alerts.Value().StateStr(alertList, 256);
        printf("      Node has non-estop alerts: %s\n", alertList);
        printf("      Clearing non-serious alerts\n");
       // theNode.Status.AlertsClear(); //require this for future clearalert button

        // Are there still alerts?
        theNode.Status.Alerts.Refresh();
        if (theNode.Status.Alerts.Value().isInAlert()) {
          theNode.Status.Alerts.Value().StateStr(alertList, 256);
          printf("   Node has serious, non-clearing alerts: %s\n", alertList);
        }
        else {
          printf("   Node %d: all alerts have been cleared\n", theNode.Info.Ex.Addr());
        }
      }
      else {
        printf("   Node %d: all alerts have been cleared\n", theNode.Info.Ex.Addr());
      }

    }
    
  

    
  
  return 1; // ERIC how to make it return an error instead of a number, one of the errors above. 
}

double _get_position(unsigned long i){
  INode &theNode = *(pTheNode[i]);
  theNode.Motion.PosnMeasured.Refresh();
  double myPosn = (theNode.Motion.PosnMeasured.Value()) / (CNTS_PER_MM * 1000);
  return myPosn;
}

double _get_torque(unsigned long i){ 
	INode &theNode = *(pTheNode[i]);
	theNode.Motion.TrqMeasured.Refresh();
	double myTorque = theNode.Motion.TrqMeasured.Value();
	return myTorque;

}

int _set_home(unsigned long i){
	INode &theNode = *(pTheNode[i]);
	double posn_measured = theNode.Motion.PosnMeasured;
    theNode.Motion.AddToPosition(-posn_measured);
	/* printf("Position set to %f", posn_measured); */
    return 1;
}

int _set_speed_rpm(unsigned long i, double speed){
	/*
	Parameters
	-------------
	speed: run to this speed
	Outputs
	-------------
	return 1: set speed successfully
	-1: did not set speed
	 */
  INode &theNode = *(pTheNode[i]);
  theNode.Motion.MoveWentDone(); //Clear the rising edge Move done register
  theNode.AccUnit(INode::RPM_PER_SEC);	//Set the units for Acceleration to RPM/SEC
  theNode.VelUnit(INode::RPM);		//Set the units for Velocity to RPM
  theNode.Motion.AccLimit = ACC_LIM_RPM_PER_SEC; //Set Acceleration Limit (RPM/Sec)
  theNode.Motion.VelLimit = VEL_LIM_RPM;	 //Set Velocity Limit (RPM)
  theNode.Motion.MoveVelStart(speed);
  double speed_mps = (speed / 60)*THREAD_PITCH;
  printf("Speed set to %lf RPM (%lf m/s)\n", speed, speed_mps);
  return 1;
}

int _set_position(unsigned long i, double pos) {
  INode &theNode = *(pTheNode[i]);
  int32_t target = (int32_t)(pos * CNTS_PER_MM * 1000);
  theNode.Motion.MoveWentDone(); //Clear the rising edge Move done register
  theNode.AccUnit(INode::RPM_PER_SEC);	//Set the units for Acceleration to RPM/SEC
  theNode.VelUnit(INode::RPM);		//Set the units for Velocity to RPM
  theNode.Motion.AccLimit = ACC_LIM_RPM_PER_SEC; //Set Acceleration Limit (RPM/Sec)
  theNode.Motion.VelLimit = VEL_LIM_RPM;	 //Set Velocity Limit (RPM)
  theNode.Motion.MovePosnStart(target, true);
  return 1;
}

int _set_position_unique(unsigned long i, double pos, double vel) {
  INode &theNode = *(pTheNode[i]);
  int32_t target = (int32_t)(pos * CNTS_PER_MM * 1000);
  int32_t velocity = vel; 
  int32_t acc = (vel *2 ) 
  theNode.Motion.MoveWentDone(); //Clear the rising edge Move done register
  theNode.AccUnit(INode::RPM_PER_SEC);	//Set the units for Acceleration to RPM/SEC
  theNode.VelUnit(INode::RPM);		//Set the units for Velocity to RPM
  theNode.Motion.AccLimit = acc ; //Set Acceleration Limit (RPM/Sec)
  theNode.Motion.VelLimit = vel;	 //Set Velocity Limit (RPM)
  theNode.Motion.MovePosnStart(target, true);
  return 1;
}


int _stop_all_motors() {
  INode &theNode = *(pTheNode[0]); //Where is there a 0 here? 
  theNode.Motion.GroupNodeStop(STOP_TYPE_ABRUPT); 
  return 1;
}

int _homing_motor(unsigned long i) { //assumption that the configuration files have been loaded 
 	INode &theNode = *(pTheNode[i]);

//  INode &theNode = myPort.Nodes(iNode); Does it matter if we use this one that was in the example or the one above?  
  
  theNode.Motion.PosnMeasured.Refresh();
  theNode.Motion.Homing.Initiate();
  theNode.Motion.PosnMeasured.Refresh();
	double measuredPosition = theNode.Motion.PosnMeasured; 
	theNode.Motion.AddToPosition(-measuredPosition); 
	theNode.Motion.PosnMeasured.Refresh();
	printf("Node %ld has already been homed, current position is: \t%8.0f \n", i, theNode.Motion.PosnMeasured.Value());
  return 1;
}

static PyObject *homing_motor(PyObject *self, PyObject *args) {
  unsigned long i;
  if (!PyArg_ParseTuple(args, "k", &i)) {
    return NULL;
  }
  
  int ret_val = _homing_motor(i);
  if (ret_val >= 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}


static PyObject *get_position(PyObject *self, PyObject *args) {
  unsigned long i;
  if (!PyArg_ParseTuple(args, "k", &i)) {
    return NULL;
  }
  return PyFloat_FromDouble(_get_position(i));
}

static PyObject *get_torque(PyObject *self, PyObject *args) {
  unsigned long i;
  if (!PyArg_ParseTuple(args, "k", &i)) {
    return NULL;
  }
  return PyFloat_FromDouble(_get_torque(i));
}



static PyObject *get_num_motors(PyObject *self, PyObject *args) {
	return PyLong_FromUnsignedLong((unsigned long)numNodesDetected);
}

static PyObject *get_motor_id(PyObject *self, PyObject *args) {
  unsigned long i;
  if (!PyArg_ParseTuple(args, "k", &i)) {
    return NULL;
  }
  if (i >= numNodesDetected) return NULL;
  INode &theNode = *(pTheNode[i]);
  return PyUnicode_FromString(theNode.Info.UserID.Value());
}

static PyObject *set_speed_rpm(PyObject *self, PyObject *args) {
  unsigned long i;
  double speed;
  if (!PyArg_ParseTuple(args, "kd", &i, &speed)) {
    return NULL;
  }
  
  int set_speed = _set_speed_rpm(i, speed);
  if (set_speed > 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}

static PyObject *stop_all_motors(PyObject *self, PyObject *args) {
  int ret_val = _stop_all_motors();
  if (ret_val >= 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}

static PyObject *motor_status(PyObject *self, PyObject *args) {
  unsigned long i;
  if (!PyArg_ParseTuple(args, "k", &i)) {
    return NULL;
  }
  
  int ret_val = _motor_status(i);
  if (ret_val >= 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}

static PyObject *set_position(PyObject *self, PyObject *args) {
  unsigned long i;
  double position;
  if (!PyArg_ParseTuple(args, "kd", &i, &position)) {
    return NULL;
  }
  
  int ret_val = _set_position(i, position);
  if (ret_val >= 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}

static PyObject *set_position_unique(PyObject *self, PyObject *args) {
  unsigned long i;
  double position;
  double vel; 
  if (!PyArg_ParseTuple(args, "kdd", &i, &position, &vel)) {
    return NULL;
  }
  
  int ret_val = _set_position_unique(i, position, vel);
  if (ret_val >= 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}

static PyObject *set_home(PyObject *self, PyObject *args) {
  unsigned long i;
  if (!PyArg_ParseTuple(args, "k", &i)) {
    return NULL;
  }
  
  int set_home = _set_home(i);
  if (set_home > 0)
    Py_RETURN_TRUE;
  else
    Py_RETURN_FALSE;
}


static PyMethodDef HydrationServo_methods[] = {
    {"get_position", get_position, METH_VARARGS, "Returns servo position"},

    {"homing_motor", homing_motor, METH_VARARGS, "Homes motor with respective limit switch"},
    {"motor_status", motor_status, METH_VARARGS, "Refreshes servo status and clears alerts"},
	{"set_position_unique", set_position_unique, METH_VARARGS, "Returns servo position for Z1 and Y1 in the F04"},
	{"set_position", set_position, METH_VARARGS, "Sets given servo to given position using MovePosnStart"},
    {"set_speed_rpm", set_speed_rpm, 
	    METH_VARARGS, "Sets servo speed"},
	{"stop_all_motors", stop_all_motors, 
	    METH_VARARGS, "Stops all motors"},
	{"get_torque", get_torque, METH_VARARGS, "Returns torque value"}, 
	{"set_home", set_home, METH_VARARGS, "Set home"},
	{"get_num_motors", get_num_motors, 
	    METH_VARARGS, "Returns the number of motors"},
	{"get_motor_id", get_motor_id, METH_VARARGS, "Returns the ID (Name) of the Motor"},
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
	for (unsigned iNode = 0; iNode < NUM_MOTORS_MAX; iNode++)
		pTheNode[iNode] = NULL;

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
				pTheNode[iNode] = &theNode; // store address to the first node

				//theNode.EnableReq(false);				//Ensure Node is disabled before starting
 				//theNode.Setup.ConfigLoad("Config File path"); //note for Eric, I do not know if two homing nodes are the same as one, note that for loop above, does that mean I'd have to do seperate cofiguration files for each of them? Must experiment at lab

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

				double timeout = myMgr.TimeStampMsec() + INIT_TIMEOUT;	//define a timeout in case the node is unable to enable
																			//This will loop checking on the Real time values of the node's Ready status
				while (!theNode.Motion.IsReady()) {
					if (myMgr.TimeStampMsec() > timeout) {
						printf("Error: Timed out waiting for Node %d to enable\n", iNode);
						msgUser("Press any key to continue."); //pause so the user can see the error message; waits for user to press a key
						return -2;
					}
				}
				numNodesDetected = iNode + 1;
				// make sure we are not assigning without allocating memory for array
				// of nodes
				if(iNode >= NUM_MOTORS_MAX) break; 
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
