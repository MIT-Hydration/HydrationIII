#include <Python.h>
#include <stdio.h>		
#include <iostream>
#include "pubSysCls.h"	

using namespace sFnd;

static PyMethodDef HydrationServo_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef HydrationServo_definition = {
    PyModuleDef_HEAD_INIT,
    "HydrationServo",
    "A Python module to control Hydration Clear Path Servos",
    -1,
    HydrationServo_methods
};

void connect_clearpath(void) {
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
        -------------------------------*/
}

PyMODINIT_FUNC PyInit_HydrationServo(void) {
  Py_Initialize();
  PyObject *m = PyModule_Create(&HydrationServo_definition);

  connect_clearpath();

  return m;
}
