# Copyright (c) 2013-2016 Dassault Systemes. All rights reserved.

# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
# http://pylint-messages.wikidot.com/all-codes
# http://hackerboss.com/how-to-distribute-commercial-python-applications/
# http://stackoverflow.com/questions/8822335/what-does-python-file-extensions-pyc-pyd-pyo-stand-for

import sys
isPython2 = (sys.version_info < (3,0,0))
if isPython2:
    from httplib import HTTPConnection, HTTPException
else:
    from http.client import HTTPConnection, HTTPException

import json
import os
import random
import subprocess
import socket
import threading
import time
import platform

from dymola.dymola_exception import *

osString = platform.system()
if osString.startswith("Win"):
    if isPython2:
        from _winreg import *
    else:
        from winreg import *

# http://effbot.org/zone/thread-synchronization.htm
dymola_lock = threading.Lock()


class _UnquotedString(object):
    # pylint: disable=missing-docstring
    def __init__(self, value):
        self.value = value


class _NamedArgument(object):
    # pylint: disable=missing-docstring
    def __init__(self, name, value):
        self.named_argument = name
        self.named_value = value


class DymolaInterfaceInternal(object):
    """This is an internal class and should not be exposed."""

    # This flag controls whether the Dymola window will be visible or not when
    # calling functions in the interface. The default value is True,
    # which means that Dymola will be hidden.
    _nowindow = True

    # For debugging the Dymola interface. Note that it is intended for
    # debugging the interface, not Modelica models. Setting this variable
    # to True outputs debug messages in the console. For advanced
    # users only.
    _debug = False

    # Use this for test cases, for example to ensure that setup.mos is not read
    _testMode = False

    # By default, Dymola only allows local connections. The default value is
    # False. Set this flag to True to allow access from
    # other machines.
    _allowremote = False

    # Corresponds to the command-line argument with the same name. The default
    # value is False.
    _nolibraryscripts = False

    # http://stackoverflow.com/questions/7275430/how-to-select-a-port-number-for-a-custom-app
    # http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
    _FIRST_AVAILABLE_PORT = 44000
    _LAST_AVAILABLE_PORT = 44400

    # There is a convention that is followed by most Python code: a name prefixed
    # with an underscore (e.g. _spam) should be treated as a non-public part of the
    # API (whether it is a function, a method or a data member).
    _HOSTNAME = "127.0.0.1"

    @staticmethod
    def _get_full_dymola_install_path(dymola_folder_name):
        # pylint: disable=missing-docstring
        try:
            aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            aKeyName = "SOFTWARE\\Wow6432Node\\Dassault Systemes\\" + dymola_folder_name
            aKey = OpenKey(aReg, aKeyName)
            path, registry_type = QueryValueEx(aKey, "InstallDir")
            if os.path.exists(path) and os.path.isdir(path):
                DymolaInterfaceInternal._print_debug_message("Found Dymola install path (1): " + path)
                return path
        except (EnvironmentError, WindowsError) as ex:
            DymolaInterfaceInternal._print_debug_message("Failed to locate Dymola install path in 64-bit registry location: " + str(ex))
            pass

        try:
            aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            aKeyName = "SOFTWARE\\Dassault Systemes\\" + dymola_folder_name
            aKey = OpenKey(aReg, aKeyName)
            path, registry_type = QueryValueEx(aKey, "InstallDir")
            if os.path.exists(path) and os.path.isdir(path):
                DymolaInterfaceInternal._print_debug_message("Found Dymola install path (2): " + path)
                return path
        except (EnvironmentError, WindowsError) as ex:
            DymolaInterfaceInternal._print_debug_message("Failed to locate Dymola install path in 32-bit registry location: " + str(ex))
            pass

        program_files_folder = os.environ.get("ProgramFiles")
        if program_files_folder:
            path = program_files_folder + "/" + dymola_folder_name
            if os.path.exists(path) and os.path.isdir(path):
                DymolaInterfaceInternal._print_debug_message("Found Dymola install path (4): " + path)
                return path

        program_files_folder = os.environ.get("ProgramFiles(x86)")
        if program_files_folder:
            path = program_files_folder + "/" + dymola_folder_name
            if os.path.exists(path) and os.path.isdir(path):
                DymolaInterfaceInternal._print_debug_message("Found Dymola install path (3): " + path)
                return path

       

        raise DymolaException("Failed to locate Dymola install path. Please specify the path to Dymola.exe when instantiating DymolaInterface.")

    @staticmethod
    def _print_debug_message(msg):
        # pylint: disable=missing-docstring
        if DymolaInterfaceInternal._debug:
            print(msg)

    def __init__(self, dymola_version, dymolapath, port, showwindow, debug, allowremote, nolibraryscripts):
        self._nowindow = not showwindow
        DymolaInterfaceInternal._debug = debug
        self._allowremote = allowremote
        self._nolibraryscripts = nolibraryscripts

        self._rpc_id = 0
        self._portnumber = -1
        self._dymola_process = None

        dymola_lock.acquire()
        try:
            if port < 0:
                self._portnumber = self._find_available_port()
                self._print_debug_message("Using auto-assigned port " + str(self._portnumber) + ".")
                if self._portnumber < 0:
                    raise DymolaConnectionException("Failed to find an available port.")
            else:
                self._portnumber = port
            self._start_dymola(dymola_version, dymolapath, self._portnumber)
        except Exception as ex:
            raise DymolaConnectionException("Failed to start Dymola. " + str(ex))
        finally:
            dymola_lock.release()

    def ExecuteCommand(self, cmd):
        # pylint: disable=missing-docstring,invalid-name
        return self._call_dymola_function(cmd, None)

    def _type_is_string(self, s):
        is_string = False
        if type(s) is str:
            is_string = True
        if isPython2 and type(s) is unicode:
            is_string = True
        return is_string

    def _escape_for_json(self, s):
        result = s
        result = result.replace("\"", "%5c%22")
        result = result.replace("\'", "%5c%27")
        return result

    def _start_dymola(self, dymola_version, dymolapath, port):
        # pylint: disable=missing-docstring
        exists = os.path.exists(dymolapath) and os.path.isfile(dymolapath)
        if not exists:
            raise DymolaException("No Dymola executable found at " + dymolapath + ".")

        if not self._is_port_available(port):
            raise DymolaConnectionException("The port " + str(port) + " is already in use. Please use another port.")

        args = []
        args.append(dymolapath)
        args.append("-serverport")
        args.append(str(port))
        if self._nowindow:
            args.append("/nowindow")
        if self._allowremote:
            args.append("/allowremote")
        if self._nolibraryscripts:
            args.append("/nolibraryscripts")
        if DymolaInterfaceInternal._testMode:
            args.append("/nosettings")
        # subprocess.Popen() only runs a process in the background if nothing in
        # the python script depends on the output of the command being run
        self._dymola_process = subprocess.Popen(args)

        self._print_debug_message("Is Dymola running?")
        if not self._is_dymola_running():
            self._print_debug_message("No")
            raise DymolaConnectionException("Dymola is not running.")
        self._print_debug_message("Yes")

        self._print_debug_message("Dymola version?")
        version = self.DymolaVersionNumber()
        self._print_debug_message("Version " + str(version) + ".")
        if version != dymola_version:
            self._print_debug_message("Wrong")
            raise DymolaConnectionException("Mismatching Dymola version. The Python interface supports " + str(dymola_version) + " but Dymola was " + str(version) + ".")
        self._print_debug_message("OK")

        self._print_debug_message("Successfully started Dymola.")

    def _is_port_available(self, port):
        # pylint: disable=missing-docstring
        result = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if isPython2:
            try:
                s.bind((self._HOSTNAME, port))
                result = True
            except socket.error:
                result = False
        else:
            try:
                s.bind((self._HOSTNAME, port))
                result = True
            except OSError:
                result = False
        s.close()
        s = None
        return result

    def _find_available_port(self):
        # pylint: disable=missing-docstring
        while True:
            port = random.randint(self._FIRST_AVAILABLE_PORT, self._LAST_AVAILABLE_PORT)
            if self._is_port_available(port):
                return port
        return -1

    def close(self):
        # pylint: disable=missing-docstring
        if self._dymola_process is None:
            return 0
        self._print_debug_message("Closing Dymola...")
        exit_code = -1
        try:
            if self._is_dymola_running():
                self._call_dymola_function("exit", [])
        except DymolaException:
            # exit() will always be without a response and will therefore throw a DymolaException
            pass
        if self._dymola_process is not None:
            exit_code = self._dymola_process.wait()
        if self._dymola_process is not None:
            self._dymola_process.terminate()
            self._dymola_process = None
        self._print_debug_message("Dymola has exited. Return value " + str(exit_code) + ".")
        return exit_code

    def DymolaVersionNumber(self):
        # pylint: disable=missing-docstring,invalid-name
        raise NotImplementedError

    def exit(self):
        # pylint: disable=missing-docstring
        raise NotImplementedError

    def _fix_json_parameter(self, item):
        # pylint: disable=missing-docstring
        result = item
        if type(item) is _NamedArgument:
            value = self._fix_json_parameter(item.named_value)
            value = str(value)
            value = value.replace("'%22", "%22")
            value = value.replace("%22'", "%22")

            tokens = value.split("%22")
            value = ""
            first = True
            outside_string = True
            for token in tokens:
                if not first:
                    value += "%22"
                if outside_string:
                    token = token.replace("[", "{")
                    token = token.replace("]", "}")
                value += token
                first = False
                outside_string = not outside_string

            if value == "True" or value == "False":
                value = value.lower()
            result = item.named_argument + "=" + value
        elif type(item) is _UnquotedString:
            result = item.value
        elif self._type_is_string(item):
            item = self._escape_for_json(item)
            item = item.replace("\\", "\\\\")
            result = "%22" + item + "%22"
        elif type(item) is list:
            result = self._fix_json_parameter_list(item)
        else:
            result = item
        return result

    def _fix_json_parameter_list(self, params):
        # pylint: disable=missing-docstring
        if params is None:
            return None
        newparams = []
        for item in params:
            newparams.append(self._fix_json_parameter(item))
        return newparams

    def _make_json_request(self, cmd, params):
        # pylint: disable=missing-docstring
        params = self._fix_json_parameter_list(params)
        self._rpc_id += 1
        request = { "method": cmd, "params": params, "id": self._rpc_id }
        return json.dumps(request)

    def _make_rpc_call(self, request):
        # pylint: disable=missing-docstring
        attempt_num = 1
        max_attempts = 30
        while True:
            self._print_debug_message("Trying to connect..." + str(attempt_num) + "/" + str(max_attempts))
            conn = HTTPConnection(self._HOSTNAME, self._portnumber)
            if isPython2:
                try:
                    conn.request("POST", url=self._HOSTNAME, body=request)
                    self._print_debug_message("Success")
                    break
                except (EnvironmentError, HTTPException) as ex:
                    self._print_debug_message("Failed. " + str(type(ex)) + " " + str(ex))
                    if conn is not None:
                        conn.close()
                    if attempt_num < max_attempts:
                        attempt_num += 1
                        time.sleep(0.5)
                    else:
                        raise DymolaConnectionException("Failed to connect to Dymola within the given timeout.")
            else:
                try:
                    conn.request("POST", url=self._HOSTNAME, body=request)
                    self._print_debug_message("Success")
                    break
                except (ConnectionError, HTTPException) as ex:
                    self._print_debug_message("Failed. " + str(type(ex)) + " " + str(ex))
                    if conn is not None:
                        conn.close()
                    if attempt_num < max_attempts:
                        attempt_num += 1
                        time.sleep(0.5)
                    else:
                        raise DymolaConnectionException("Failed to connect to Dymola within the given timeout.")

        if conn is None:
            raise DymolaConnectionException("Failed to create connection to Dymola.")

        response = None
        if isPython2:
            try:
                response = conn.getresponse()
            except (EnvironmentError, HTTPException) as ex:
                raise DymolaConnectionException(str(ex))
            finally:
                if conn is not None:
                    conn.close()
        else:
            try:
                response = conn.getresponse()
            except (ConnectionError, HTTPException) as ex:
                raise DymolaConnectionException(str(ex))
            finally:
                if conn is not None:
                    conn.close()

        json_response = response.read()
        json_response = json_response.decode("utf-8")
        return json_response

    def _is_dymola_running(self):
        # pylint: disable=missing-docstring
        result = True
        try:
            request = self._make_json_request("ping", None)
            self._print_debug_message("Request: " + request)
            response = self._make_rpc_call(request)
            self._print_debug_message("Response: " + response)
        except DymolaException:
            result = False
        return result

    def _call_dymola_function(self, cmd, params):
        # pylint: disable=missing-docstring
        request = self._make_json_request(cmd, params)
        self._print_debug_message("Request: " + request)

        response = self._make_rpc_call(request)
        self._print_debug_message("Response: " + response)

        result = None
        try:
            obj = json.loads(response)
            if obj is not None:
                error = obj["error"]
                if error is not None:
                    msg = "Error when calling Dymola function " + cmd
                    self._print_debug_message(msg)
                    raise DymolaFunctionException(msg)
                response_id = obj["id"]
                if type(response_id) is int:
                    if response_id != self._rpc_id:
                        msg = "Mismatch request/response ID in JSON-RPC call."
                        self._print_debug_message(msg)
                        raise DymolaFunctionException(msg)
                result = obj["result"]
        except Exception as ex:
            msg = "Failed to parse JSON response. " + str(ex) + " " + response
            print(msg)
            raise DymolaFunctionException(msg)

        self._print_debug_message("Returning result.")
        return result

    def _parse_response_and_return(self, result, expected_type):
        # pylint: disable=missing-docstring
        ok = False
        if expected_type == "float" and type(result) is float:
            ok = True
        elif expected_type == "int" and type(result) is int:
            ok = True
        elif expected_type == "bool" and type(result) is bool:
            ok = True
        elif expected_type == "str" and self._type_is_string(result):
            ok = True
        elif expected_type == "list" and isinstance(result, list):
            ok = True
        elif expected_type == "list2d" and isinstance(result, list):
            if len(result) > 0 and isinstance(result[0], list):
                ok = True
        if ok:
            return result

        print(("ERROR: Bad return type. Expected " + expected_type + " but got " + str(type(result)) + "."))
        self._print_debug_message("\"" + str(result) + "\"")
        return None
