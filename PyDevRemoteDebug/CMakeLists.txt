#-----------------------------------------------------------------------------
set(MODULE_NAME PyDevRemoteDebug)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  )

set(MODULE_PYTHON_RESOURCES
  ptvsd-2.2.2/ptvsd/__init__.py
  ptvsd-2.2.2/ptvsd/__main__.py
  ptvsd-2.2.2/ptvsd/attach_server.py
  ptvsd-2.2.2/ptvsd/visualstudio_py_debugger.py
  ptvsd-2.2.2/ptvsd/visualstudio_py_repl.py
  ptvsd-2.2.2/ptvsd/visualstudio_py_util.py
  ptvsd-3.0.0/ptvsd/__init__.py
  ptvsd-3.0.0/ptvsd/__main__.py
  ptvsd-3.0.0/ptvsd/attach_server.py
  ptvsd-3.0.0/ptvsd/visualstudio_py_debugger.py
  ptvsd-3.0.0/ptvsd/visualstudio_py_launcher.py
  ptvsd-3.0.0/ptvsd/visualstudio_py_repl.py
  ptvsd-3.0.0/ptvsd/visualstudio_py_util.py
  ptvsd-3.2.1/ptvsd/__init__.py
  ptvsd-3.2.1/ptvsd/__main__.py
  ptvsd-3.2.1/ptvsd/attach_server.py
  ptvsd-3.2.1/ptvsd/debugger.py
  ptvsd-3.2.1/ptvsd/ipcjson.py
  ptvsd-3.2.1/ptvsd/util.py
  ptvsd-3.2.1/ptvsd/repl/__init__.py
  ptvsd-3.2.1/ptvsd/repl/ipython.py
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )
