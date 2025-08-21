import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# PyDevRemoteDebug
#

class PyDevRemoteDebug(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    parent.title = "Python debugger"
    parent.categories = ["Developer Tools"]
    parent.dependencies = []
    parent.contributors = ["Andras Lasso (PerkLab at Queen's University)"]
    parent.helpText = """
    This module connects to debugpy or PyDev remote debugger for debugging Python scripts in the VisualStudio, VisualStudio Code, PyCharm, or Eclipse integrated development environment.
    <a href="https://github.com/SlicerRt/SlicerDebuggingTools">More information...</a>
    """
    parent.acknowledgementText = """
    This work is part of the SparKit project, funded by An Applied Cancer Research Unit of Cancer Care Ontario with funds provided by the Ministry of Health and Long-Term Care and the Ontario Consortium for Adaptive Interventions in Radiation Oncology (OCAIRO) to provide free, open-source toolset for radiotherapy and related image-guided interventions.
    """

    self.logic = PyDevRemoteDebugLogic()
    slicer.app.connect("startupCompleted()", self.onDebuggerAutoConnect)

  def onDebuggerAutoConnect(self):
    # allow some time for all modules to initialize and then connect
    debuggerAutoConnectDelayMsec = 2000
    qt.QTimer.singleShot(debuggerAutoConnectDelayMsec, self.logic.onDebuggerAutoConnect)


#
# PyDevRemoteDebugWidget
#

class PyDevRemoteDebugWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModuleWidget.__init__(self, parent)
    self.logic = slicer.modules.PyDevRemoteDebugInstance.logic

  def setup(self):

    # Parent setup is commented out to not show reload&test in developer mode, as debugger is mostly used by developers
    # but they are not interested in debugging this module.
    # ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    # Settings Area
    self.settingsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.settingsCollapsibleButton.text = "Settings"
    self.settingsCollapsibleButton.collapsed = True
    self.layout.addWidget(self.settingsCollapsibleButton)
    settingsFormLayout = qt.QFormLayout(self.settingsCollapsibleButton)

    # Debugger selector
    self.debuggerSelector = qt.QComboBox()
    self.debuggerSelector.toolTip = "Choose debugger."
    self.debuggerSelector.addItem("PyCharm")
    self.debuggerSelector.addItem("VisualStudio Code")
    self.debuggerSelector.addItem("VisualStudio")
    self.debuggerSelector.addItem("Eclipse")
    settingsFormLayout.addRow("Debugger: ", self.debuggerSelector)
    self.debuggerSelector.connect('currentIndexChanged(int)', self.onDebuggerSelected)

    # pydevd.py path selector
    self.pydevdDirSelector = ctk.ctkPathLineEdit()
    self.pydevdDirSelector.filters = self.pydevdDirSelector.Dirs
    self.pydevdDirSelector.setMaximumWidth(300)
    self.pydevdDirSelector.setToolTip("Set the path to pydevd.py. It is in the eclipse folder within plugins/...pydev.../pysrc.")
    self.pydevdDirLabel = qt.QLabel("Eclipse pydevd.py directory:")
    settingsFormLayout.addRow(self.pydevdDirLabel, self.pydevdDirSelector)

    # pycharm-debug.egg path selector
    self.pyCharmDebugEggPathSelector = ctk.ctkPathLineEdit()
    self.pyCharmDebugEggPathSelector.nameFilters=['pydevd-pycharm.egg', 'pycharm-debug.egg']
    self.pyCharmDebugEggPathSelector.setMaximumWidth(300)
    self.pyCharmDebugEggPathSelector.setToolTip("Set the path to pydevd-pycharm.egg or pycharm-debug.egg . It is in the .../PyCharm/debug-eggs folder.")
    self.pyCharmDebugEggPathLabel = qt.QLabel("PyCharm debug egg path:")
    settingsFormLayout.addRow(self.pyCharmDebugEggPathLabel, self.pyCharmDebugEggPathSelector)

    # port number
    self.portInputSpinBox = qt.QSpinBox()
    self.portInputSpinBox.minimum = 0
    self.portInputSpinBox.maximum = 65535
    self.portInputLabel = qt.QLabel("Port:")
    settingsFormLayout.addRow(self.portInputLabel, self.portInputSpinBox)

    # Connection Area
    connectionCollapsibleButton = ctk.ctkCollapsibleButton()
    connectionCollapsibleButton.text = "Connection"
    connectionCollapsibleButton.collapsed = False
    self.layout.addWidget(connectionCollapsibleButton)
    connectionFormLayout = qt.QFormLayout(connectionCollapsibleButton)

    # Connect Button
    self.connectButton = qt.QPushButton("Connect to debug server")
    self.connectButton.toolTip = "Connect to remote debug server"
    self.connectButton.setAutoFillBackground(True)
    self.connectButton.setStyleSheet("background-color: rgb(150, 255, 150); color: rgb(0, 0, 0)")
    connectionFormLayout.addRow(self.connectButton)

    # Auto-connect button (only show after a successful connection to make sure
    # Slicer does not hang on startup due to failed attempt to connect to debugger)
    self.autoConnectCheckBox = qt.QCheckBox()
    self.autoConnectCheckBox.visible = False
    self.autoConnectCheckBox.checked = self.logic.getDebuggerAutoConnect()
    self.autoConnectCheckBox.setToolTip("If checked, Slicer will attempt to connect to the remote debugger on startup.")
    self.autoConnectCheckBoxLabel = qt.QLabel("Auto-connect on next application startup:")
    self.autoConnectCheckBoxLabel.visible = False
    connectionFormLayout.addRow(self.autoConnectCheckBoxLabel, self.autoConnectCheckBox)

    self.updateGUIFromLogic()

    if not self.isCurrentSettingValid():
      self.settingsCollapsibleButton.collapsed = False

    # Connections
    self.connectButton.connect('clicked(bool)', self.onConnect)
    self.autoConnectCheckBox.connect('toggled(bool)', self.onAutoConnectChanged)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def updateGUIFromLogic(self):

    debugger = self.logic.getDebugger()

    wasBlocked = self.debuggerSelector.blockSignals(True)
    self.debuggerSelector.setCurrentText(debugger)
    self.debuggerSelector.blockSignals(wasBlocked)

    pydevdDir = self.logic.getEclipsePydevdDir(enableAutoDetect = (debugger=='Eclipse') )
    self.pydevdDirSelector.setCurrentPath(pydevdDir)

    portNumber=self.logic.getPortNumber()
    self.portInputSpinBox.setValue(int(portNumber))

    pyCharmDebugEggPath=self.logic.getPyCharmDebugEggPath(enableAutoDetect=(debugger=='PyCharm'))
    self.pyCharmDebugEggPathSelector.setCurrentPath(pyCharmDebugEggPath)

    connected = self.logic.isConnected()
    self.connectButton.text = "Connected to debug server" if connected else "Connect to debug server"
    self.autoConnectCheckBox.visible = connected
    self.autoConnectCheckBoxLabel.visible = connected
    if debugger == 'Eclipse':
      if not connected:
        self.connectButton.text = "Connect to Eclipse debugger"
        self.connectButton.toolTip = "Connect to PyDev remote debug server"
      # Auto-detect path
      if not self.pydevdDirSelector.currentPath:
        pydevdDir=self.logic.getEclipsePydevdDir(enableAutoDetect=True)
        if pydevdDir:
          self.pydevdDirSelector.setCurrentPath(pydevdDir)
    elif debugger=='PyCharm':
      if not connected:
        self.connectButton.text = "Connect to PyCharm debugger"
        self.connectButton.toolTip = "Connect to PyCharm remote debug server"
      # Auto-detect path
      if not self.pyCharmDebugEggPathSelector.currentPath:
        eggDir=self.logic.getPyCharmDebugEggPath(enableAutoDetect=True)
        if eggDir:
          self.pyCharmDebugEggPathSelector.setCurrentPath(eggDir)
    elif debugger=='VisualStudio':
      if not connected:
        self.connectButton.text = "Connect to VisualStudio debugger"
        self.connectButton.toolTip = "Connect to VisualStudio Python debugger (using debugpy)."
    elif debugger=='VisualStudio Code':
      if not connected:
        self.connectButton.text = "Connect to VisualStudio Code debugger"
        self.connectButton.toolTip = "Connect to VisualStudio Code Python remote debugger (using debugpy)."

    self.pydevdDirSelector.visible = (debugger=="Eclipse")
    self.pydevdDirLabel.visible = (debugger=="Eclipse")
    self.pyCharmDebugEggPathSelector.visible = (debugger=="PyCharm")
    self.pyCharmDebugEggPathLabel.visible = (debugger=="PyCharm")

  def onDebuggerSelected(self):
    self.logic.setDebugger(self.debuggerSelector.currentText)
    self.updateGUIFromLogic()

  def isCurrentSettingValid(self):
    if not self.logic.getDebugger():
      return False
    if self.logic.getDebugger()=="Eclipse" and self.logic.isValidPydevdDir(self.pydevdDirSelector.currentPath):
      return True
    if self.logic.getDebugger()=="PyCharm" and self.logic.isValidPyCharmDebugEggPath(self.pyCharmDebugEggPathSelector.currentPath):
      return True
    if self.logic.isDebuggerDebugpy():
      return True
    return False

  def onAutoConnectChanged(self, enabled):
    self.logic.setDebuggerAutoConnect(enabled)

  def onConnect(self):

    debugger = self.logic.getDebugger()
    isDebugpy = self.logic.isDebuggerDebugpy()
    if debugger=='Eclipse':
      pydevdDir=self.pydevdDirSelector.currentPath
      # Verify path
      if not self.logic.isValidPydevdDir(pydevdDir):
        qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyDev", 'Please set the correct path to pydevd.py in the settings panel')
        self.settingsCollapsibleButton.collapsed = False
        return
      self.logic.setPydevdDir(pydevdDir)
    elif debugger=='PyCharm':
      pydevdDir=self.pyCharmDebugEggPathSelector.currentPath
      # Verify path
      if not self.logic.isValidPyCharmDebugEggPath(pydevdDir):
        qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyCharm", 'Please set the correct path to PyCharm debug egg file in the settings panel')
        self.settingsCollapsibleButton.collapsed = False
        return
      self.logic.setPyCharmDebugEggPath(pydevdDir)
    elif isDebugpy:
      # there is nothing specific to save
      pass
    else:
      # No debugger is selected
      qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to Python remote debug server", 'Please select a debugger in the settings panel')
      self.settingsCollapsibleButton.collapsed = False
      return

    portNumber = self.portInputSpinBox.value
    self.logic.setPortNumber(portNumber)

    self.connectButton.enabled = False
    try:
      with slicer.util.tryWithErrorDisplay("Failed to connect to debugger.", waitCursor=True):
        self.logic.connect()
    finally:
      self.connectButton.enabled = True
      self.updateGUIFromLogic()


#
# PyDevRemoteDebugLogic
#

class PyDevRemoteDebugLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    ScriptedLoadableModuleLogic.__init__(self)

    self.enableDebuggerAutoConnectAfterSuccessfulConnection = False

  def onDebuggerAutoConnect(self):
    if not self.getDebuggerAutoConnect():
      # auto-connect is disabled
      return
    if self.isConnected():
      # already connected
      return
    logging.debug("Auto-connect to Python remote debug server")
    # Disable auto-connect to prevent hanging Slicer on every startup in case there is no debugger available anymore
    self.enableDebuggerAutoConnectAfterSuccessfulConnection = True
    self.setDebuggerAutoConnect(False)
    self.connect()
    logging.debug("Auto-connect to Python remote debug server completed")

  def getDebuggerAutoConnect(self):
    settings = qt.QSettings()
    if settings.contains('Developer/PythonRemoteDebugAutoConnect'):
      return settings.value('Developer/PythonRemoteDebugAutoConnect').lower() == 'true'
    return False

  def setDebuggerAutoConnect(self, autoConnect):
    # don't save it if already saved
    settings = qt.QSettings()
    if self.getDebuggerAutoConnect()==autoConnect:
      return
    settings.setValue('Developer/PythonRemoteDebugAutoConnect','true' if autoConnect else 'false')

  def getDebugger(self):
    settings = qt.QSettings()
    if settings.contains('Developer/PythonRemoteDebugServer'):
      debugger = settings.value('Developer/PythonRemoteDebugServer')
      if (debugger=="Eclipse" or debugger=="PyCharm"
        or debugger=='VisualStudio 2013/2015'
        or debugger=='VisualStudio 2017' or debugger=='VisualStudio Code'
        or debugger=="VisualStudio" or debugger=='VisualStudio 2019/2022'):
        return debugger
    return ''

  def isDebuggerDebugpy(self):
    debugger = self.getDebugger()
    return (debugger == "VisualStudio" or debugger == "VisualStudio 2019/2022" or debugger == "VisualStudio Code")

  def getPortNumber(self):
    if self.isDebuggerDebugpy():
      settingsKeyPrefix = 'Developer/VisualStudio'
    else:
      settingsKeyPrefix = 'Developer/Pydevd'
    settings = qt.QSettings()
    if settings.contains(settingsKeyPrefix+'PortNumber'):
      port = settings.value(settingsKeyPrefix+'PortNumber')
      return int(port)
    return 5678

  def setDebugger(self, debugger):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains('Developer/PythonRemoteDebugServer'):
      debuggerSaved = settings.value('Developer/PythonRemoteDebugServer')
      if debuggerSaved == debugger:
        return
    settings.setValue('Developer/PythonRemoteDebugServer', debugger)

  def isValidPydevdDir(self, pydevdDir):
    import os.path
    pydevdPath=pydevdDir+'/pydevd.py'
    return os.path.isfile(pydevdPath)

  def findFileInSubdirectory(self, pattern, root=os.curdir):
    """Find file in a subdirectory tree. Returns the first occurrence."""
    import os, fnmatch
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            return os.path.join(path, filename)
    return None

  def getEclipsePydevdDir(self, enableAutoDetect = False):
    settings = qt.QSettings()
    if settings.contains('Developer/EclipsePyDevDir'):
      pydevdDir = settings.value('Developer/EclipsePyDevDir')
      if self.isValidPydevdDir(pydevdDir):
        # found a good value in the settings
        return pydevdDir

    if not enableAutoDetect:
      return ''

    # Auto-detect
    import platform
    if platform.system() == 'Windows':
      pydevdPath = self.findFileInSubdirectory('pydevd.py','c:/Program Files/Brainwy')
      if pydevdPath:
        import os.path
        pydevdDir = os.path.dirname(pydevdPath)
        if self.isValidPydevdDir(pydevdDir):
          return pydevdDir

    # not found
    return ''

  def setPydevdDir(self, pydevdDir):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains('Developer/EclipsePyDevDir'):
      pydevdDirSaved = settings.value('Developer/EclipsePyDevDir')
      if pydevdDirSaved == pydevdDir:
        return
    settings.setValue('Developer/EclipsePyDevDir',pydevdDir)

  def setPyCharmDebugEggPath(self, pydevdDir):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains('Developer/PyCharmDebugEggPath'):
      pydevdDirSaved = settings.value('Developer/PyCharmDebugEggPath')
      if pydevdDirSaved == pydevdDir:
        return
    settings.setValue('Developer/PyCharmDebugEggPath',pydevdDir)

  def setPortNumber(self, portNumber):
    if self.isDebuggerDebugpy():
      settingsKeyPrefix = 'Developer/VisualStudio'
    else:
      settingsKeyPrefix = 'Developer/Pydevd'
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains(settingsKeyPrefix+'PortNumber'):
      portNumberSaved = settings.value(settingsKeyPrefix+'PortNumber')
      if portNumberSaved == portNumber:
        return
    settings.setValue(settingsKeyPrefix+'PortNumber',portNumber)

  def isValidPyCharmDebugEggPath(self, pyCharmDebugEggPath):
    import os.path
    # Check if file
    if not os.path.isfile(pyCharmDebugEggPath):
      return False
    # Check if extension is .egg
    [fn, ext] = os.path.splitext(pyCharmDebugEggPath)
    if ext != ".egg":
      return False
    return True

  def getPyCharmDebugEggPath(self, enableAutoDetect = False):

    # If path is defined in settings then use that
    settings = qt.QSettings()
    if settings.contains('Developer/PyCharmDebugEggPath'):
      pyCharmDebugEggPath = settings.value('Developer/PyCharmDebugEggPath')
      if self.isValidPyCharmDebugEggPath(pyCharmDebugEggPath):
        # found a good value in the settings
        return pyCharmDebugEggPath

    if not enableAutoDetect:
      return ''

    # Auto-detect
    import platform
    if platform.system() == 'Windows':
      try:
        # Python2
        import _winreg as winreg
      except ImportError:
        # Python3
        import winreg

      value = None
      pycharmExeKeys = [r"Applications\pycharm.exe\shell\open\command", r"Applications\pycharm64.exe\shell\open\command"]
      for pycharmExeKey in pycharmExeKeys:
        try:
          aReg = winreg.ConnectRegistry(None,winreg.HKEY_CLASSES_ROOT)
          aKey = winreg.OpenKey(aReg, pycharmExeKey)
          value = winreg.QueryValue(aKey, None)
          if value:
            # found a non-empty value
            break
        except:
          # not found
          pass
      if not value:
        # PyCharm not found in registry
        return ''
      logging.debug("PyCharm was found in registry: "+value)

      # Get PyCharm path by removing bin\pycharm... and anything beyond that
      # from value variable, which initially contains something like:
      # 'C:\Program Files (x86)\JetBrains\PyCharm 4.5.4\bin\pycharm.exe "%1"'
      pyCharmPath = value[:value.find(r"\bin\pycharm.exe")]
      pyCharmPath = value[:value.find(r"\bin\pycharm64.exe")]
      # remove leading " character if present
      if pyCharmPath[0] == "\"":
        pyCharmPath = pyCharmPath[1:]
      pyCharmDebugEggPath = pyCharmPath+r"\debug-eggs\pycharm-debug.egg" # PyCharm version of 2018 or older
      if self.isValidPyCharmDebugEggPath(pyCharmDebugEggPath):
        # found a good value in registry
        return pyCharmDebugEggPath
      pyCharmDebugEggPath = pyCharmPath+r"\debug-eggs\pydevd-pycharm.egg"
      if self.isValidPyCharmDebugEggPath(pyCharmDebugEggPath):
        # found a good value in registry
        return pyCharmDebugEggPath

    # Not found
    return ''

  def getPydevdPath(self):
    debugger = self.getDebugger()
    if debugger=='Eclipse':
      return self.getEclipsePydevdDir()
    elif debugger=='PyCharm':
      return self.getPyCharmDebugEggPath()
    else:
      return ''

  def updatePydevdPath(self):
    import sys
    pydevdPath = self.getPydevdPath()
    if not pydevdPath:
      return False
    if sys.path[0]!=pydevdPath:
      sys.path.insert(0,pydevdPath)
    return True

  def isConnected(self):
    if self.isDebuggerDebugpy():
      try:
        import debugpy
      except ImportError:
        slicer.util.pip_install('debugpy')
      try:
        import debugpy
      except ImportError:
        return False
      return debugpy.is_client_connected()
    else:
      if not self.updatePydevdPath():
        return False

      imported = False
      if not imported:
        try:
          # More recent pycharm versions (e.g., 2024.3)
          import pydevd_pycharm as pydevd
          imported = True
        except ImportError:
          pass
      if not imported:
        try:
          # Older pycharm versions (e.g., 2019.1.2)
          import pydevd
          imported = True
        except ImportError:
          pass
      if not imported:
        return False

      # return attribute depending on which version of pydevd.py is being used
      if hasattr(pydevd, '_debugger_setup'):
        return pydevd._debugger_setup     # updated PyDev
      elif hasattr(pydevd, 'connected'):
        return pydevd.connected           # older version
      else:
        return False

  def connect(self):

    # Refuse to connect if already connected
    if self.isConnected():
      raise RuntimeError("You are already connected to the remote debugger. If the connection is broken (e.g., because the server terminated the connection) then you need to restart Slicer to be able to connect again.")

    # Show a dialog that explains that Slicer will hang
    infoDlg = qt.QDialog()
    infoDlg.setModal(False)
    infoLayout = qt.QVBoxLayout()
    infoDlg.setLayout(infoLayout)
    if self.getDebugger()=="VisualStudio":
      connectionHelp = ("Waiting for VisualStudio debugger attachment...\n\n"
        + "To attach debugger:\n"
        + "- In VisualStudio, open menu: Debug / Attach to process\n"
        + "- Select 'Attach to' -> 'Python code'\n"
        + "- Set 'Process' -> 'SlicerApp-real.exe'\n"
        + "- Click Attach")
    elif self.getDebugger()=="VisualStudio Code":
      connectionHelp = ("Waiting for VisualStudio Code debugger attachment...\n\n"
        + "Make sure you have configured `Python: Attach` debugging configuration like this:\n"
        + '\n'
        + '  {\n'
        + '    "name": "Python: Attach",\n'
        + '    "type": "python",\n'
        + '    "request": "attach",\n'
        +f'    "port": {self.getPortNumber()}\n'
        + '    "host": "localhost"\n'
        + '  }\n'
        + '\n'
        + "To attach debugger:\n"
        + "- In VisualStudio Code, choose debugging configuration 'Python: Attach'\n"
        + "- Click Start Debugging")
    else:  # pydevd
      connectionHelp = f"Connecting to remote debug server at port {self.getPortNumber()}...\nSlicer is paused until {self.getDebugger()} accepts the connection."

    label = qt.QLabel(connectionHelp)
    label.setParent(slicer.util.mainWindow())
    infoLayout.addWidget(label)
    infoDlg.show()
    infoDlg.repaint()
    slicer.app.processEvents()

    # Connect to the debugger

    try:
      if self.isDebuggerDebugpy():
        # Visual Studio or Visual Studio Code

        try:
          import debugpy
        except ImportError:
          # Using 3DSlicer on Windows (5.9.0-2025-08-17-win-amd64) VS Code could not connect using debugpy==1.8.16
          slicer.util.pip_install('debugpy!=1.8.16')
        try:
          import debugpy
        except ImportError:
          raise RuntimeError("Failed to import debugpy import failed.")

        if self.getDebugger() == "VisualStudio Code":
          debugpy.listen(self.getPortNumber())
          debugpy.wait_for_client()

        else:
          # Visual Studio does not work with `wait_for_client()`
          import time
          connected = False
          for i in range(240):
              time.sleep(0.5)
              slicer.app.processEvents(qt.QEventLoop.ExcludeUserInputEvents)
              if debugpy.is_client_connected():
                  connected = True
                  break
          if not connected:
            raise RuntimeError("Timeout while waiting for debugger client to connect.")

      else:
        # pydevd
        try:
          import pydevd
          pydevd.settrace('localhost', port=self.getPortNumber(), stdoutToServer=True, stderrToServer=True, suspend=False)
        except (Exception, SystemExit) as e:
          infoDlg.hide()
          import traceback
          traceback.print_exc()
          raise RuntimeError("An error occurred while trying to connect to PyDev remote debugger. Make sure pydev server is started.")

      logging.debug("Connected to remote debug server")

    finally:
      infoDlg.hide()

      if self.isConnected():
        # successful connection
        if self.enableDebuggerAutoConnectAfterSuccessfulConnection:
          self.setDebuggerAutoConnect(True)
          self.enableDebuggerAutoConnectAfterSuccessfulConnection = False

class PyDevRemoteDebugTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_PyDevRemoteDebug1()

  def test_PyDevRemoteDebug1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Just call a few basic methods that don't change any settings
    logic = PyDevRemoteDebugLogic()
    logic.getDebuggerAutoConnect()
    logic.getDebugger()
    logic.getEclipsePydevdDir()
    logic.getPyCharmDebugEggPath()
    logic.getPydevdPath()
    logic.getPortNumber()
    logic.updatePydevdPath()
    logic.isConnected()

    self.delayDisplay('Test passed!')
