#include <Python.h>

static PyMethodDef example_methods[] = {
    {"pants", pants, METH_VARARGS, "Returns a square of an integer."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef example_definition = {
    PyModuleDef_HEAD_INIT,
    "example",
    "A Python module containing Classy type and pants() function",
    -1,
    example_methods
};

PyMODINIT_FUNC PyInit_example(void) {
  Py_Initialize();
  PyObject *m = PyModule_Create(&example_definition);

  return m;
}