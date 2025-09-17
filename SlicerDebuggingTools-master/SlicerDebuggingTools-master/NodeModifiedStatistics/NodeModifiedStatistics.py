import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

import numpy as np
import time

class NodeModifiedStatistics(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Node modified statistics"
    self.parent.categories = ["Developer Tools"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mikael Brudfors (Laboratorio de Imagen Medica, Hospital Gregorio Maranon - http://image.hggm.es/), Andras Lasso (PerkLab, Queen's University)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    Collect statistics about refresh rate of continuously changing nodes. The module observes Modified event of the selected node.
    """
    self.parent.acknowledgementText = """
""" # replace with organization, grant and thanks.

class NodeModifiedStatisticsWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    self.logic = NodeModifiedStatisticsLogic()

    self.chartNode = None
    self.seriesNode = None

    ScriptedLoadableModuleWidget.setup(self)

    # Parameters
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    parametersFormLayout.addRow("Input Node: ", self.inputSelector)

    self.showHiddenNodesCheckBox = qt.QCheckBox('')
    self.showHiddenNodesCheckBox.checked = False
    parametersFormLayout.addRow('Show Hidden Nodes: ', self.showHiddenNodesCheckBox)

    self.computeStatisticsButton = qt.QPushButton("Compute Statistics")
    self.computeStatisticsButton.enabled = False
    self.computeStatisticsButton.checkable = True
    parametersFormLayout.addRow(self.computeStatisticsButton)

    # Statistics
    statisticsCollapsibleButton = ctk.ctkCollapsibleButton()
    statisticsCollapsibleButton.text = "Statistics"
    self.layout.addWidget(statisticsCollapsibleButton)
    statisticsFormLayout = qt.QFormLayout(statisticsCollapsibleButton)

    self.latestLineEdit = qt.QLineEdit('N/A')
    self.latestLineEdit.setReadOnly(True)
    statisticsFormLayout.addRow("Latest (ms): ", self.latestLineEdit)
    self.averageLineEdit = qt.QLineEdit('N/A')
    self.averageLineEdit.setReadOnly(True)
    self.fpsLineEdit = qt.QLineEdit('N/A')
    self.fpsLineEdit.setReadOnly(True)
    statisticsFormLayout.addRow("Average (updates per second): ", self.fpsLineEdit)
    statisticsFormLayout.addRow("Average (ms): ", self.averageLineEdit)
    self.sdLineEdit = qt.QLineEdit('N/A')
    self.sdLineEdit.setReadOnly(True)
    statisticsFormLayout.addRow("Standard deviation (ms): ", self.sdLineEdit)
    self.minLineEdit = qt.QLineEdit('N/A')
    self.minLineEdit.setReadOnly(True)
    statisticsFormLayout.addRow("Minimum (ms): ", self.minLineEdit)
    self.maxLineEdit = qt.QLineEdit('N/A')
    self.maxLineEdit.setReadOnly(True)
    statisticsFormLayout.addRow("Maximum (ms): ", self.maxLineEdit)

    self.resetStatisticsButton = qt.QPushButton("Reset Statistics")
    self.resetStatisticsButton.enabled = True
    statisticsFormLayout.addRow(self.resetStatisticsButton)

    samplesCollapsibleButton = ctk.ctkCollapsibleButton()
    samplesCollapsibleButton.text = "Samples"
    self.layout.addWidget(samplesCollapsibleButton)
    samplesFormLayout = qt.QFormLayout(samplesCollapsibleButton)

    self.outputTableSelector = slicer.qMRMLNodeComboBox()
    self.outputTableSelector.selectNodeUponCreation = True
    self.outputTableSelector.nodeTypes = ['vtkMRMLTableNode']
    self.outputTableSelector.addEnabled = True
    self.outputTableSelector.removeEnabled = True
    self.outputTableSelector.noneEnabled = True
    self.outputTableSelector.showHidden = False
    self.outputTableSelector.showChildNodeTypes = False
    self.outputTableSelector.setMRMLScene(slicer.mrmlScene)
    samplesFormLayout.addRow("Output table: ", self.outputTableSelector)

    self.showSamplesButton = qt.QPushButton("Get latest samples")
    samplesFormLayout.addRow(self.showSamplesButton)

    self.showSamplesPlotButton = qt.QPushButton("Show latest samples plot")
    samplesFormLayout.addRow(self.showSamplesPlotButton)

    self.sampleList = slicer.qMRMLTableView()
    self.sampleList.setMRMLScene(slicer.mrmlScene)
    samplesFormLayout.addRow(self.sampleList)

    # connections
    self.computeStatisticsButton.connect('clicked(bool)', self.onComputeStatisticsClicked)
    self.resetStatisticsButton.connect('clicked(bool)', self.onResetStatisticsClicked)
    self.showSamplesButton.connect('clicked(bool)', self.onShowSamplesClicked)
    self.showSamplesPlotButton.connect('clicked(bool)', self.onShowSamplesPlotClicked)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.showHiddenNodesCheckBox.connect('stateChanged(int)', self.onShowHiddenNodesChecked)
    self.outputTableSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

    self.lineEdits = [self.latestLineEdit, self.fpsLineEdit, self.averageLineEdit, self.sdLineEdit, self.minLineEdit, self.maxLineEdit]

  def cleanup(self):
    pass

  def onShowHiddenNodesChecked(self, state):
    self.inputSelector.showHidden = state

  def onSelect(self):
    if self.computeStatisticsButton.enabled:
      if self.computeStatisticsButton.checked:
        self.logic.removeModifiedObserver()
        self.resetStatsDisplay()
        self.logic.reset()
        self.computeStatisticsButton.checked = False
      elif not self.computeStatisticsButton.checked:
        self.resetStatsDisplay()
        self.logic.reset()
    self.computeStatisticsButton.enabled = self.inputSelector.currentNode()
    self.sampleList.setMRMLTableNode(self.outputTableSelector.currentNode())

  def onComputeStatisticsClicked(self):
    if self.computeStatisticsButton.checked:
      self.logic.addModifiedObserver(self.inputSelector.currentNode(), self.lineEdits)
    elif not self.computeStatisticsButton.checked:
      self.logic.removeModifiedObserver()

  def onResetStatisticsClicked(self):
    self.logic.reset()
    self.resetStatsDisplay()

  def resetStatsDisplay(self):
    for lineEdit in self.lineEdits:
      lineEdit.setText('N/A')
    if self.sampleList.mrmlTableNode():
      self.sampleList.mrmlTableNode().RemoveAllColumns()

  def onShowSamplesClicked(self):
    tableNode = self.outputTableSelector.currentNode()
    if not tableNode:
      tableNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLTableNode", slicer.mrmlScene.GetUniqueNameByString("NodeModifiedStatisticsSamplesTable"))
      self.outputTableSelector.setCurrentNode(tableNode)
    slicer.util.updateTableFromArray(tableNode, self.logic.movingAverageSamples, 'time (s)')

  def onShowSamplesPlotClicked(self):
    # Ensure table node is created
    self.onShowSamplesClicked()
    tableNode = self.outputTableSelector.currentNode()

    # Create chart and add plot
    if not self.chartNode:
      self.chartNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLPlotChartNode", slicer.mrmlScene.GetUniqueNameByString("NodeModifiedStatisticsSamplesChart"))
      self.chartNode.SetTitle(self.chartNode.GetName())

    # Create plot series node(s)
    if not self.seriesNode:
      self.seriesNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLPlotSeriesNode", slicer.mrmlScene.GetUniqueNameByString("NodeModifiedStatisticsSamplesSeries"))
      self.seriesNode.SetUniqueColor()
    self.seriesNode.SetAndObserveTableNodeID(tableNode.GetID())
    self.seriesNode.SetPlotType(self.seriesNode.PlotTypeLine)
    self.seriesNode.SetYColumnName(tableNode.GetTable().GetColumn(0).GetName())
    if not self.chartNode.HasPlotSeriesNodeID(self.seriesNode.GetID()):
      self.chartNode.AddAndObservePlotSeriesNodeID(self.seriesNode.GetID())

    # Show plot in layout
    slicer.modules.plots.logic().ShowChartInLayout(self.chartNode)

    # Without this, chart view may show up completely empty when the same nodes are updated
    # (this is probably due to a bug in plotting nodes or widgets).
    self.chartNode.Modified()

class NodeModifiedStatisticsLogic(ScriptedLoadableModuleLogic):

  def __init__(self):
    self.latestInputNode = None
    self.modifiedObserverTag = -1
    self.ouputLineEdits = []
    self.movingAverageSamples = np.zeros(50) # Array to store the movingAverageSampleCount last measurements used to calculate average and SD
    self.reset()

  def __del__(self):
    self.removeModifiedObserver()

  def reset(self):
    self.movingAverageSec = 0
    self.maxTimeSec = 0
    self.minTimeSec = 100000
    self.previousTimeSec = -1
    self.movingStddevSec = 0
    self.numberOfMovingAverageSamplesCollected = 0

  def addModifiedObserver(self, inputNode, ouputLineEdits):
    self.previousTimeSec = -1
    self.ouputLineEdits = ouputLineEdits
    self.removeModifiedObserver()
    self.latestInputNode = inputNode
    self.modifiedObserverTag = inputNode.AddObserver('ModifiedEvent', self.nodeModifiedCallback)

  def removeModifiedObserver(self):
    if self.modifiedObserverTag != -1:
      self.latestInputNode.RemoveObserver(self.modifiedObserverTag)
      self.latestInputNode = None
      self.modifiedObserverTag = -1

  def nodeModifiedCallback(self, modifiedNode, event=None):
    currentTimeSec = time.time()
    if self.previousTimeSec < 0:
      # this is the first modified call, we cannot compute elapsed time yet
      self.previousTimeSec = currentTimeSec
      return
    # Latest
    latestElapsedTimeSec = currentTimeSec - self.previousTimeSec
    self.movingAverageSamples[self.numberOfMovingAverageSamplesCollected % len(self.movingAverageSamples)] = latestElapsedTimeSec
    self.numberOfMovingAverageSamplesCollected = self.numberOfMovingAverageSamplesCollected + 1
    # Max
    if latestElapsedTimeSec > self.maxTimeSec:
      self.maxTimeSec = latestElapsedTimeSec
    # Min
    if latestElapsedTimeSec < self.minTimeSec:
      self.minTimeSec = latestElapsedTimeSec
    # Average and SD
    if self.numberOfMovingAverageSamplesCollected >= len(self.movingAverageSamples):
      self.movingAverageSec = np.mean(self.movingAverageSamples)
      self.movingStddevSec = np.std(self.movingAverageSamples)
    self.setOutputLineEdits(latestElapsedTimeSec, self.movingAverageSec, self.movingStddevSec, self.minTimeSec, self.maxTimeSec)
    self.previousTimeSec = currentTimeSec

  def setOutputLineEdits(self, latestElapsedTimeSec, movingAverageSec, movingStddevSec, minSec, maxSec):
    self.ouputLineEdits[0].setText('%.0f' % (latestElapsedTimeSec * 1000))
    if self.numberOfMovingAverageSamplesCollected >= len(self.movingAverageSamples):
      self.ouputLineEdits[1].setText('%.1f' % (1/movingAverageSec))
      self.ouputLineEdits[2].setText('%.0f' % (movingAverageSec * 1000))
      self.ouputLineEdits[3].setText('%.0f' % (movingStddevSec * 1000))
    else:
      self.ouputLineEdits[1].setText('N/A')
      self.ouputLineEdits[2].setText('N/A')
      self.ouputLineEdits[3].setText('N/A')
    self.ouputLineEdits[4].setText('%.0f' % (minSec * 1000))
    self.ouputLineEdits[5].setText('%.0f' % (maxSec * 1000))