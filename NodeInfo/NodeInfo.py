import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# NodeInfo
#

class NodeInfo(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Node info"
    self.parent.categories = ["Developer Tools"]
    self.parent.dependencies = []
    self.parent.contributors = ["Andras Lasso (PerkLab, Queen's University)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """Opens a popup window that shows contents of a MRML node."""
    self.parent.acknowledgementText = """ """ # replace with organization, grant and thanks.
    slicer.app.connect("startupCompleted()", self.initializeNodesObject)

  def initializeNodesObject(self):
    """Create nodes object and add it to the Python console's namespace.
    It makes MRML nodes available in the Python console by autcomplete,by typing `n.` and pressing `Tab` key.
    For example, the `MRHead` node becomes available in the Python console as `n.MRHead`.
    """
    # Create a Nodes object
    slicer.nodes = Nodes()
    # Make the object available in the Python console
    pm = slicer.app.pythonManager()
    pm.executeString("from slicer import nodes as n")

#
# Nodes object that makes all MRML nodes available as attribute.
#

class Nodes(object):
    """This object has MRML nodes in the slicer scene available as attributes.
    The attribute name is generated from the node name, replacing invalid characters by underscore
    and prepending `n` to node names that start with a number.
    """
    def __init__(self, ignoreHiddenNodes=True):
        self.variableNameToId = {}
        self.ignoreHiddenNodes = ignoreHiddenNodes
    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        return slicer.mrmlScene.GetNodeByID(self.variableNameToId[name])
    @property
    def __dict__(self):
        import slicer
        import re
        attributes = {}
        scene = slicer.mrmlScene
        count = scene.GetNumberOfNodes()
        for idx in range(count):
            node = scene.GetNthNode(idx)
            if self.ignoreHiddenNodes and node.GetHideFromEditors():
                continue
            nodeName = node.GetName()
            id = node.GetID()
            # Python variable can only contain word characters (a-z, A-Z, 0-9, including _),
            # replace non-word characters by underscore.
            variableName = re.sub(r'\W+', '_', nodeName)
            # Python variable name cannot start with a number, prepend "n" if it does.
            if variableName[:1].isdigit():
                variableName = "n" + variableName
            self.variableNameToId[variableName] = id
            attributes[variableName] = type(node)
        return attributes

#
# NodeInfoWidget
#

class NodeInfoWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Input
    inputsCollapsibleButton = ctk.ctkCollapsibleButton()
    inputsCollapsibleButton.text = "Inputs"
    self.layout.addWidget(inputsCollapsibleButton)
    inputsFormLayout = qt.QFormLayout(inputsCollapsibleButton)

    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = True
    self.inputSelector.renameEnabled = True
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    inputsFormLayout.addRow("Input Node: ", self.inputSelector)

    self.showHiddenNodesCheckBox = qt.QCheckBox('')
    self.showHiddenNodesCheckBox.checked = False
    inputsFormLayout.addRow('Show Hidden Nodes: ', self.showHiddenNodesCheckBox)

    # Quick info
    quickInfoCollapsibleButton = ctk.ctkCollapsibleButton()
    quickInfoCollapsibleButton.text = "Node overview"
    self.layout.addWidget(quickInfoCollapsibleButton)
    quickInfoFormLayout = qt.QFormLayout(quickInfoCollapsibleButton)

    self.nodeNameLabel = qt.QLabel()
    quickInfoFormLayout.addRow("Node name: ", self.nodeNameLabel)

    self.nodeIdLabel = qt.QLabel()
    quickInfoFormLayout.addRow("Node ID: ", self.nodeIdLabel)

    self.nodeTypeLabel = qt.QLabel()
    quickInfoFormLayout.addRow("Node type: ", self.nodeTypeLabel)

    referencedNodeFrame = qt.QFrame()
    hbox = qt.QHBoxLayout()
    referencedNodeFrame.setLayout(hbox)
    self.referencedNodeSelector = qt.QComboBox()
    self.referencedNodeSelectButton = qt.QPushButton("Select")
    hbox.addWidget(self.referencedNodeSelector)
    hbox.addWidget(self.referencedNodeSelectButton)
    quickInfoFormLayout.addRow("Referenced nodes: ", referencedNodeFrame)

    referencingNodeFrame = qt.QFrame()
    hbox = qt.QHBoxLayout()
    referencingNodeFrame.setLayout(hbox)
    self.referencingNodeSelector = qt.QComboBox()
    self.referencingNodeSelectButton = qt.QPushButton("Select")
    hbox.addWidget(self.referencingNodeSelector)
    hbox.addWidget(self.referencingNodeSelectButton)
    quickInfoFormLayout.addRow("Nodes referencing this node: ", referencingNodeFrame)

    self.showInfoButton = qt.QPushButton("Show node information window")
    quickInfoFormLayout.addRow(self.showInfoButton)

    self.createVariableButtonBaseText = "Create variable in Python console"
    self.createVariableButton = qt.QPushButton(self.createVariableButtonBaseText)
    quickInfoFormLayout.addRow(self.createVariableButton)

    # connections
    self.showInfoButton.connect('clicked(bool)', self.onShowInfoClicked)
    self.createVariableButton.connect('clicked(bool)', self.onCreateVariableClicked)
    self.showHiddenNodesCheckBox.connect('stateChanged(int)', self.onShowHiddenNodesChecked)
    self.inputSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelectNode)
    self.referencedNodeSelectButton.connect('clicked(bool)', self.onSelectReferencedNodeClicked)
    self.referencingNodeSelectButton.connect('clicked(bool)', self.onSelectReferencingNodeClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Initialize
    self.onSelectNode()

  def cleanup(self):
    pass

  def onSelectNode(self):
    node = self.inputSelector.currentNode()
    if node:
      self.nodeNameLabel.text = node.GetName()
      self.nodeIdLabel.text = node.GetID()
      self.nodeTypeLabel.text = node.GetClassName()
      self.createVariableButton.text = self.createVariableButtonBaseText + ": " + self.getNodeVariableName()
      self.createVariableButton.setEnabled(True)
      self.referencedNodeSelector.clear()
      referencedNodeIds = set()
      for roleIndex in range(node.GetNumberOfNodeReferenceRoles()):
        roleName = node.GetNthNodeReferenceRole(roleIndex)
        numberOfReferencedNodes = node.GetNumberOfNodeReferences(roleName)
        for referencedNodeIndex in range(numberOfReferencedNodes):
          referencedNode = node.GetNthNodeReference(roleName, referencedNodeIndex)
          if numberOfReferencedNodes > 1:
            label = "{0} [{1}]: {2} ({3})".format(roleName, referencedNodeIndex, referencedNode.GetName(), referencedNode.GetID())
          else:
            label = "{0}: {1} ({2})".format(roleName, referencedNode.GetName(), referencedNode.GetID())
          self.referencedNodeSelector.addItem(label, referencedNode.GetID())
          referencedNodeIds.add(referencedNode.GetID())
      self.referencingNodeSelector.clear()
      numberOfNodeReferences = slicer.mrmlScene.GetNumberOfNodeReferences()
      for nodeReferenceIndex in range(numberOfNodeReferences):
        if slicer.mrmlScene.GetNthReferencingNode(nodeReferenceIndex) == node:
          # referenced node
          # Before node reference infrastructure in vtkMRMLNode was introduced, nodes used
          # hand-crafted code to implement references. Some nodes still use the old mechanism.
          # If we find referenced nodes that are not yet added to the combobox, we add them.
          referencedNodeId = slicer.mrmlScene.GetNthReferencedID(nodeReferenceIndex)
          if referencedNodeId in referencedNodeIds:
            continue
          label = "{0} ({1})".format(slicer.mrmlScene.GetNodeByID(referencedNodeId).GetName(), referencedNodeId)
          self.referencedNodeSelector.addItem(label, referencedNodeId)
          referencedNodeIds.add(referencedNodeId)
        if slicer.mrmlScene.GetNthReferencedID(nodeReferenceIndex) == node.GetID():
          # referencing node
          referencingNode = slicer.mrmlScene.GetNthReferencingNode(nodeReferenceIndex)
          label = "{0} ({1})".format(referencingNode.GetName(), referencingNode.GetID())
          self.referencingNodeSelector.addItem(label, referencingNode.GetID())
    else:
      self.nodeNameLabel.text = ""
      self.nodeIdLabel.text = ""
      self.nodeTypeLabel.text = ""
      self.referencedNodeSelector.clear()
      self.referencedNodeSelectButton.setEnabled(False)
      self.createVariableButton.setEnabled(False)
    self.referencedNodeSelectButton.setEnabled(self.referencedNodeSelector.count > 0)
    self.referencingNodeSelectButton.setEnabled(self.referencingNodeSelector.count > 0)

  def onShowInfoClicked(self):
    logic = NodeInfoLogic()
    logic.createNodeInfoPopupWindow(self.inputSelector.currentNode())

  def onSelectReferencedNodeClicked(self):
    referenceNodeId = self.referencedNodeSelector.itemData(self.referencedNodeSelector.currentIndex)
    referencedNode = slicer.mrmlScene.GetNodeByID(referenceNodeId)
    if referencedNode.GetHideFromEditors():
      # We can only select a hidden node if hidden nodes are listed in the node selector
      self.showHiddenNodesCheckBox.checked = True
    self.inputSelector.setCurrentNodeID(referenceNodeId)

  def onSelectReferencingNodeClicked(self):
    referencingNodeId = self.referencingNodeSelector.itemData(self.referencingNodeSelector.currentIndex)
    referencingNode = slicer.mrmlScene.GetNodeByID(referencingNodeId)
    if referencingNode.GetHideFromEditors():
      # We can only select a hidden node if hidden nodes are listed in the node selector
      self.showHiddenNodesCheckBox.checked = True
    self.inputSelector.setCurrentNodeID(referencingNodeId)

  def onShowHiddenNodesChecked(self, state):
    self.inputSelector.showHidden = state

  def getNodeVariableName(self):
    nodeName = self.inputSelector.currentNode().GetName()
    varName = nodeName.lower()
    # remove special characters (space, dot, etc)
    import re
    varName = re.sub(r'\W+', '', varName)
    return varName

  def onCreateVariableClicked(self):
    pm=slicer.app.pythonManager()
    currentNode = self.inputSelector.currentNode()
    pm.executeString(self.getNodeVariableName()+"=slicer.mrmlScene.GetNodeByID('"+currentNode.GetID()+"')")
    pm.executeString("print('Created variable: " + currentNode.GetName() + " (" + currentNode.GetID()
      + ") -> " + self.getNodeVariableName() + "')")
    # Switch focus to the Python console so that the user can start typing immediately
    mw=slicer.util.mainWindow()
    mw.onPythonConsoleToggled(True)


#
# NodeInfoLogic
#

class NodeInfoLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def createNodeInfoPopupWindow(self, node, returnPopupWindow = False):

    # Main frame

    mainWindow = slicer.util.mainWindow()
    nodeInfoDockWidget = qt.QDockWidget(node.GetName(), mainWindow)
    #nodeInfoDockWidget.setObjectName(node.GetID())
    nodeInfoDockWidget.setFeatures(qt.QDockWidget.DockWidgetClosable + qt.QDockWidget.DockWidgetMovable + qt.QDockWidget.DockWidgetFloatable)

    nodeInfoMainFrame = qt.QFrame(nodeInfoDockWidget)
    nodeInfoMainFrameLayout = qt.QVBoxLayout(nodeInfoMainFrame)

    infoWidget = slicer.qMRMLNodeAttributeTableWidget(nodeInfoMainFrame)

    # Buttons

    buttonFrame = qt.QFrame(nodeInfoMainFrame)
    hbox = qt.QHBoxLayout()
    buttonFrame.setLayout(hbox)

    if hasattr(infoWidget, 'updateWidgetFromMRML'):
      forceRefreshButton = qt.QPushButton("Force refresh")
      forceRefreshButton.setToolTip(
        "Update window contents from node. Note that node modified event automatically refreshes the window.")
      hbox.addWidget(forceRefreshButton)
      forceRefreshButton.connect('clicked()', infoWidget.updateWidgetFromMRML)

    forceModifiedButton = qt.QPushButton("Invoke modified")
    forceModifiedButton.setToolTip("Calls Modified() on the node. Useful for triggering updates during debugging.")
    hbox.addWidget(forceModifiedButton)
    forceModifiedButton.connect('clicked()', node.Modified)

    # Info area

    nodeInfoScrollArea = qt.QScrollArea(nodeInfoMainFrame)
    infoWidget.setMRMLNode(node)
    nodeInfoScrollArea.setWidget(infoWidget)
    nodeInfoScrollArea.setWidgetResizable(True)

    slicer.util.findChildren(infoWidget, 'MRMLNodeAttributeTableView')[0].hide()
    slicer.util.findChildren(infoWidget, 'AddAttributeButton')[0].hide()
    slicer.util.findChildren(infoWidget, 'RemoveAttributeButton')[0].hide()
    slicer.util.findChildren(infoWidget, 'NodeInformationGroupBox')[0].collapsed = False
    slicer.util.findChildren(infoWidget, 'NodeInformationGroupBox')[0].layout().addStretch(1)

    # Show main frame
    nodeInfoMainFrameLayout.addWidget(buttonFrame)
    nodeInfoMainFrameLayout.addWidget(nodeInfoScrollArea)
    nodeInfoDockWidget.setWidget(nodeInfoMainFrame)
    mainWindow.addDockWidget(qt.Qt.RightDockWidgetArea, nodeInfoDockWidget)

    if returnPopupWindow:
      return nodeInfoDockWidget


class NodeInfoTest(ScriptedLoadableModuleTest):
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
    self.test_NodeInfo1()

  def test_NodeInfo1(self):
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
    logic = NodeInfoLogic()
    popup = logic.createNodeInfoPopupWindow(slicer.util.getNode('Selection'), returnPopupWindow=True)
    self.assertIsNotNone(popup)
    self.delayDisplay('Test passed!')
