cmake_minimum_required(VERSION 2.8.9)

project(DebuggingTools)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/DebuggingTools")
set(EXTENSION_CATEGORY "Developer Tools")
set(EXTENSION_CONTRIBUTORS "Andras Lasso (PerkLab, Queen's University), Mikael Brudfors (Laboratorio de Imagen Medica, Hospital Gregorio Maranon - http://image.hggm.es/)")
set(EXTENSION_DESCRIPTION "This extension contains various tools useful for developing and debugging modules. Includes a tool for connecting Slicer to remote visual debugger for Python scripts using PyDev (http://pydev.org/) and node update performance statistics")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/SlicerRt/SlicerDebuggingTools/master/DebuggingTools.png")
set(EXTENSION_SCREENSHOTURLS "https://www.slicer.org/slicerWiki/images/f/f2/PyDevRemoteDebugSlicer.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(PyDevRemoteDebug)
add_subdirectory(NodeModifiedStatistics)
add_subdirectory(NodeInfo)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
