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

PyMODINIT_FUNC PyInit_HydrationServo(void) {
  Py_Initialize();
  PyObject *m = PyModule_Create(&HydrationServo_definition);

  return m;
}
