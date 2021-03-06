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
  ptvsd-4.1.3/ptvsd/attach_server.py
  ptvsd-4.1.3/ptvsd/daemon.py
  ptvsd-4.1.3/ptvsd/debugger.py
  ptvsd-4.1.3/ptvsd/exit_handlers.py
  ptvsd-4.1.3/ptvsd/futures.py
  ptvsd-4.1.3/ptvsd/ipcjson.py
  ptvsd-4.1.3/ptvsd/pathutils.py
  ptvsd-4.1.3/ptvsd/pydevd_hooks.py
  ptvsd-4.1.3/ptvsd/reraise.py
  ptvsd-4.1.3/ptvsd/reraise2.py
  ptvsd-4.1.3/ptvsd/reraise3.py
  ptvsd-4.1.3/ptvsd/runner.py
  ptvsd-4.1.3/ptvsd/safe_repr.py
  ptvsd-4.1.3/ptvsd/session.py
  ptvsd-4.1.3/ptvsd/socket.py
  ptvsd-4.1.3/ptvsd/ThirdPartyNotices.txt
  ptvsd-4.1.3/ptvsd/untangle.py
  ptvsd-4.1.3/ptvsd/version.py
  ptvsd-4.1.3/ptvsd/wrapper.py
  ptvsd-4.1.3/ptvsd/_attach.py
  ptvsd-4.1.3/ptvsd/_local.py
  ptvsd-4.1.3/ptvsd/_remote.py
  ptvsd-4.1.3/ptvsd/_util.py
  ptvsd-4.1.3/ptvsd/_version.py
  ptvsd-4.1.3/ptvsd/__init__.py
  ptvsd-4.1.3/ptvsd/__main__.py
  ptvsd-4.1.3/ptvsd/_vendored/force_pydevd.py
  ptvsd-4.1.3/ptvsd/_vendored/_pydevd_packaging.py
  ptvsd-4.1.3/ptvsd/_vendored/_util.py
  ptvsd-4.1.3/ptvsd/_vendored/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevconsole.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_file_utils.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_tracing.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_app_engine_debug_startup.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_coverage.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_pysrc.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_run_in_console.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/setup_cython.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/add_code_to_python_process.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/attach_amd64.dll
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/attach_pydevd.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/attach_script.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/attach_x86.dll
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/attach_x86.dylib
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/attach_x86_64.dylib
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/README.txt
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/_always_live_program.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/_check.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/_test_attach_to_process.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/_test_attach_to_process_linux.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/dll/attach.cpp
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/dll/attach.h
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/dll/compile_dll.bat
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/dll/python.h
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/dll/stdafx.cpp
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/dll/stdafx.h
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/dll/targetver.h
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/attach_linux.c
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/compile_mac.sh
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/compile_so.sh
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/gdb_threads_settrace.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/lldb_prepare.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/lldb_threads_settrace.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/Makefile
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/linux/python.h
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/breakpoint.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/compat.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/crash.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/debug.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/disasm.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/event.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/interactive.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/module.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/plugins
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/process.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/registry.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/search.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/sql.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/system.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/textio.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/thread.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/util.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/window.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/plugins/do_example.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/plugins/do_exchain.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/plugins/do_exploitable.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/plugins/do_symfix.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/plugins/README
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/plugins/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/advapi32.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/context_amd64.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/context_i386.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/dbghelp.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/defines.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/gdi32.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/kernel32.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/ntdll.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/peb_teb.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/psapi.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/shell32.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/shlwapi.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/user32.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/version.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/wtsapi32.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_attach_to_process/winappdbg/win32/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_concurrency_analyser/pydevd_concurrency_logger.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_concurrency_analyser/pydevd_thread_wrappers.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_concurrency_analyser/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/django_debug.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/jinja2_debug.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/extensions/README.md
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/extensions/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/extensions/types/pydevd_helpers.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/extensions/types/pydevd_plugins_django_form_str.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/extensions/types/pydevd_plugin_numpy_types.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydevd_plugins/extensions/types/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhook.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhookglut.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhookgtk.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhookgtk3.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhookpyglet.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhookqt4.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhookqt5.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhooktk.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/inputhookwx.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/matplotlibtools.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/qt.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/qt_for_kernel.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/qt_loaders.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/README
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/version.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_ipython/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_sitecustomize/sitecustomize.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/pydev_sitecustomize/__not_in_default_pythonpath.txt
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevconsole_code_for_ironpython.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_additional_thread_info.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_additional_thread_info_regular.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_breakpoints.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_comm.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_command_line_handling.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_console.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_constants.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_custom_frames.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_cython.c
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_cython.pyx
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_cython_wrapper.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_dont_trace.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_dont_trace_files.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_exec.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_exec2.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_extension_api.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_extension_utils.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_frame.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_frame_utils.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_import_class.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_io.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_kill_all_pydevd_threads.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_plugin_utils.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_process_net_command.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_referrers.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_reload.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_resolver.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_save_locals.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_signature.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_stackless.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_traceproperty.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_trace_api.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_trace_dispatch.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_trace_dispatch_regular.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_utils.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_vars.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_vm_type.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/pydevd_xml.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_bundle/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_evaluator.c
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_evaluator.pxd
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_evaluator.pyx
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_eval_cython_wrapper.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_eval_main.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/pydevd_frame_tracing.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/pydevd_modify_bytecode.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydevd_frame_eval/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/fix_getpass.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_console_utils.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_imports.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_import_hook.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_ipython_console.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_ipython_console_011.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_is_thread_alive.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_localhost.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_log.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_monkey.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_monkey_qt.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_override.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_umd.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/pydev_versioncheck.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_calltip_util.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_completer.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_filesystem_encoding.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_getopt.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_imports_tipper.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_jy_imports_tipper.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_log.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/_pydev_tipper_common.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_bundle/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_BaseHTTPServer.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_execfile.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_inspect.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_pkgutil_old.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_saved_modules.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_SimpleXMLRPCServer.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_SocketServer.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_sys_patch.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_uuid_old.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/_pydev_xmlrpclib.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_imps/__init__.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles_coverage.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles_nose.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles_parallel.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles_parallel_client.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles_pytest2.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles_unittest.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/pydev_runfiles_xml_rpc.py
  ptvsd-4.1.3/ptvsd/_vendored/pydevd/_pydev_runfiles/__init__.py
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )
