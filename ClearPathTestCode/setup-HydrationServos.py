from distutils.core import setup, Extension

HydrationServo_module = Extension(
    'HydrationServo',
    sources=['HydrationServo.cpp'],
    language='C++', )

setup(
    name='HydrationServo',
    version='0.1.0',
    description='Hydration Servo module written in C++',
    ext_modules=[HydrationServo_module], )