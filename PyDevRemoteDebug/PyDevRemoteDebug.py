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
    This module connects to PyDev remote debugger for running Python scripts in the Eclipse integrated development environment.
    <a href="http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/DebuggingTools">More information...</a>
    """
    parent.acknowledgementText = """
    This work is part of the SparKit project, funded by An Applied Cancer Research Unit of Cancer Care Ontario with funds provided by the Ministry of Health and Long-Term Care and the Ontario Consortium for Adaptive Interventions in Radiation Oncology (OCAIRO) to provide free, open-source toolset for radiotherapy and related image-guided interventions.
    """

    self.logic = PyDevRemoteDebugLogic()

#
# PyDevRemoteDebugWidget
#

class PyDevRemoteDebugWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModuleWidget.__init__(self, parent)

    #if 'PyDevRemoteDebugLogic' in vars(slicer):
    #  self.logic = PyDevRemoteDebugLogic()
    #else
    #  self.logic = slicer.PyDevRemoteDebugLogic

    # If user switches quickly to the module widget then the logic may not have been created yet
    #if not slicer.modules.PyDevRemoteDebugInstance.logic:
    #  slicer.modules.PyDevRemoteDebugInstance.logic = PyDevRemoteDebugLogic()
    self.logic = slicer.modules.PyDevRemoteDebugInstance.logic

  def setup(self):

    # Do not show reload&test in developer mode, as debugger is mostly used by developers
    # but they are not interested in debugging this module.
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...


    # Settings Area
    self.settingsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.settingsCollapsibleButton.text = "Settings"
    self.settingsCollapsibleButton.collapsed = True
    self.layout.addWidget(self.settingsCollapsibleButton)
    settingsFormLayout = qt.QFormLayout(self.settingsCollapsibleButton)
    
    # Debugger selector
    self.debuggerSelector = qt.QComboBox()
    self.debuggerSelector.toolTip = "Chose debugger server."
    debugger = self.logic.getDebugger()
    self.debuggerSelector.addItem("Eclipse")
    self.debuggerSelector.addItem("PyCharm")
    if debugger=='Eclipse':
      self.debuggerSelector.currentIndex = 0
    elif debugger=='PyCharm':
      self.debuggerSelector.currentIndex = 1
    else:
      self.debuggerSelector.currentIndex = -1
    settingsFormLayout.addRow("Debugger: ", self.debuggerSelector)
    self.debuggerSelector.connect('currentIndexChanged(int)', self.onDebuggerSelected)
    
    # pydevd.py path selector
    pydevdDir=self.logic.getEclipsePydevdDir(enableAutoDetect=(debugger=='Eclipse'))
    self.pydevdDirSelector = ctk.ctkPathLineEdit()
    self.pydevdDirSelector.setCurrentPath(pydevdDir)
    self.pydevdDirSelector.filters=self.pydevdDirSelector.Dirs
    self.pydevdDirSelector.setMaximumWidth(300)
    self.pydevdDirSelector.setToolTip("Set the path to pydevd.py. It is in the eclipse folder within plugins/...pydev.../pysrc.")
    settingsFormLayout.addRow("Eclipse pydevd.py directory:", self.pydevdDirSelector)

    # pycharm-debug.egg path selector
    pyCharmDebugEggPathSelector=self.logic.getPyCharmDebugEggPath(enableAutoDetect=(debugger=='PyCharm'))
    self.pyCharmDebugEggPathSelector = ctk.ctkPathLineEdit()
    self.pyCharmDebugEggPathSelector.setCurrentPath(pyCharmDebugEggPathSelector)
    self.pyCharmDebugEggPathSelector.nameFilters=['pycharm-debug.egg']
    self.pyCharmDebugEggPathSelector.setMaximumWidth(300)
    self.pyCharmDebugEggPathSelector.setToolTip("Set the path to pycharm-debug.egg . It is in the .../PyCharm/debug-eggs folder.")
    settingsFormLayout.addRow("PyCharm pycharm-debug.egg path:", self.pyCharmDebugEggPathSelector)

    if not self.isCurrentSettingValid():
      self.settingsCollapsibleButton.collapsed = False
    
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

    if self.logic.isConnected():
      # already connected
      self.onConnectionComplete(True)
    
    # Connections
    self.connectButton.connect('clicked(bool)', self.onConnect)
    self.autoConnectCheckBox.connect('toggled(bool)', self.onAutoConnectChanged)

    # Add vertical spacer
    self.layout.addStretch(1)
    
    self.onDebuggerSelected()

  def cleanup(self):
    pass

  def onDebuggerSelected(self):
  
    self.logic.saveDebugger(self.debuggerSelector.currentText)

    connected = self.logic.isConnected()

    if self.debuggerSelector.currentText=='Eclipse':
      if not connected:
        self.connectButton.text = "Connect to Eclipse debugger"
        self.connectButton.toolTip = "Connect to PyDev remote debug server"
      self.pydevdDirSelector.enabled = True
      self.pyCharmDebugEggPathSelector.enabled = False
      # Auto-detect path
      if not self.pydevdDirSelector.currentPath:
        pydevdDir=self.logic.getEclipsePydevdDir(enableAutoDetect=True)
        if pydevdDir:
          self.pydevdDirSelector.setCurrentPath(pydevdDir)
    elif self.debuggerSelector.currentText=='PyCharm':
      if not connected:
        self.connectButton.text = "Connect to PyCharm debugger"
        self.connectButton.toolTip = "Connect to PyCharm remote debug server"
      self.pydevdDirSelector.enabled = False
      self.pyCharmDebugEggPathSelector.enabled = True
      # Auto-detect path
      if not self.pyCharmDebugEggPathSelector.currentPath:
        eggDir=self.logic.getPyCharmDebugEggPath(enableAutoDetect=True)
        if eggDir:
          self.pyCharmDebugEggPathSelector.setCurrentPath(eggDir)
    else:
      self.pydevdDirSelector.enabled = False
      self.pyCharmDebugEggPathSelector.enabled = False

  def isCurrentSettingValid(self):
    if not self.logic.getDebugger():
      return False
    if self.logic.getDebugger()=="Eclipse" and self.logic.isValidPydevdDir(self.pydevdDirSelector.currentPath):
      return True
    if self.logic.getDebugger()=="PyCharm" and self.logic.isValidPyCharmDebugEggPath(self.pyCharmDebugEggPathSelector.currentPath):
      return True
    return False

  def onAutoConnectChanged(self, enabled):
    self.logic.saveDebuggerAutoConnect(enabled)

  def onConnect(self):

    debugger = self.debuggerSelector.currentText
    if debugger=='Eclipse':
      pydevdDir=self.pydevdDirSelector.currentPath
      # Verify path
      if not self.logic.isValidPydevdDir(pydevdDir):
        qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyDev", 'Please set the correct path to pydevd.py in the settings panel')
        self.settingsCollapsibleButton.collapsed = False
        return
      self.logic.savePydevdDir(pydevdDir)
    elif debugger=='PyCharm':
      pydevdDir=self.pyCharmDebugEggPathSelector.currentPath
      # Verify path
      if not self.logic.isValidPyCharmDebugEggPath(pydevdDir):
        qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyCharm", 'Please set the correct path to PyCharm debug egg file in the settings panel')
        self.settingsCollapsibleButton.collapsed = False
        return
      self.logic.savePyCharmDebugEggPath(pydevdDir)
    else:
      qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to Python remote debug server", 'Please select a debugger in the settings panel')
      self.settingsCollapsibleButton.collapsed = False
      return

    self.logic.connectionCompleteCallback = self.onConnectionComplete
    self.logic.connect()

  def onConnectionComplete(self, connected):
    if connected:
      self.connectButton.text = "Connected to debug server"
      self.autoConnectCheckBox.visible = True
      self.autoConnectCheckBoxLabel.visible = True
    else:
      self.connectButton.text = "Connect to debug server"

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

    self.portNumber = 5678

    # This function is called when connection request is completed. It takes a single bool argument,
    # which is set to True if the connection is established.
    self.connectionCompleteCallback = None

    self.enableDebuggerAutoConnectAfterSuccessfulConnection = False

    # allow some time for all modules to initialize and then connect
    debuggerAutoConnectDelayMsec = 3000
    qt.QTimer.singleShot(debuggerAutoConnectDelayMsec, self.onDebuggerAutoConnect)

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
    self.saveDebuggerAutoConnect(False)
    self.connect()
    logging.debug("Auto-connect to Python remote debug server completed")

  def getDebuggerAutoConnect(self):
    settings = qt.QSettings()
    if settings.contains('Developer/PythonRemoteDebugAutoConnect'):
      return settings.value('Developer/PythonRemoteDebugAutoConnect').lower() == 'true'
    return False

  def saveDebuggerAutoConnect(self, autoConnect):
    # don't save it if already saved
    settings = qt.QSettings()
    if self.getDebuggerAutoConnect()==autoConnect:
      return
    settings.setValue('Developer/PythonRemoteDebugAutoConnect',autoConnect)

  def getDebugger(self):
    settings = qt.QSettings()
    if settings.contains('Developer/PythonRemoteDebugServer'):
      debugger = settings.value('Developer/PythonRemoteDebugServer')
      if debugger=="Eclipse" or debugger=="PyCharm":
        return debugger
    return ''

  def saveDebugger(self, debugger):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains('Developer/PythonRemoteDebugServer'):
      debuggerSaved = settings.value('Developer/PythonRemoteDebugServer')
      if debuggerSaved == debugger:
        return
    settings.setValue('Developer/PythonRemoteDebugServer',debugger)

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

  def savePydevdDir(self, pydevdDir):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains('Developer/EclipsePyDevDir'):
      pydevdDirSaved = settings.value('Developer/EclipsePyDevDir')
      if pydevdDirSaved == pydevdDir:
        return
    settings.setValue('Developer/EclipsePyDevDir',pydevdDir)

  def savePyCharmDebugEggPath(self, pydevdDir):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains('Developer/PyCharmDebugEggPath'):
      pydevdDirSaved = settings.value('Developer/PyCharmDebugEggPath')
      if pydevdDirSaved == pydevdDir:
        return
    settings.setValue('Developer/PyCharmDebugEggPath',pydevdDir)

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
      import _winreg
      aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_CLASSES_ROOT)
      aKey = _winreg.OpenKey(aReg, r"Applications\pycharm.exe\shell\open\command")
      value = _winreg.QueryValue(aKey, None) # something like: 'C:\Program Files (x86)\JetBrains\PyCharm 4.5.4\bin\pycharm.exe "%1"'
      if not value:
        # PyCharm not found in registry
        return ''
      # remove bin\pycharm and anything after that
      pyCharmPath = value[:value.find("bin\pycharm.exe")]
      pyCharmDebugEggPath = pyCharmPath+"\\debug-eggs\\pycharm-debug.egg"
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
    if not self.updatePydevdPath():
      return False
    try:
      import pydevd
    except ImportError:
      return False
    return pydevd.connected

  def connect(self):

    self.updatePydevdPath()
    import pydevd

    # Return if already connected
    if pydevd.connected:
      qt.QMessageBox.warning(slicer.util.mainWindow(),
      "Connect to PyDev remote debug server", 'You are already connected to the remote debugger. If the connection is broken (e.g., because the server terminated the connection) then you need to restart Slicer to be able to connect again.')
      return

    # Show a dialog that explains that Slicer will hang
    self.info = qt.QDialog()
    self.info.setModal(False)
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel("Connecting to remote debug server at port {0}...\nSlicer is paused until {1} accepts the connection.".format(self.portNumber,self.getDebugger()),self.info)
    self.infoLayout.addWidget(self.label)
    self.info.show()
    self.info.repaint()
    qt.QTimer.singleShot(2000, self.onConnectionComplete)

    # Connect to the debugger
    try:
      pydevd.settrace('localhost', port=self.portNumber, stdoutToServer=True, stderrToServer=True, suspend=False)
    except Exception, e:
      self.info.hide()
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyDev remote debug server", 'An error occurred while trying to connect to PyDev remote debugger. Make sure he pydev server is started.\n\n' + str(e))
      if self.connectionCompleteCallback:
        self.connectionCompleteCallback(False)
      return

    logging.debug("Connected to remote debug server")

  def onConnectionComplete(self):
    import pydevd
    self.info.hide()
    if pydevd.connected:
      # successful connection
      if self.enableDebuggerAutoConnectAfterSuccessfulConnection:
        self.saveDebuggerAutoConnect(True)
        self.enableDebuggerAutoConnectAfterSuccessfulConnection = False

    if self.connectionCompleteCallback:
      self.connectionCompleteCallback(pydevd.connected)

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
    logic.updatePydevdPath()
    logic.isConnected()
    
    self.delayDisplay('Test passed!')
