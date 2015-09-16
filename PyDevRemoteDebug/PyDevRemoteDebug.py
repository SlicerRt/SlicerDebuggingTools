import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# PyDevRemoteDebug
#

class PyDevRemoteDebug:
  def __init__(self, parent):
    parent.title = "Python debugger"
    parent.categories = ["Developer Tools"]
    parent.dependencies = []
    parent.contributors = ["Andras Lasso (PerkLab at Queen's University)"]
    parent.helpText = """
    This module connects to PyDev remote debugger for running Python scripts in the Eclipse integrated development environment.
    <a href="http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/PyDevRemoteDebug">More information...</a>
    """
    parent.acknowledgementText = """
    This work is part of the SparKit project, funded by An Applied Cancer Research Unit of Cancer Care Ontario with funds provided by the Ministry of Health and Long-Term Care and the Ontario Consortium for Adaptive Interventions in Radiation Oncology (OCAIRO) to provide free, open-source toolset for radiotherapy and related image-guided interventions.
    """
    self.parent = parent

#
# qPyDevRemoteDebugWidget
#

class PyDevRemoteDebugWidget:
  def __init__(self, parent = None):
    self.developerMode = False # change this to True to get reload and test
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()


  def savePydevdDir(self, pydevdDir):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains('PydevdPath'):
      pydevdDirSaved = settings.value('PydevdPath')
      if pydevdDirSaved == pydevdDir:
        return
    settings.setValue('PydevdPath',pydevdDir)

  def isValidPydevdDir(self, pydevdDir):
    import os.path
    pydevdPath=pydevdDir+'/pydevd.py'
    return os.path.isfile(pydevdPath)

  def getPydevdDir(self):
    pydevdDir=''

    settings = qt.QSettings()
    if settings.contains('PydevdPath'):
      pydevdDir = settings.value('PydevdPath')
      if self.isValidPydevdDir(pydevdDir):
        # found a good value in the settings
        return pydevdDir

    if not pydevdDir:
      candidatePydevdDirs=[]
      candidatePydevdDirs.append('f:/devel/PyDevRemoteDebug/PyDevRemoteDebug')
      candidatePydevdDirs.append('c:/Program Files/Brainwy/LiClipse 0.9.7/plugins/org.python.pydev_3.3.3.201401272005/pysrc')
      for pydevdDir in candidatePydevdDirs:
        if self.isValidPydevdDir(pydevdDir):
          return pydevdDir

    # not found
    return ''


  def setup(self):
    # Instantiate and connect widgets ...
    
    # Reload and Test area
    if self.developerMode:
      # section
      reloadCollapsibleButton = ctk.ctkCollapsibleButton()
      reloadCollapsibleButton.text = "Reload && Test"
      self.layout.addWidget(reloadCollapsibleButton)
      reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)
      # reload button
      self.reloadButton = qt.QPushButton("Reload")
      self.reloadButton.toolTip = "Reload this module."
      self.reloadButton.name = "PyDevRemoteDebug Reload"
      reloadFormLayout.addWidget(self.reloadButton)
      self.reloadButton.connect('clicked()', self.onReload)

    # Settings Area
    self.settingsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.settingsCollapsibleButton.text = "Settings"
    self.settingsCollapsibleButton.collapsed = True
    self.layout.addWidget(self.settingsCollapsibleButton)
    settingsFormLayout = qt.QFormLayout(self.settingsCollapsibleButton)
    # pydevd.py path selector
    pydevdDir=self.getPydevdDir()
    self.pydevdDirSelector = ctk.ctkPathLineEdit()
    self.pydevdDirSelector.setCurrentPath(pydevdDir)
    self.pydevdDirSelector.filters=self.pydevdDirSelector.Dirs
    self.pydevdDirSelector.setMaximumWidth(300)
    self.pydevdDirSelector.setToolTip("Set the path to pydevd.py. It is in the eclipse folder within plugins/...pydev.../pysrc.")
    settingsFormLayout.addRow("Path to pydevd.py: ", self.pydevdDirSelector)
    if not self.isValidPydevdDir(pydevdDir):
      self.settingsCollapsibleButton.collapsed = False

    # Connection Area
    connectionCollapsibleButton = ctk.ctkCollapsibleButton()
    connectionCollapsibleButton.text = "Connection"
    connectionCollapsibleButton.collapsed = False
    self.layout.addWidget(connectionCollapsibleButton)
    connectionFormLayout = qt.QFormLayout(connectionCollapsibleButton)
    # Connect Button
    self.connectButton = qt.QPushButton("Connect")
    self.connectButton.toolTip = "Connect to PyDev remote debugger"
    self.connectButton.setAutoFillBackground(True)
    self.connectButton.setStyleSheet("background-color: rgb(150, 255, 150); color: rgb(0, 0, 0)");
    connectionFormLayout.addRow(self.connectButton)

    # Connections
    self.connectButton.connect('clicked(bool)', self.onConnect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onReload(self,moduleName="PyDevRemoteDebug"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    globals()[moduleName] = slicer.util.reloadScriptedModule(moduleName)

  def onConnect(self):
    pydevdDir=self.pydevdDirSelector.currentPath

    # Verify pydevd path
    if not self.isValidPydevdDir(pydevdDir):
      self.settingsCollapsibleButton.collapsed = False
      qt.QMessageBox.warning(slicer.util.mainWindow(),
        "Connect to PyDev", 'Please set the correct path to pydevd.py in the settings panel')
      return

    # Import the debugger
    import sys
    self.savePydevdDir(pydevdDir)
    sys.path.insert(0,pydevdDir)
    import pydevd

    # Return if already connected
    if pydevd.connected:
      qt.QMessageBox.warning(slicer.util.mainWindow(),
      "Connect to PyDev", 'You are already connected to the remote debugger. If the connection is broken (e.g., because the server terminated the connection) then you need to restart Slicer to be able to connect again.')
      return
      
    # Show a dialog that explains that Slicer will hang
    self.info = qt.QDialog()
    self.info.setModal(False)
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel("Note: Slicer will now be paused for debugging until execution is resumed in PyDev",self.info)
    self.infoLayout.addWidget(self.label)
    self.info.show()
    self.info.repaint()
    qt.QTimer.singleShot(3000, self.info.hide)
    
    # Connect to the debugger        
    try:
      pydevd.settrace(pydevd.settrace(stdoutToServer=True, stderrToServer=True, suspend=False))      
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Connect to PyDev", 'An error occurred while trying to connect to PyDev remote debugger. Make sure he pydev server is started.\n\n' + str(e))

    # You are seeing the script that established the PyDev remote debugger connection.
    # Click "Resume" (or press F8) to resume execution.
    ###########################################
    self.info.hide
    ###########################################
    