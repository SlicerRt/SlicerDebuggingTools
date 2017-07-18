#-----------------------------------------------------------------------------
set(MODULE_NAME PyDevRemoteDebug)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  )

set(MODULE_PYTHON_RESOURCES
  ptvsd/__init__.py
  ptvsd/__main__.py
  ptvsd/attach_server.py
  ptvsd/visualstudio_py_debugger.py
  ptvsd/visualstudio_py_repl.py
  ptvsd/visualstudio_py_util.py 
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )
