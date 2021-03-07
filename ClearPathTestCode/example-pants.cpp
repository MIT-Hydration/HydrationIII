#include <Python.h>

PyMODINIT_FUNC PyInit_example(void) {
  Py_Initialize();
  PyObject *m = PyModule_Create(&example_definition);

  return m;
}