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

#
# PyDevRemoteDebugWidget
#

class PyDevRemoteDebugWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  
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

  def isCurrentSettingValid(self):
    if not self.getDebugger():
      return False
    if self.getDebugger()=="Eclipse" and self.isValidPydevdDir(self.pydevdDirSelector.currentPath):
      return True
    if self.getDebugger()=="PyCharm" and self.isValidPyCharmDebugEggPath(self.pyCharmDebugEggPathSelector.currentPath):
      return True
    return False
    
  def setup(self):

    # Do not show reload&test in developer mode, as debugger is mostly used by developers
    # but they are not interested in debugging this module.
    # ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...
    
    self.portNumber = 5678
    
    # Settings Area
    self.settingsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.settingsCollapsibleButton.text = "Settings"
    self.settingsCollapsibleButton.collapsed = True
    self.layout.addWidget(self.settingsCollapsibleButton)
    settingsFormLayout = qt.QFormLayout(self.settingsCollapsibleButton)
    
    # Debugger selector
    self.debuggerSelector = qt.QComboBox()
    self.debuggerSelector.toolTip = "Chose debugger server."
    debugger = self.getDebugger()
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
    pydevdDir=self.getEclipsePydevdDir(enableAutoDetect=(debugger=='Eclipse'))
    self.pydevdDirSelector = ctk.ctkPathLineEdit()
    self.pydevdDirSelector.setCurrentPath(pydevdDir)
    self.pydevdDirSelector.filters=self.pydevdDirSelector.Dirs
    self.pydevdDirSelector.setMaximumWidth(300)
    self.pydevdDirSelector.setToolTip("Set the path to pydevd.py. It is in the eclipse folder within plugins/...pydev.../pysrc.")
    settingsFormLayout.addRow("Eclipse pydevd.py directory:", self.pydevdDirSelector)

    # pycharm-debug.egg path selector
    pyCharmDebugEggPathSelector=self.getPyCharmDebugEggPath(enableAutoDetect=(debugger=='PyCharm'))
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
    self.connectButton.setStyleSheet("background-color: rgb(150, 255, 150); color: rgb(0, 0, 0)");
    connectionFormLayout.addRow(self.connectButton)

    # Connections
    self.connectButton.connect('clicked(bool)', self.onConnect)

    # Add vertical spacer
    self.layout.addStretch(1)
    
    self.onDebuggerSelected()

  def cleanup(self):
    pass

  def onDebuggerSelected(self):
  
    self.saveDebugger(self.debuggerSelector.currentText)

    if self.debuggerSelector.currentText=='Eclipse':
      self.connectButton.text = "Connect to Eclipse debugger"
      self.connectButton.toolTip = "Connect to PyDev remote debug server"
      self.pydevdDirSelector.enabled = True
      self.pyCharmDebugEggPathSelector.enabled = False
      # Auto-detect path
      if not self.pydevdDirSelector.currentPath:
        pydevdDir=self.getEclipsePydevdDir(enableAutoDetect=True)
        if pydevdDir:
          self.pydevdDirSelector.setCurrentPath(pydevdDir)
    elif self.debuggerSelector.currentText=='PyCharm':
      self.connectButton.text = "Connect to PyCharm debugger"
      self.connectButton.toolTip = "Connect to PyCharm remote debug server"
      self.pydevdDirSelector.enabled = False
      self.pyCharmDebugEggPathSelector.enabled = True
      # Auto-detect path
      if not self.pyCharmDebugEggPathSelector.currentPath:
        eggDir=self.getPyCharmDebugEggPath(enableAutoDetect=True)
        if eggDir:
          self.pyCharmDebugEggPathSelector.setCurrentPath(eggDir)
    else:
      self.pydevdDirSelector.enabled = False
      self.pyCharmDebugEggPathSelector.enabled = False
    
  def onConnect(self):
  
    if self.debuggerSelector.currentText=='Eclipse':
      pydevdDir=self.pydevdDirSelector.currentPath
      # Verify path
      if not self.isValidPydevdDir(pydevdDir):
        self.settingsCollapsibleButton.collapsed = False
        qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyDev", 'Please set the correct path to pydevd.py in the settings panel')
        return
      self.savePydevdDir(pydevdDir)
    elif self.debuggerSelector.currentText=='PyCharm':
      pydevdDir=self.pyCharmDebugEggPathSelector.currentPath
      # Verify path
      if not self.isValidPyCharmDebugEggPath(pydevdDir):
        self.settingsCollapsibleButton.collapsed = False
        qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyCharm", 'Please set the correct path to PyCharm debug egg file in the settings panel')
        return
      self.savePyCharmDebugEggPath(pydevdDir)
    else:
      self.settingsCollapsibleButton.collapsed = False
      qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to Python remote debug server", 'Please select a debugger in the settings panel')
      return
    
    import sys
    sys.path.insert(0,pydevdDir)
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

    # #########################################
    # Connected to remote debug server
    ###########################################
    logging.debug("Connected to remote debug server")

  def onConnectionComplete(self):
    import pydevd
    if pydevd.connected:
      self.connectButton.text = "Connected to debug server"
    else:
      self.connectButton.text = "Connect to debug server"
    self.info.hide()
