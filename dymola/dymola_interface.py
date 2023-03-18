# Copyright (c) 2013-2017 Dassault Systemes. All rights reserved.

from dymola.dymola_enums import *
from dymola.dymola_exception import DymolaException
from dymola.dymola_interface_internal import DymolaInterfaceInternal, _NamedArgument, _UnquotedString

class DymolaInterface(DymolaInterfaceInternal):
    """
    This class provides a Python API for accessing the most useful built-in functions in Dymola.
    The API is compatible with **Dymola 2018**.

    An example of usage::

        from dymola.dymola_interface import DymolaInterface
        from dymola.dymola_exception import DymolaException

        dymola = None
        try:
            # Instantiate the Dymola interface and start Dymola
            dymola = DymolaInterface()

            # Call a function in Dymola and check its return value
            result = dymola.simulateModel("Modelica.Mechanics.Rotational.Examples.CoupledClutches")
            if not result:
                print("Simulation failed. Below is the translation log.")
                log = dymola.getLastError()
                print(log)

            dymola.plot(["J1.w", "J2.w", "J3.w", "J4.w"])
            dymola.ExportPlotAsImage("C:/temp/plot.png")
        except DymolaException as ex:
            print("Error: " + str(ex))

        if dymola is not None:
            dymola.close()
            dymola = None

    There is a one-to-one correspondence between the parameters in a Dymola command and the
    parameters in the corresponding Python method. If a parameter has a default value, it is
    shown in the documentation for that parameter. Note that in the Python interface documentation,
    default values and arrays dimensions are formatted as Modelica.

    If you want to execute a command that is not part of the Python interface, you can use the method
    :func:`ExecuteCommand`. It takes a string parameter that can contain any command or
    expression. For example::

        dymola.ExecuteCommand("a=1")

    The command is not type checked so you are responsible for making sure that the command is
    valid. It is not possible to retrieve the output from the command.
    """

    # The version of Dymola that this interface is compatible with.
    __version__ = 2018.0

    _DEFAULT_INSTALL_PATH = "Dymola 2018"

    def __init__(self, dymolapath="", use64bit=True, port=-1, showwindow=False, debug=False, allowremote=False, nolibraryscripts=False):
        """
        Creates a wrapper for Dymola and starts Dymola.
        Uses 64-bit Dymola in the installation that corresponds to this interface.
        The connection is created using the default port number.

        :param str dymolapath: The path to ``Dymola.exe``. Default is an empty string, which means that the path should be auto-detected. 
        :param bool use64bit: If ``True``, the 64-bit Dymola is used. If ``False``, the 32-bit Dymola is used. Default is ``True``.
        :param int port: The port number to use for connecting to Dymola. Default is ``-1``, which means that a port should be auto-assigned.
        :param bool showwindow: This flag controls whether the Dymola window will be visible or not when calling functions in the interface. The default value is ``False``, which means that Dymola will be hidden.
        :param bool debug: For debugging the Dymola Python interface. Note that it is intended for debugging the interface, not Modelica models. Setting this variable to ``True`` outputs debug messages in the console. For advanced users only.
        :param bool allowremote: By default, Dymola only allows local connections. The default value is ``False``. Set this flag to ``True`` to allow access from other machines.
        :param bool nolibraryscripts: Corresponds to the command-line argument with the same name. The default value is ``False``.
        :returns: A Dymola wrapper object.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        DymolaInterfaceInternal._debug = debug
        if not dymolapath:
            exepath = DymolaInterfaceInternal._get_full_dymola_install_path(self._DEFAULT_INSTALL_PATH)
            if use64bit:
                exepath += "/bin64/Dymola.exe"
            else:
                exepath += "/bin/Dymola.exe"
        else:
            exepath = dymolapath
        super(DymolaInterface, self).__init__(dymola_version=DymolaInterface.__version__, dymolapath=exepath, port=port,
                                        showwindow=showwindow, debug=debug, allowremote=allowremote, nolibraryscripts=nolibraryscripts)

    def ExecuteCommand(self, cmd):
        """
        Executes a command in the scripting window. Use this method if you want to execute
        a command that is not part of the Python interface. It takes a string parameter that can
        contain any command or expression. For example::

            dymola.ExecuteCommand("a=1")

        The command is not type checked so you are responsible for making sure that the
        command is valid. It is not possible to retrieve the output from the command. If the
        command failed to execute the error message can be retrieved using :func:`getLastError`.

        :param str cmd: The command to execute.
        :returns: result
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        return super(DymolaInterface, self).ExecuteCommand(cmd)

    def close(self):
        """
        This method exits Dymola gracefully. It calls :func:`exit` and then waits until Dymola
        has terminated before returning. Remember to set the :class:`DymolaInterface` object to
        ``None`` afterwards.
        """
        return super(DymolaInterface, self).close()

    def AddModelicaPath(self, path, erase=False):
        """
        Append the given string to the Modelica path.

        :param str path: The directory.
        :param bool erase: Instead erase from path. Default ``False``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(path)
        params.append(erase)
        self._call_dymola_function("AddModelicaPath", params)

    def animationSetup(self):
        """
        .. raw:: html

           <html><p>The function lists the current animation setup in the Commands window. An example is provided below.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>animationSetup();
           animationRemove(id&nbsp;=&nbsp;1);
           animationPosition(position={20,50,490,370},id=1);
           animationGrid(grid_square&nbsp;=&nbsp;1.0,&nbsp;grid_size&nbsp;=&nbsp;50.0);
           animationView(view&nbsp;=&nbsp;
           [1.0,&nbsp;0.0,&nbsp;0.0,&nbsp;0.0;
           0.0,&nbsp;1.0,&nbsp;0.0,&nbsp;0.0;
           0.0,&nbsp;0.0,&nbsp;1.0,&nbsp;0.0;
           0.0,&nbsp;0.0,&nbsp;0.0,&nbsp;1.0]);
           animationFollow(followFirst&nbsp;=&nbsp;false,&nbsp;followX&nbsp;=&nbsp;true,&nbsp;followY&nbsp;=&nbsp;true,&nbsp;followZ&nbsp;=&nbsp;false,&nbsp;followRotation&nbsp;=&nbsp;false);
           animationViewing(cylinder&nbsp;=&nbsp;false,&nbsp;fillmode&nbsp;=&nbsp;false,&nbsp;unitcube&nbsp;=&nbsp;false,&nbsp;xygrid&nbsp;=&nbsp;false,&nbsp;xzgrid&nbsp;=&nbsp;false,&nbsp;yzgrid&nbsp;=&nbsp;false,&nbsp;perspective&nbsp;=&nbsp;false,&nbsp;antialias&nbsp;=&nbsp;false,&nbsp;continuously&nbsp;=&nbsp;false,&nbsp;axisreference&nbsp;=&nbsp;false,&nbsp;traceall&nbsp;=&nbsp;false);
           animationSelected(name&nbsp;=&nbsp;true,&nbsp;highlight&nbsp;=&nbsp;true,&nbsp;follow&nbsp;=&nbsp;false,&nbsp;trace&nbsp;=&nbsp;true,&nbsp;selectedName&nbsp;=&nbsp;&QUOT;&QUOT;);
           animationFrames(history&nbsp;=&nbsp;0,&nbsp;interval&nbsp;=&nbsp;1,&nbsp;delays&nbsp;=&nbsp;0);
           animationColor(background&nbsp;=&nbsp;{0.75,&nbsp;0.75,&nbsp;0.75},&nbsp;selected&nbsp;=&nbsp;{1.0,&nbsp;0.0,&nbsp;0.0},&nbsp;grid&nbsp;=&nbsp;{0.875,&nbsp;0.875,&nbsp;0.875},&nbsp;selectedbackground&nbsp;=&nbsp;{1.0,&nbsp;1.0,&nbsp;1.0},&nbsp;traceColor&nbsp;=&nbsp;{0.0,&nbsp;0.0,&nbsp;1.0});
           animationVectorScaling(force&nbsp;=&nbsp;0.0,&nbsp;torque&nbsp;=&nbsp;0.0,&nbsp;velocity&nbsp;=&nbsp;0.0,&nbsp;acceleration&nbsp;=&nbsp;0.0,&nbsp;angularvelocity&nbsp;=&nbsp;0.0,&nbsp;angularacceleration&nbsp;=&nbsp;0.0);
           animationOnline(onlineAnimation&nbsp;=&nbsp;false,&nbsp;realtime&nbsp;=&nbsp;false,&nbsp;scaleFactor&nbsp;=&nbsp;1.0,&nbsp;loadInterval&nbsp;=&nbsp;0.5);
           animationSubdivisions(subdivision&nbsp;=&nbsp;{16,&nbsp;8,&nbsp;16,&nbsp;1,&nbsp;1,&nbsp;64,&nbsp;1,&nbsp;1,&nbsp;12,&nbsp;12,&nbsp;6,&nbsp;12,&nbsp;1});
           animationPerspective(perspective&nbsp;=&nbsp;{-40.0,&nbsp;40.0,&nbsp;1.0,&nbsp;100.0,&nbsp;0.0,&nbsp;0.0,&nbsp;-3.0});
           animationSpeed(speed&nbsp;=&nbsp;1.0);
           animationTransparency();
           animationTrace();
           animationRedraw();</pre></html>

        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("animationSetup", params)
        return self._parse_response_and_return(result, "bool")

    def cd(self, Dir=""):
        """
        .. raw:: html

           <html><p>Function to change the current directory or report the current directory. Can be used both with and wihtout parantheses as in the examples below. </p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>Report current directory</p>
           <pre>cd
           cd()
           cd(&QUOT;&QUOT;)</pre>
           <p>Change current directory </p>
           <pre>cd&nbsp;C:/Test/NewDir
           cd&nbsp;(&QUOT;C:/Test/NewDir&QUOT;)</pre>
           <p>Change to parent directory</p>
           <pre>cd ..
           cd(&QUOT;..&QUOT;)</pre></html>

        :param str Dir: Directory to change to. Default ``""``.
        :returns: Cd ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(Dir)
        result = self._call_dymola_function("cd", params)
        return self._parse_response_and_return(result, "bool")

    def checkModel(self, problem, simulate=False, constraint=False):
        """
        .. raw:: html

           <html><p>Check the model validity. This corresponds to <b>Check (Normal)</b> in the menus.</p>
           <p>If <code>simulate=true</code> in the call, associated commands will also be included in the check. The commands will be executed and the model will be simulated with stored simulation setup.</p>
           <p>This corresponds to <b>Check (With simulation)</b> in the menus.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>Check model:</p>
           <pre>checkModel(&QUOT;Modelica.Mechanics.Rotational.Examples.CoupledClutches&QUOT;);</pre>
           <p>Check model and simulate it:</p>
           <pre>checkModel(&QUOT;Modelica.Mechanics.Rotational.Examples.CoupledClutches&QUOT;,simulate=true);</pre></html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch.
        :param bool simulate: Check simulations as well. Default ``False``.
        :param bool constraint: Check as constraining class as well. Default ``False``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(problem)
        params.append(simulate)
        params.append(constraint)
        result = self._call_dymola_function("checkModel", params)
        return self._parse_response_and_return(result, "bool")

    def classDirectory(self):
        """
        Useful for accessing local external files.

        :returns: The directory in which the call resides
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("classDirectory", params)
        return self._parse_response_and_return(result, "str")

    def clear(self, fast=False):
        """
        .. raw:: html

           <html><p>Function to clear exerything, for example the packages loaded in the Package Browser and variables created in the Commands Window.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>clear
           clear()</pre></html>

        :param bool fast: Only clear user classes. Default ``False``.
        :returns: Command ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fast)
        result = self._call_dymola_function("clear", params)
        return self._parse_response_and_return(result, "bool")

    def clearFlags(self):
        """
        Clears flags and integer constants

        :returns: Command ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("clearFlags", params)
        return self._parse_response_and_return(result, "bool")

    def clearlog(self):
        """
        .. raw:: html

           <html><p>Function to clear the history in the Commands Window.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>clearlog
           clearlog()</pre></html>

        :returns: Command ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("clearlog", params)
        return self._parse_response_and_return(result, "bool")

    def clearPlot(self, Id=0):
        """
        Erases curves and annotations in the diagram.

        :param int Id: Identity of window (0-means last). Default ``0``.
        :returns: true of successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(Id)
        result = self._call_dymola_function("clearPlot", params)
        return self._parse_response_and_return(result, "bool")

    def createPlot(self, Id=None, position=None, x=None, y=None, heading=None, Range=None, erase=None, autoscale=None, autoerase=None, autoreplot=None, description=None, grid=None, color=None, online=None, legend=None, timeWindow=None, filename=None, legendLocation=None, legendHorizontal=None, legendFrame=None, supressMarker=None, logX=None, logY=None, legends=None, subPlot=None, uniformScaling=None, leftTitleType=None, leftTitle=None, bottomTitleType=None, bottomTitle=None, colors=None, patterns=None, markers=None, thicknesses=None, range2=None, logY2=None, rightTitleType=None, rightTitle=None, axes=None, timeUnit=None, displayUnits=None, showOriginal=None, showDifference=None):
        """
        .. raw:: html

           <html><p>Create a plot window with all settings.</p>
           <p>This built-in function contains a number of input parameters also used in other built-in functions documented below. All parameters are output parameters except the last one. Some parameters are further commented in notes below the table.</p>
           <p>Note that if having a plot already, the command <b>File &GT; Generate Script&hellip; &GT; Plot setup</b> will produce a script (.mos) file with relevant flags and the corresponding <code>createPlot</code> function call for the plot. Note the additional setting <b>Include result filenames</b>.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>To illustrate how <code>createPlot</code> might look like (and also some flags from plot), use the command <b>File &GT; Demos</b> to open the model Coupled clutches, then use the command <b>Commands &GT; Simulate and Plot</b> to get a plot window.</p>
           <p>Now use the command <b>File &GT; Generate Script&hellip; &GT; Plot setup</b> to save a script (.mos) file. (There is also a setting <b>Include result filenames</b>, ticking this setting gives an extra line; see comment in the script below.) Give it a name, e. g. PlotTest, and keep the default directory for saving. Note what directory that is.</p>
           <p>Finding the file and opening it in the Dymola script editor (or in e.g. Notepad) will display:</p>
           <pre>  // Script generated by Dymola Wed Dec 02 10:48:17 2015
           // Plot commands
           removePlots(false);
           Advanced.FilenameInLegend = false;
           Advanced.SequenceInLegend = true;
           Advanced.PlotLegendTooltip = true;
           Advanced.FullPlotTooltip = true;
           Advanced.DefaultAutoErase = true;
           Advanced.Legend.Horizontal = true;
           Advanced.Legend.Frame = false;
           Advanced.Legend.Transparant = true;
           Advanced.Legend.Location = 1;
           Advanced.FilesToKeep = 2;
           createPlot(id = 1,
           position = {15, 10, 584, 421},
           y = {"J1.w", "J2.w", "J3.w", "J4.w"},
           range = {0.0, 1.2000000000000002, -2.0, 11.0},
           grid = true,
           filename = "dsres.mat", (only if Include result filenames is set)
           colors = {{28,108,200}, {238,46,47}, {0,140,72},  {217,67,180}});</pre>
           <h4><span style="color: #008000">Python Example</span></h4>
           <pre>dymola.createPlot(Id=1, position=[15, 10, 584, 421], y=[&quot;J1.w&quot;, &quot;J2.w&quot;, &quot;J3.w&quot;, &quot;J4.w&quot;], Range=[0.0, 1.5, -1.0, 11.0], grid=True, colors=[[28,108,200], [238,46,47], [0,140,72], [217,67,180]])</pre>
           </html>

        :param int Id: Window id. Default ``0``.
        :param int[] position: Window position (x0, y0, inner width, inner height). Dimension ``[4]``. Default ``[15, 10, 400, 283]``.
        :param str x: Independent variable. Default ``"time"``.
        :param str[] y: Variables. Dimension ``[:]``. Default ``fill("", 0)``.
        :param str heading: Plot heading. Use the command plotHeading to create a rich text heading. Default ``""``.
        :param float[] Range: Range. Dimension ``[4]``. Default ``[0.0, 1.0, 0.0, 1.0]``.
        :param bool erase: Start with a fresh window. Default ``True``.
        :param bool autoscale: Autoscaling of y-axis. Default ``True``.
        :param bool autoerase: Erase plot when loading new file after simulation. Default ``True``.
        :param bool autoreplot: Automatically replot after simulation. Default ``True``.
        :param bool description: Include description in label. Default ``False``.
        :param bool grid: Add grid. Default ``False``.
        :param bool color: Deprecated. Replaced by colors, patterns, markers, and thicknesses. Default ``True``.
        :param bool online: Online plotting. Default ``False``.
        :param bool legend: Variable legend. Default ``True``.
        :param float timeWindow: Time window for online plotting. Default ``0.0``.
        :param str filename: Result file to read data from. Default ``""``.
        :param int legendLocation: Where to place legend (1 above, 2 right, 3 below, 4-7 inside). Default ``1``.
        :param bool legendHorizontal: Horizontal legend. Default ``True``.
        :param bool legendFrame: Draw frame around legend. Default ``False``.
        :param bool supressMarker: Deprecated. Replaced by colors, patterns, markers, and thicknesses. Default ``False``.
        :param bool logX: Logarithmic X scale. Default ``False``.
        :param bool logY: Logarithmic Y scale. Default ``False``.
        :param str[] legends: Legends. Dimension ``[size(y, 1)]``. Default ``fill("", size(y, 1))``.
        :param int subPlot: Sub plot number. Default ``1``.
        :param bool uniformScaling: Same vertical and horizontal axis increment. Default ``False``.
        :param int leftTitleType: Type of left axis title (0=none, 1=description, 2=custom). Default ``1``.
        :param str leftTitle: Custom left axis title. Default ``""``.
        :param int bottomTitleType: Type of bottom axis title (0=none, 1=description, 2=custom). Default ``1``.
        :param str bottomTitle: Custom bottom axis title. Default ``""``.
        :param int[][] colors: Line colors. Dimension ``[size(y, 1), 3]``. Default ``fill({-1, -1, -1}, size(y, 1))``.
        :param int[] patterns: Line patterns, e.g., LinePattern.Solid. Dimension ``[size(y, 1)]``. Default ``fill(LinePattern.Solid, size(y, 1))``. Enumeration.
        :param int[] markers: Line markers, e.g., MarkerStyle.Cross. Dimension ``[size(y, 1)]``. Default ``fill(-1, size(y, 1))``. Enumeration.
        :param float[] thicknesses: Line thicknesses. Dimension ``[size(y, 1)]``. Default ``fill(0.25, size(y, 1))``.
        :param float[] range2: Range, right vertical axis. Dimension ``[2]``. Default ``[0.0, 1.0]``.
        :param bool logY2: Logarithmic right Y scale. Default ``False``.
        :param int rightTitleType: Type of right axis title (0=none, 1=description, 2=custom). Default ``1``.
        :param str rightTitle: Custom right axis title. Default ``""``.
        :param int[] axes: Vertical axes, 1=left, 2=right. Dimension ``[size(y, 1)]``. Default ``fill(1, size(y, 1))``.
        :param str timeUnit: Time unit. Default ``"s"``.
        :param str[] displayUnits: Display units. Empty string means use the default display unit. Dimension ``[size(y, 1)]``. Default ``fill("", size(y, 1))``.
        :param bool showOriginal: When enabled, original curves are shown. Default ``True``.
        :param bool showDifference: When enabled, the difference between curves is shown. Default ``False``.
        :returns: _window
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if Id is not None:
            params.append(_NamedArgument("id", Id))
        if position:
            params.append(_NamedArgument("position", position))
        if x is not None:
            params.append(_NamedArgument("x", x))
        if y:
            params.append(_NamedArgument("y", y))
        if heading is not None:
            params.append(_NamedArgument("heading", heading))
        if Range:
            params.append(_NamedArgument("range", Range))
        if erase is not None:
            params.append(_NamedArgument("erase", erase))
        if autoscale is not None:
            params.append(_NamedArgument("autoscale", autoscale))
        if autoerase is not None:
            params.append(_NamedArgument("autoerase", autoerase))
        if autoreplot is not None:
            params.append(_NamedArgument("autoreplot", autoreplot))
        if description is not None:
            params.append(_NamedArgument("description", description))
        if grid is not None:
            params.append(_NamedArgument("grid", grid))
        if color is not None:
            params.append(_NamedArgument("color", color))
        if online is not None:
            params.append(_NamedArgument("online", online))
        if legend is not None:
            params.append(_NamedArgument("legend", legend))
        if timeWindow is not None:
            params.append(_NamedArgument("timeWindow", timeWindow))
        if filename is not None:
            params.append(_NamedArgument("filename", filename))
        if legendLocation is not None:
            params.append(_NamedArgument("legendLocation", legendLocation))
        if legendHorizontal is not None:
            params.append(_NamedArgument("legendHorizontal", legendHorizontal))
        if legendFrame is not None:
            params.append(_NamedArgument("legendFrame", legendFrame))
        if supressMarker is not None:
            params.append(_NamedArgument("supressMarker", supressMarker))
        if logX is not None:
            params.append(_NamedArgument("logX", logX))
        if logY is not None:
            params.append(_NamedArgument("logY", logY))
        if legends:
            params.append(_NamedArgument("legends", legends))
        if subPlot is not None:
            params.append(_NamedArgument("subPlot", subPlot))
        if uniformScaling is not None:
            params.append(_NamedArgument("uniformScaling", uniformScaling))
        if leftTitleType is not None:
            params.append(_NamedArgument("leftTitleType", leftTitleType))
        if leftTitle is not None:
            params.append(_NamedArgument("leftTitle", leftTitle))
        if bottomTitleType is not None:
            params.append(_NamedArgument("bottomTitleType", bottomTitleType))
        if bottomTitle is not None:
            params.append(_NamedArgument("bottomTitle", bottomTitle))
        if colors:
            params.append(_NamedArgument("colors", colors))
        if patterns:
            params.append(_NamedArgument("patterns", patterns))
        if markers:
            params.append(_NamedArgument("markers", markers))
        if thicknesses:
            params.append(_NamedArgument("thicknesses", thicknesses))
        if range2:
            params.append(_NamedArgument("range2", range2))
        if logY2 is not None:
            params.append(_NamedArgument("logY2", logY2))
        if rightTitleType is not None:
            params.append(_NamedArgument("rightTitleType", rightTitleType))
        if rightTitle is not None:
            params.append(_NamedArgument("rightTitle", rightTitle))
        if axes:
            params.append(_NamedArgument("axes", axes))
        if timeUnit is not None:
            params.append(_NamedArgument("timeUnit", timeUnit))
        if displayUnits:
            params.append(_NamedArgument("displayUnits", displayUnits))
        if showOriginal is not None:
            params.append(_NamedArgument("showOriginal", showOriginal))
        if showDifference is not None:
            params.append(_NamedArgument("showDifference", showDifference))
        result = self._call_dymola_function("createPlot", params)
        return self._parse_response_and_return(result, "int")

    def DefaultModelicaVersion(self, version, forceUpgrade):
        """
        .. raw:: html

           <html><p>Set the default Modelica Version in Dymola. Also available in &QUOT;<b>Edit &GT; Options... &GT; Version &GT; Modelica version</b>&QUOT;</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>To set Modelica version 3.2.2 as default version and force upgrade of models to this version execute:</p>
           <pre>DefaultModelicaVersion(&QUOT;3.2.2&QUOT;,&nbsp;true);</pre></html>

        :param str version: 
        :param bool forceUpgrade: 
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(version)
        params.append(forceUpgrade)
        self._call_dymola_function("DefaultModelicaVersion", params)

    def document(self, _function):
        """
        Write calling syntax for named function, or descripting for flag.

        :param str _function: Name of built-in function or flag.
        :returns: true if successful (i.e. function or flag exists)
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(_function)
        result = self._call_dymola_function("document", params)
        return self._parse_response_and_return(result, "bool")

    def DymolaVersion(self):
        """
        .. raw:: html

           <html><p><code>DymolaVersion()</code> returns the full version number and date of Dymola as a String<code>. </code></p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>In Dymola 2014 FD01</p>
           <pre>DymolaVersion();
           &nbsp;=&nbsp;&QUOT;Dymola&nbsp;Version&nbsp;2014&nbsp;FD01&nbsp;(64-bit),&nbsp;2013-10-17&QUOT;</pre></html>

        :returns: version
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("DymolaVersion", params)
        return self._parse_response_and_return(result, "str")

    def DymolaVersionNumber(self):
        """
        .. raw:: html

           <html><p><code>DymolaVersionNumber()</code> returns the version number of Dymola as a Real number.</p>
           <p>The decimal value is used to indicate if it is a main version (=0) or a FD version (=1 etc.) </p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>In Dymola 2014</p>
           <pre>DymolaVersionNumber();
           &nbsp;=&nbsp;2014.0</pre>
           <p>In Dymola 2014 FD01 </p>
           <pre>DymolaVersionNumber();
           &nbsp;=&nbsp;2014.1 </pre></html>

        :returns: versionNumber
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("DymolaVersionNumber", params)
        return self._parse_response_and_return(result, "float")

    def eraseClasses(self, classnames_):
        """
        .. raw:: html

           <html><p>Function to erase the given models. It requires that no models outside of this list depend on them. This is not primarily an interactive function, but designed to be called by other controlling and changing models. Corresponds to <b>Delete</b> in the Package Browser.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>eraseClasses({&QUOT;model1&QUOT;,&QUOT;PackageA.model2&QUOT;})</pre>
           <p>will erase the listed models from the Package Browser.</p></html>

        :param str[] classnames_: List of classes to erase. Dimension ``[:]``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if classnames_:
            params.append(classnames_)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        result = self._call_dymola_function("eraseClasses", params)
        return self._parse_response_and_return(result, "bool")

    def Execute(self, File):
        """
        .. raw:: html

           <html><p>Function to execute a file/command.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>Execute(&QUOT;test.bat&QUOT;)</pre>
           <p>executes the batch file <code>test.bat</code> in the current directory.</p></html>

        :param str File: 
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(File)
        result = self._call_dymola_function("Execute", params)
        return self._parse_response_and_return(result, "bool")

    def existTrajectoryNames(self, fileName, names):
        """
        .. raw:: html

           <html><p>Check if the provided names exists in the trajectory file.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating the example <b>File &GT; Demos &GT; Coupled clutches</b> the result file <i>CoupledClutches.mat</i> should be available in the current dir. </p>
           <p>Executing</p>
           <pre>existTrajectoryNames(&QUOT;CoupledClutches.mat&QUOT;,&nbsp;{&QUOT;J1.w&QUOT;,&nbsp;&QUOT;J2.w&QUOT;,&nbsp;&QUOT;J10.w&QUOT;});
           ={true, true, false}</pre>
           <p>indicates that <code>J1.w</code> and <code>J2.w</code> but not <code>J10.w</code> exists in the trajectory file.</p></html>

        :param str fileName: File containing a trajectory, e.g. dsres.mat.
        :param str[] names: Potential names in trajectory file. Dimension ``[:]``.
        :returns: Indicator for the names
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        if names:
            params.append(names)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        result = self._call_dymola_function("existTrajectoryNames", params)
        return self._parse_response_and_return(result, "list")

    def exit(self, status=0):
        """
        .. raw:: html

           <html><p>Function to exit Dymola from script.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>exit
           exit()</pre></html>
        :param int status:  Default ``0``.
        """
        try:
            params = []
            params.append(status)
            self._call_dymola_function("exit", params)
        except DymolaException:
            pass  # normal

    def experiment(self, StartTime=0.0, StopTime=1.0, NumberOfIntervals=0, OutputInterval=0.0, Algorithm="", Tolerance=0.0001, FixedStepSize=0.0):
        """
        Set up default experiment

        :param float StartTime: Start of simulation. Default ``0.0``.
        :param float StopTime: End of simulation. Default ``1.0``.
        :param int NumberOfIntervals: Number of output points. Default ``0``.
        :param float OutputInterval: Distance between output points. Default ``0.0``.
        :param str Algorithm: Integration method. Default ``""``.
        :param float Tolerance: Tolerance of integration. Default ``0.0001``.
        :param float FixedStepSize: Fixed step size for Euler. Default ``0.0``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(StartTime)
        params.append(StopTime)
        params.append(NumberOfIntervals)
        params.append(OutputInterval)
        params.append(Algorithm)
        params.append(Tolerance)
        params.append(FixedStepSize)
        result = self._call_dymola_function("experiment", params)
        return self._parse_response_and_return(result, "bool")

    def experimentGetOutput(self):
        """
        .. raw:: html

           <html><p>Return the current simulation output setup as an array of booleans.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>experimentGetOutput()
           ={false, false, true, true, true, true, true, true, true, false}</pre></html>

        :returns: Textual storage
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("experimentGetOutput", params)
        return self._parse_response_and_return(result, "list")

    def experimentSetupOutput(self, textual=False, doublePrecision=False, states=True, derivatives=True, inputs=True, outputs=True, auxiliaries=True, equidistant=True, events=True, debug=False):
        """
        .. raw:: html

           <html><p>Setup the simulation output, corresponds to the <b>Format</b>, <b>Store</b> and <b>Output selection</b> sections in <b>Simulation &GT; Setup... &GT; Output</b>.</p></html>

        :param bool textual: Textual storage. Default ``False``.
        :param bool doublePrecision: Double precision. Default ``False``.
        :param bool states: Store state variables. Default ``True``.
        :param bool derivatives: Store derivative variables. Default ``True``.
        :param bool inputs: Store input variables. Default ``True``.
        :param bool outputs: Store outputs variables. Default ``True``.
        :param bool auxiliaries: Store auxiliary variables. Default ``True``.
        :param bool equidistant: Store equidistantly. Default ``True``.
        :param bool events: Store variables at events. Default ``True``.
        :param bool debug: Write log messages. Default ``False``.
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(textual)
        params.append(doublePrecision)
        params.append(states)
        params.append(derivatives)
        params.append(inputs)
        params.append(outputs)
        params.append(auxiliaries)
        params.append(equidistant)
        params.append(events)
        params.append(debug)
        result = self._call_dymola_function("experimentSetupOutput", params)
        return self._parse_response_and_return(result, "bool")

    def exportAnimation(self, path, width=-1, height=-1):
        """
        Export an animation to file. Supported file formats are AVI (only on Windows), VRML (wrl), and X3D.
        The file format is determined by the file extension. Use wrl as file extension for VRML.
        If there is more than one animation window, the last window is used.

        :param str path: File path. Supported file formats are AVI (only on Windows), VRML (wrl), and X3D.
        :param int width: Width. Only applicable for X3D. Default ``-1``.
        :param int height: Height. Only applicable for X3D. Default ``-1``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(path)
        params.append(width)
        params.append(height)
        result = self._call_dymola_function("exportAnimation", params)
        return self._parse_response_and_return(result, "bool")

    def exportDiagram(self, path, width=400, height=400, trim=True):
        """
        Export the diagram layer to file. Supported file formats are PNG and SVG.
        The file format is determined by the file extension. To export in SVG, the diagram layer must exist.

        :param str path: File path. Supported file formats are PNG and SVG.
        :param int width: Width. Default ``400``.
        :param int height: Height. Default ``400``.
        :param bool trim: Remove unnecessary space around the image. Default ``True``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(path)
        params.append(width)
        params.append(height)
        params.append(trim)
        result = self._call_dymola_function("exportDiagram", params)
        return self._parse_response_and_return(result, "bool")

    def exportDocumentation(self, path, className=""):
        """
        Export the documentation for a model to an HTML file.

        :param str path: File path. Supported file format is HTML.
        :param str className: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch. Default ``""``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(path)
        params.append(className)
        result = self._call_dymola_function("exportDocumentation", params)
        return self._parse_response_and_return(result, "bool")

    def exportEquations(self, path):
        """
        Export the equations to file. Supported file formats are PNG and MathML.
        The file format is determined by the file extension. Use mml as file extension for MathML.

        :param str path: File path. Supported file formats are PNG and MathML (mml).
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(path)
        result = self._call_dymola_function("exportEquations", params)
        return self._parse_response_and_return(result, "bool")

    def exportIcon(self, path, width=80, height=80, trim=True):
        """
        Export the icon layer to file. Supported file formats are PNG and SVG.
        The file format is determined by the file extension. To export in SVG, the icon layer must exist.

        :param str path: File path. Supported file formats are PNG and SVG.
        :param int width: Width. Default ``80``.
        :param int height: Height. Default ``80``.
        :param bool trim: Remove unnecessary space around the image. Default ``True``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(path)
        params.append(width)
        params.append(height)
        params.append(trim)
        result = self._call_dymola_function("exportIcon", params)
        return self._parse_response_and_return(result, "bool")

    def exportInitial(self, dsName, scriptName, exportAllVariables, exportSimulator):
        """
        .. raw:: html

           <html><p>The function generates a Modelica script, such that running the script re-creates the simulation setup. After running the generated script it is possible to override specific parameters or start-values before simulating. By generating a script from a &ldquo;steady-state&rdquo; dsfinal.txt it is possible to perform parameter studies from that point.</p>
           <p><b>Note:</b> This cannot be combined with non-standard setting of fixed for variables if <code>dsName=&QUOT;dsin.txt&QUOT;</code>. All other cases work fine.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>exportInitial(&QUOT;dsin.txt&QUOT;,&nbsp;&QUOT;scripInitial.mos&QUOT;)</pre></html>

        :param str dsName: 
        :param str scriptName: 
        :param bool exportAllVariables: 
        :param bool exportSimulator: 
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(dsName)
        params.append(scriptName)
        params.append(exportAllVariables)
        params.append(exportSimulator)
        result = self._call_dymola_function("exportInitial", params)
        return self._parse_response_and_return(result, "bool")

    def exportInitialDsin(self, scriptName):
        """
        Generate a copy of internal dsin.txt

        :param str scriptName: 
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(scriptName)
        result = self._call_dymola_function("exportInitialDsin", params)
        return self._parse_response_and_return(result, "bool")

    def ExportPlotAsImage(self, fileName, Id=-1, includeInLog=True, onlyActiveSubplot=True):
        """
        .. raw:: html

           <html><p>Export (save) a plot window as an image. The image can only be saved in .png format. The parameter id specifies what plot window will be saved. The default -1 means the first (lowest number) plot window in the Dymola main window. The <code>includeInLog</code> specifies whether the plot should be included in the command log. </p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p><pre>ExportPlotAsImage(E:/MyExperiment/Plots/Plot3.png, id=3)</pre> </p>
           <p>will save the plot window Plot[3] as the image Plot3.png in the folder E:\MyExperiment\Plots. It will also be saved in the command log.</p></html>

        :param str fileName: The path to save the plot. Supported file formats are PNG and SVG.
        :param int Id: ID of the plot window to export. -1 means last plot window. Default ``-1``.
        :param bool includeInLog: Include image in command log. Default ``True``.
        :param bool onlyActiveSubplot: Include all subplots or only the active subplot. Default ``True``.
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(Id)
        params.append(includeInLog)
        params.append(onlyActiveSubplot)
        result = self._call_dymola_function("ExportPlotAsImage", params)
        return self._parse_response_and_return(result, "bool")

    def getClassText(self, fullName, includeAnnotations=False, formatted=False):
        """
        Returns the Modelica text for a given model.

        :param str fullName: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch.
        :param bool includeAnnotations: Include annotations. Default ``False``.
        :param bool formatted: If the text should be returned as HTML or plain text. Default ``False``.
        :returns: The Modelica text. (``str``), true if the model is read-only. (``bool``)
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fullName)
        params.append(includeAnnotations)
        params.append(formatted)
        result = self._call_dymola_function("getClassText", params)
        return self._parse_response_and_return(result, "list")

    def getExperiment(self):
        """
        Get current experiment setting

        :returns: Start of simulation (``float``), End of simulation (``float``) (``float``), Number of output points (``int``) (``int``), Distance between output points (``float``) (``float``), Integration method (``str``) (``str``), Tolerance of integration (``float``) (``float``), Fixed step size for Euler (``float``)
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("getExperiment", params)
        return self._parse_response_and_return(result, "list")

    def getLastError(self):
        """
        .. raw:: html

           <html><p>Returns the last error. If the last command was successful an empty string is returned. For check, translate, etc, the log is returned.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>translateModel(&QUOT;Modelica.Mechanics.Rotational.Examples.CoupledClutches&QUOT;);
           getLastError()
           &nbsp;=&nbsp;&QUOT;Warning:&nbsp;Undeclared&nbsp;variable&nbsp;or&nbsp;command:&nbsp;Modelica.Constants.g_n
           Warning:&nbsp;Undeclared&nbsp;variable&nbsp;or&nbsp;command:&nbsp;Modelica.Constants.g_n
           Error:&nbsp;Failed&nbsp;to&nbsp;write&nbsp;dsin.txt.
           Translation&nbsp;of&nbsp;&LT;a&nbsp;href=\&QUOT;Modelica://Modelica.Mechanics.Rotational.Examples.CoupledClutches\&QUOT;&GT;Modelica.Mechanics.Rotational.Examples.CoupledClutches&LT;/a&GT;:
           The&nbsp;DAE&nbsp;has&nbsp;106&nbsp;scalar&nbsp;unknowns&nbsp;and&nbsp;106&nbsp;scalar&nbsp;equations.
           &nbsp;
           Statistics
           &nbsp;
           Original&nbsp;Model
           &nbsp;&nbsp;Number&nbsp;of&nbsp;components:&nbsp;14
           &nbsp;&nbsp;Variables:&nbsp;182
           &nbsp;&nbsp;Constants:&nbsp;23&nbsp;(23&nbsp;scalars)
           &nbsp;&nbsp;Parameters:&nbsp;53&nbsp;(56&nbsp;scalars)
           &nbsp;&nbsp;Unknowns:&nbsp;106&nbsp;(106&nbsp;scalars)
           &nbsp;&nbsp;Differentiated&nbsp;variables:&nbsp;14&nbsp;scalars
           &nbsp;&nbsp;Equations:&nbsp;98
           &nbsp;&nbsp;&nbsp;&nbsp;Nontrivial&nbsp;:&nbsp;79
           Translated&nbsp;Model
           &nbsp;&nbsp;Constants:&nbsp;38&nbsp;scalars
           &nbsp;&nbsp;Free&nbsp;parameters:&nbsp;39&nbsp;scalars
           &nbsp;&nbsp;Parameter&nbsp;depending:&nbsp;3&nbsp;scalars
           &nbsp;&nbsp;Continuous&nbsp;time&nbsp;states:&nbsp;8&nbsp;scalars
           &nbsp;&nbsp;Time-varying&nbsp;variables:&nbsp;51&nbsp;scalars
           &nbsp;&nbsp;Alias&nbsp;variables:&nbsp;54&nbsp;scalars
           &nbsp;&nbsp;Number&nbsp;of&nbsp;mixed&nbsp;real/discrete&nbsp;systems&nbsp;of&nbsp;equations:&nbsp;1
           &nbsp;&nbsp;Sizes&nbsp;of&nbsp;linear&nbsp;systems&nbsp;of&nbsp;equations:&nbsp;{13}
           &nbsp;&nbsp;Sizes&nbsp;after&nbsp;manipulation&nbsp;of&nbsp;the&nbsp;linear&nbsp;systems:&nbsp;{4}
           &nbsp;&nbsp;Sizes&nbsp;of&nbsp;nonlinear&nbsp;systems&nbsp;of&nbsp;equations:&nbsp;{&nbsp;}
           &nbsp;&nbsp;Sizes&nbsp;after&nbsp;manipulation&nbsp;of&nbsp;the&nbsp;nonlinear&nbsp;systems:&nbsp;{&nbsp;}
           &nbsp;&nbsp;Number&nbsp;of&nbsp;numerical&nbsp;Jacobians:&nbsp;0
           &nbsp;
           Selected&nbsp;continuous&nbsp;time&nbsp;states
           Statically&nbsp;selected&nbsp;continuous&nbsp;time&nbsp;states
           &nbsp;&nbsp;clutch1.phi_rel
           &nbsp;&nbsp;clutch1.w_rel
           &nbsp;&nbsp;clutch2.phi_rel
           &nbsp;&nbsp;clutch2.w_rel
           &nbsp;&nbsp;clutch3.phi_rel
           &nbsp;&nbsp;clutch3.w_rel
           &nbsp;&nbsp;J1.phi
           &nbsp;&nbsp;J1.w
           &QUOT;</pre></html>

        :returns: The error message from the last command.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        result = self._call_dymola_function("getLastError", params)
        return self._parse_response_and_return(result, "str")

    def importFMU(self, fileName, includeAllVariables=True, integrate=True, promptReplacement=False, packageName=""):
        """
        .. raw:: html

           <html><p>Imports an FMU, i. e. unzips, XSL transforms the model description and opens the resulting Modelica model. Note: The model description file from any previous import is replaced. This also applies to the binary library files.</p>
           <p>This built-in function corresponds to the command <b>File &GT; Import &GT; FMU&hellip;</b>.</p>
           <p>For more information, please see the manual &ldquo;Dymola User Manual Volume 2&rdquo;, chapter 6 &ldquo;Other Simulation Environments&rdquo;, section &ldquo;FMI Support in Dymola&rdquo;.</p>
           <p>Note: For big models it is recommended to set<code> includeAllVariables=false </code>to avoid the Modelica wrapper becoming huge.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>importFMU(&QUOT;C:/test/Modelica_Mechanics_Rotational_Examples_CoupledClutches.fmu&QUOT;,&nbsp;true,&nbsp;true,&nbsp;false,&nbsp;&QUOT;&QUOT;);</pre></html>

        :param str fileName: The FMU file.
        :param bool includeAllVariables: Include other variables than inputs, outputs and parameters. Default ``True``.
        :param bool integrate: Integrate outside the FMU, set to false for co-simulation. Default ``True``.
        :param bool promptReplacement: Prompt for name and save location when importing. Default ``False``.
        :param str packageName: Name of package to insert FMU in. Default ``""``.
        :returns: True if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(includeAllVariables)
        params.append(integrate)
        params.append(promptReplacement)
        params.append(packageName)
        result = self._call_dymola_function("importFMU", params)
        return self._parse_response_and_return(result, "bool")

    def importInitial(self, dsName="dsfinal.txt"):
        """
        .. raw:: html

           <html><p>This function sets up integration or linearization to start from the initial conditions given in the file specified (including start and stop-time and choice of integration algorithm). The default is &ldquo;dsfinal.txt&rdquo;.</p>
           <p>(Calling the function<code> importInitial </code>with the (unchanged) default file, followed by calling the function <code>simulate</code> corresponds to the command <b>Simulation &GT; Continue &GT; Continue</b>. The function <code>simulate</code> works like <code>simulateModel</code>, but works with the default model.)</p>
           <p>After calling<code> importInitial </code>it is possible to override specific parameters or start-values before simulating by using the usual parameter setting in the variable browser.</p>
           <p>Calling the function <code>importInitial</code> with a text file that differs from the unchanged default file corresponds to the command <b>Simulation &GT; Continue &GT; Import Initial&hellip;</b>.</p>
           <p>Please see the section &ldquo;Simulation &GT; Continue &GT; Import Initial&hellip;&rdquo; in the User Manual for more additional important information.</p>
           <p>Note: Basically <code>importInitial()</code> corresponds to copying dsfinal.txt (the default variable output file containing variable values etc. at the end of the simulation) to dsin.txt (the default variable input file for a simulation run). Please compare the command below.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>importInitial(&QUOT;C:/test/dsfinal.txt&QUOT;);</pre></html>

        :param str dsName:  Default ``"dsfinal.txt"``.
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(dsName)
        result = self._call_dymola_function("importInitial", params)
        return self._parse_response_and_return(result, "bool")

    def importInitialResult(self, dsResName, atTime):
        """
        .. raw:: html

           <html><p>This function is similar to<code> importInitial</code>, with the following exceptions:</p>
           <ul>
           <li>The start value file has to be specified, and it has to be a simulation result, i.e. a file that you can plot/animate.</li>
           <li>The start time has to be specified.</li>
           <li>The integration method will be the one presently selected.</li>
           </ul>
           <p>Concerning other information, please see <code>importInitial</code>.</p></html>

        :param str dsResName: 
        :param float atTime: 
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(dsResName)
        params.append(atTime)
        result = self._call_dymola_function("importInitialResult", params)
        return self._parse_response_and_return(result, "bool")

    def initialized(self, allVars=False, isInitialized=True):
        """
        .. raw:: html

           <html><p>This function sets states and parameters to fixed and all other variables to free. It is used before setting initial values for states and parameters. <code>isInitialized=true</code> is default (and corresponds to continuing a simulation). If false it will initialize according to the initial equations at the start of the simulation.</p></html>

        :param bool allVars:  Default ``False``.
        :param bool isInitialized:  Default ``True``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(allVars)
        params.append(isInitialized)
        self._call_dymola_function("initialized", params)

    def interpolateTrajectory(self, fileName, signals, times):
        """
        .. raw:: html

           <html><p>Interpolates multiple variables from a trajectory file. This is useful for post-processing of simulations results: comparison with references, plotting, etc.</p></html>

        :param str fileName: File containing a trajectory, e.g. dsres.mat.
        :param str[] signals: Vector of variable names, in Modelica-syntax, e.g a[1].b. Dimension ``[:]``.
        :param float[] times: The time-points to interpolate at; most efficient if increasing. Dimension ``[:]``.
        :returns: Interpolated values
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        if signals:
            params.append(signals)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        if times:
            params.append(times)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        result = self._call_dymola_function("interpolateTrajectory", params)
        return self._parse_response_and_return(result, "list2d")

    def linearizeModel(self, problem="", startTime=0.0, stopTime=1.0, numberOfIntervals=0, outputInterval=0.0, method="Dassl", tolerance=0.0001, fixedstepsize=0.0, resultFile="dslin"):
        """
        .. raw:: html

           <html><p>The function translates a model (if not done previously) and then calculates a linearized model at the initial values. The linearized model is by default stored in the Dymola working directory in Matlab format as the file <code>dslin.mat</code>.</p>
           <p>This built-in function corresponds to the command <b>Simulation &GT; Linearize</b>. For more information about the content of the dslin.mat file and handling of linearization, please see the section about that command, section &ldquo;Simulation &GT; Linearize&rdquo; in Dymola User Manual. In particular note how to linearize around other values than the initial ones (the corresponding parameters in the function cannot be used to change the time-point of linearization).</p></html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch. Default ``""``.
        :param float startTime: Start of simulation. Default ``0.0``.
        :param float stopTime: End of simulation. Default ``1.0``.
        :param int numberOfIntervals: Number of output points. Default ``0``.
        :param float outputInterval: Distance between output points. Default ``0.0``.
        :param str method: Integration method. Default ``"Dassl"``.
        :param float tolerance: Tolerance of integration. Default ``0.0001``.
        :param float fixedstepsize: Fixed step size for Euler. Default ``0.0``.
        :param str resultFile: Where to store result. Default ``"dslin"``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(problem)
        params.append(startTime)
        params.append(stopTime)
        params.append(numberOfIntervals)
        params.append(outputInterval)
        params.append(method)
        params.append(tolerance)
        params.append(fixedstepsize)
        params.append(resultFile)
        result = self._call_dymola_function("linearizeModel", params)
        return self._parse_response_and_return(result, "bool")

    def list(self, filename="", variables=["*"]):
        """
        .. raw:: html

           <html><p>Writes a list of interactive variables and their values to the screen (or file). The list includes both interactive variables, and interactive setting of translator switches such as Evaluate.</p>
           <p>The function lists (on screen or to a file) the interactive variables in the variable workspace with their type and value. Predefined variables are also described by a comment. Also interactive settings of translator switches such as Evaluate are listed. </p>
           <p>The output from the function is in alphabethical order, and grouped. </p>
           <p>The wildcards * and ? are supported.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <ul>
           <li><code>list(variables={&QUOT;A*&QUOT;})</code> &ndash; lists all items starting with A. </li>
           <li><code>list(variables={&QUOT;Advanced.*&QUOT;})</code> &ndash; lists all items starting with <code>Advanced.</code> &ndash; that is, list all Advanced flags settings.</li>
           <li><code>list(variables={&QUOT;*Output*&QUOT;})</code> &ndash; lists all items containing<code> Output</code> in the text.</li>
           </ul>
           <p>It is possible to write the variables to a script file (which can be executed) <code>filename=&QUOT;script.mos&QUOT;</code>, and limit it to certain variables by using <code>variables={&QUOT;var1&QUOT;,&QUOT;var2&QUOT;}</code>.</p></html>

        :param str filename:  Default ``""``.
        :param str[] variables: Select a subset of the variables. Wildcards * and ? may be used. Dimension ``[:]``. Default ``["*"]``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(filename)
        if variables:
            params.append(variables)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        self._call_dymola_function("list", params)

    def listfunctions(self, filter="*"):
        """
        Writes a list of built-in functions and their descriptions to the screen.

        :param str filter: Select a subset of the functions. Wildcards * and ? may be used. Default ``"*"``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(filter)
        self._call_dymola_function("listfunctions", params)

    def loadAnimation(self, fileName, Id=0, together=False):
        """
        .. raw:: html

           <html><p>Load animation data from result file in animation window.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>loadAnimation(&QUOT;resultFile.mat&QUOT;,&nbsp;2);</pre>
           <p>loads the animation data (if available) from <code>resultFile.mat </code>in the animation window with <code>id=2</code> (second animation window opened).</p>
           <pre>loadAnimation(&QUOT;otherResultFile.mat&QUOT;,&nbsp;2, true);</pre>
           <p>loads the animation in the same windows as the previous command (window #2) keeping the old animation in the window. Both animations (from <code>resultFile.mat</code> and <code>otherResultFile.mat</code>) will be in the same animation window.</p></html>

        :param str fileName: 
        :param int Id: New window if zero else number of window. Default ``0``.
        :param bool together: Similar to Animate together. Default ``False``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(Id)
        params.append(together)
        self._call_dymola_function("loadAnimation", params)

    def openModel(self, path, mustRead=True, changeDirectory=True):
        """
        .. raw:: html

           <html><p>Reads the file specified by <code>path</code>, for example <code>openModel(path=&QUOT;E:\Experiments\MyLib.mo&QUOT;)</code>, and displays its window. This corresponds to<b> File &GT; Open</b> in the menus. Note: This will automatically change directory to the right directory.</p>
           <p><code>mustRead=false</code> means that if the file already is opened/read, it is not opened/read again. If <code>mustRead=true</code> in such a case the user is promted for removing the present one and open it again. The default value <code>false</code> can be useful in scriping, when only wanting to assure that a certain file has been read.</p></html>

        :param str path: File-path to open.
        :param bool mustRead: If false we can skip reading the file. Default ``True``.
        :param bool changeDirectory: If true (default) we automatically change to the directory of the file. Default ``True``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(path)
        params.append(mustRead)
        params.append(changeDirectory)
        result = self._call_dymola_function("openModel", params)
        return self._parse_response_and_return(result, "bool")

    def openModelFile(self, modelName, path="", version=""):
        """
        Opens a Modelica-file and pops up a window with the given model in it

        :param str modelName: Model to open.
        :param str path: File-path to open (can be the empty string). Default ``""``.
        :param str version: Version to open (can be the empty string). Default ``""``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(modelName)
        params.append(path)
        params.append(version)
        result = self._call_dymola_function("openModelFile", params)
        return self._parse_response_and_return(result, "bool")

    def plot(self, y, legends=None, plotInAll=None, colors=None, patterns=None, markers=None, thicknesses=None, axes=None):
        """
        .. raw:: html

           <html><p>Plot the given variables in the plot window. It is currently not possible to set ranges or independent variable.</p>
           <p>Note: the argument is a vector of strings; the names correspond to the names when selecting variables in the plot window. Subcomponents are accessed by dot-notation.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After running <b>File &GT; Demos &GT; Coupled clutches</b>, the function call</p>
           <pre>plot({&QUOT;J1.w&QUOT;, &QUOT;J2.w&QUOT;}, colors={{28,108,200}, {238,46,47}},
           patterns={LinePattern.Dash, LinePattern.Solid},
           markers={MarkerStyle.None, MarkerStyle.Cross},
           thicknesses={0.5, 0.25},
           axes={1, 2});</pre>
           <p>plots <code>J1.w</code> and <code>J2.w</code>.</p></html>

        :param str[] y: Variables. Dimension ``[:]``.
        :param str[] legends: Legends. Dimension ``[size(y, 1)]``. Default ``fill("", size(y, 1))``.
        :param bool plotInAll: Plot variable from all files. Default ``False``.
        :param int[][] colors: Line colors. Dimension ``[size(y, 1), 3]``. Default ``fill({-1, -1, -1}, size(y, 1))``.
        :param int[] patterns: Line patterns, e.g., LinePattern.Solid. Dimension ``[size(y, 1)]``. Default ``fill(-1, size(y, 1))``. Enumeration.
        :param int[] markers: Line markers, e.g., MarkerStyle.Cross. Dimension ``[size(y, 1)]``. Default ``fill(-1, size(y, 1))``. Enumeration.
        :param float[] thicknesses: Line thicknesses. Dimension ``[size(y, 1)]``. Default ``fill(0.25, size(y, 1))``.
        :param int[] axes: Vertical axes, 1=left, 2=right. Dimension ``[size(y, 1)]``. Default ``fill(1, size(y, 1))``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if y:
            params.append(_NamedArgument("y", y))
        if legends:
            params.append(_NamedArgument("legends", legends))
        if plotInAll is not None:
            params.append(_NamedArgument("plotInAll", plotInAll))
        if colors:
            params.append(_NamedArgument("colors", colors))
        if patterns:
            params.append(_NamedArgument("patterns", patterns))
        if markers:
            params.append(_NamedArgument("markers", markers))
        if thicknesses:
            params.append(_NamedArgument("thicknesses", thicknesses))
        if axes:
            params.append(_NamedArgument("axes", axes))
        result = self._call_dymola_function("plot", params)
        return self._parse_response_and_return(result, "bool")

    def plotArray(self, x, y, style=0, legend="", Id=0, color=[-1, -1, -1], pattern=LinePattern.Solid, marker=-1, thickness=0.25, erase=True, axis=1, unit=""):
        """
        .. raw:: html

           <html><p>X-y plot for plotting of data computed in functions or scripts. For plot of arrays, please see the function <code>plotArrays</code>.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>plotArray(x=1:10,y=sin(1:10), pattern=LinePattern.Dash,
           marker=MarkerStyle.Cross,color={0,128,0},thickness=0.5, axis=2,
           legend=&QUOT;Plotted data&QUOT;);</pre>
           <h4><span style="color: #008000;">Python example</span></h4>
           <pre>x_val= [1,2,3,4,5,6,7,8,9,10]
           y_val = []
           for i in x_val:
           y_val.append(math.sin(i))
           <span style="color: #008c48;"># Using enumerations LinePattern.Dash and MarkerStyle.Cross requires import of dymola.dymola_enums</span>
           dymola.plotArray(x=x_val, y=y_val, pattern=LinePattern.Dash, marker=MarkerStyle.Cross, color=[0,128,0], thickness=0.5, axis=2, legend=&quot;Plotted data&quot;)</pre>
           </html>

        :param float[] x: X-values. Dimension ``[:]``.
        :param float[] y: Y-values. Dimension ``[size(x, 1)]``.
        :param int style: Deprecated. Replaced by color, pattern, marker, and thickness. Default ``0``.
        :param str legend: Legend describing plotted data. Default ``""``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :param int[] color: Line color. Dimension ``[3]``. Default ``[-1, -1, -1]``.
        :param int pattern: Line pattern, e.g., LinePattern.Solid. Default ``LinePattern.Solid``. Enumeration.
        :param int marker: Line marker, e.g., MarkerStyle.Cross. Default ``-1``. Enumeration.
        :param float thickness: Line thickness. Default ``0.25``.
        :param bool erase: Erase window content before plotting. Default ``True``.
        :param int axis: Vertical axis, 1=left, 2=right. Default ``1``.
        :param str unit: Unit. If the string has the format 'unit|displayunit' it sets the display unit too. For example, 'rad|deg'. Default ``""``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if x:
            params.append(x)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        if y:
            params.append(y)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        params.append(style)
        params.append(legend)
        params.append(Id)
        if color:
            params.append(color)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        params.append(pattern)
        params.append(marker)
        params.append(thickness)
        params.append(erase)
        params.append(axis)
        params.append(unit)
        result = self._call_dymola_function("plotArray", params)
        return self._parse_response_and_return(result, "bool")

    def plotArrays(self, x, y, style=None, legend=None, Id=None, title=None, colors=None, patterns=None, markers=None, thicknesses=None, axes=None, units=None):
        """
        .. raw:: html

           <html><p>X-y plot for plotting of data computed in functions or scripts. Note similarity with the function <code>plotArray</code>. </p>
           <p>(The input style[:] is deprecated.)</p></html>

        :param float[] x: X-values. Dimension ``[:]``.
        :param float[][] y: Y-values. Dimension ``[size(x, 1), :]``.
        :param int[] style: Deprecated. Replaced by colors, patterns, markers, and thicknesses. Dimension ``[:]``. Default ``[0]``.
        :param str[] legend: Legends describing plotted data. Dimension ``[:]``. Default ``[""]``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :param str title: Plot heading. Use the command plotHeading to create a rich text plot heading. Default ``""``.
        :param int[][] colors: Line colors. Dimension ``[size(y, 2), 3]``. Default ``fill({-1, -1, -1}, size(y, 2))``.
        :param int[] patterns: Line patterns, e.g., LinePattern.Solid. Dimension ``[size(y, 2)]``. Default ``fill(LinePattern.Solid, size(y, 2))``. Enumeration.
        :param int[] markers: Line markers, e.g., MarkerStyle.Cross. Dimension ``[size(y, 2)]``. Default ``fill(MarkerStyle.None, size(y, 2))``. Enumeration.
        :param float[] thicknesses: Line thicknesses. Dimension ``[size(y, 2)]``. Default ``fill(0.25, size(y, 2))``.
        :param int[] axes: Vertical axes, 1=left, 2=right. Dimension ``[size(y, 2)]``. Default ``fill(1, size(y, 2))``.
        :param str[] units: Units. Dimension ``[size(y, 2)]``. Default ``fill("", size(y, 2))``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if x:
            params.append(_NamedArgument("x", x))
        if y:
            params.append(_NamedArgument("y", y))
        if style:
            params.append(_NamedArgument("style", style))
        if legend:
            params.append(_NamedArgument("legend", legend))
        if Id is not None:
            params.append(_NamedArgument("id", Id))
        if title is not None:
            params.append(_NamedArgument("title", title))
        if colors:
            params.append(_NamedArgument("colors", colors))
        if patterns:
            params.append(_NamedArgument("patterns", patterns))
        if markers:
            params.append(_NamedArgument("markers", markers))
        if thicknesses:
            params.append(_NamedArgument("thicknesses", thicknesses))
        if axes:
            params.append(_NamedArgument("axes", axes))
        if units:
            params.append(_NamedArgument("units", units))
        self._call_dymola_function("plotArrays", params)

    def plotExpression(self, mapFunction, eraseOld=False, expressionName="", Id=0, axis=1):
        """
        .. raw:: html

           <html><p>The function plots an expression in a specified plot window. </p>
           <p>The <code>expressionName</code> is the description string of the expression; it will be displayed as the label of the expression. The <code>id</code> is the identity of the plot window, where &ldquo;0&rdquo; is the last window, -1 the second last etc.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>plotExpression(apply(CoupledClutches[end].J1.w+CoupledClutches[end-1].J1.w), false,
           &QUOT;CoupledClutches[end].J1.w+CoupledClutches[end-1].J1.w&QUOT;, 1);</pre></html>

        :param str mapFunction: apply expression.
        :param bool eraseOld: if true, erase old plot content. Default ``False``.
        :param str expressionName: Legend describing plotted data. Default ``""``.
        :param int Id:  Default ``0``.
        :param int axis: Vertical axis, 1=left, 2=right. Default ``1``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if not mapFunction.startswith("apply"):
            mapFunction = "apply(" + mapFunction + ")"
        params.append(_UnquotedString(mapFunction))
        params.append(eraseOld)
        params.append(expressionName)
        params.append(Id)
        params.append(axis)
        result = self._call_dymola_function("plotExpression", params)
        return self._parse_response_and_return(result, "bool")

    def plotHeading(self, textString=None, fontSize=None, fontName=None, lineColor=None, textStyle=None, horizontalAlignment=None, Id=None):
        """
        .. raw:: html

           <html><p>This function creates a heading in a plot window. An empty string as <code>textstring</code> removes the heading.
           <code>fontSize=0</code> means that the default base font size is used. For more about font size, and about <code>textStyle</code> and
           <code>horizontalAlignment</code>, see the function <code>plotText</code>.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>plotHeading(textString=&QUOT;Coupled Clutches
           w plots&QUOT;,fontSize=12, lineColor={28,108,200}, textStyle={TextStyle.Bold, TextStyle.Italic});</pre>
           </html>

        :param str textString: Text string. An empty string removes the heading. Default ``""``.
        :param int fontSize: Font size. A zero value means that the default base font size is used. Default ``0``.
        :param str fontName: Font family. An empty string means that the default font family is used. Default ``""``.
        :param int[] lineColor: Text color. Dimension ``[3]``. Default ``[0, 0, 0]``.
        :param int[] textStyle: Text style. Available values are TextStyle.Bold, TextStyle.Italic, and TextStyle.UnderLine. Dimension ``[:]``. Default ``fill(TextStyle.Bold, 0)``. Enumeration.
        :param int horizontalAlignment: Horizontal alignment. Available values are TextAlignment.Left, TextAlignment.Center, TextAlignment.Right. Default ``TextAlignment.Center``. Enumeration.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if textString is not None:
            params.append(_NamedArgument("textString", textString))
        if fontSize is not None:
            params.append(_NamedArgument("fontSize", fontSize))
        if fontName is not None:
            params.append(_NamedArgument("fontName", fontName))
        if lineColor:
            params.append(_NamedArgument("lineColor", lineColor))
        if textStyle:
            params.append(_NamedArgument("textStyle", textStyle))
        if horizontalAlignment is not None:
            params.append(_NamedArgument("horizontalAlignment", horizontalAlignment))
        if Id is not None:
            params.append(_NamedArgument("id", Id))
        result = self._call_dymola_function("plotHeading", params)
        return self._parse_response_and_return(result, "bool")

    def plotParametricCurve(self, x, y, s, xName="", yName="", sName="", legend="", Id=0, color=[-1, -1, -1], pattern=LinePattern.Solid, marker=-1, thickness=0.25, labelWithS=False, erase=True, axis=1):
        """
        .. raw:: html

           <html><p>The function plots a curve defined by a parameter; the x(s) &ndash; y(s) plot.</p>
           <p><code>labelWithS</code> will present parameter labels in the curve if set to true, it corresponds to the context menu command Parameter Labels.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>s=0:0.1:10
           y={sin(t)*exp(-0.1*t) for t in s}
           x={cos(t)*exp(-0.1*t) for t in s}
           plotParametricCurve(x,y,s,labelWithS=true);</pre></html>

        :param float[] x: x(s) values. Dimension ``[:]``.
        :param float[] y: y(s) values. Dimension ``[size(x, 1)]``.
        :param float[] s: s values. Dimension ``[size(x, 1)]``.
        :param str xName: The name of the x variable. Default ``""``.
        :param str yName: The name of the y variable. Default ``""``.
        :param str sName: The name of the s parameter. Default ``""``.
        :param str legend: Legend describing plotted data. Default ``""``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :param int[] color: Line color. Dimension ``[3]``. Default ``[-1, -1, -1]``.
        :param int pattern: Line pattern, e.g., LinePattern.Solid. Default ``LinePattern.Solid``. Enumeration.
        :param int marker: Line marker, e.g., MarkerStyle.Cross. Default ``-1``. Enumeration.
        :param float thickness: Line thickness. Default ``0.25``.
        :param bool labelWithS: if true, output values of s along the curve. Default ``False``.
        :param bool erase: Erase window content before plotting. Default ``True``.
        :param int axis: Vertical axis, 1=left, 2=right. Default ``1``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if x:
            params.append(x)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        if y:
            params.append(y)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        if s:
            params.append(s)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        params.append(xName)
        params.append(yName)
        params.append(sName)
        params.append(legend)
        params.append(Id)
        if color:
            params.append(color)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        params.append(pattern)
        params.append(marker)
        params.append(thickness)
        params.append(labelWithS)
        params.append(erase)
        params.append(axis)
        result = self._call_dymola_function("plotParametricCurve", params)
        return self._parse_response_and_return(result, "bool")

    def plotParametricCurves(self, x, y, s, xName=None, yName=None, sName=None, legends=None, Id=None, colors=None, patterns=None, markers=None, thicknesses=None, labelWithS=None, axes=None):
        """
        .. raw:: html

           <html><p>The function plots curves defined by x(s) &ndash; y(s). The function is an extension of the function <code>plotParametricCurve</code>, covering multiple curves.</p></html>

        :param float[][] x: x(s) vectors. Dimension ``[:, size(s, 1)]``.
        :param float[][] y: y(s) vectors. Dimension ``[size(x, 1), size(s, 1)]``.
        :param float[] s: s values. Dimension ``[:]``.
        :param str xName: The name of the x variable. Default ``""``.
        :param str yName: The name of the y variable. Default ``""``.
        :param str sName: The name of the s parameter. Default ``""``.
        :param str[] legends: Legends describing plotted data. Dimension ``[:]``. Default ``fill("", size(y, 1))``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :param int[][] colors: Line colors. Dimension ``[size(y, 1), 3]``. Default ``fill({-1, -1, -1}, size(y, 1))``.
        :param int[] patterns: Line patterns, e.g., LinePattern.Solid. Dimension ``[size(y, 1)]``. Default ``fill(LinePattern.Solid, size(y, 1))``. Enumeration.
        :param int[] markers: Line markers, e.g., MarkerStyle.Cross. Dimension ``[size(y, 1)]``. Default ``fill(MarkerStyle.None, size(y, 1))``. Enumeration.
        :param float[] thicknesses: Line thicknesses. Dimension ``[size(y, 1)]``. Default ``fill(0.25, size(y, 1))``.
        :param bool labelWithS: if true, output values of s along the curve. Default ``False``.
        :param int[] axes: Vertical axes, 1=left, 2=right. Dimension ``[size(y, 1)]``. Default ``fill(1, size(y, 1))``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if x:
            params.append(_NamedArgument("x", x))
        if y:
            params.append(_NamedArgument("y", y))
        if s:
            params.append(_NamedArgument("s", s))
        if xName is not None:
            params.append(_NamedArgument("xName", xName))
        if yName is not None:
            params.append(_NamedArgument("yName", yName))
        if sName is not None:
            params.append(_NamedArgument("sName", sName))
        if legends:
            params.append(_NamedArgument("legends", legends))
        if Id is not None:
            params.append(_NamedArgument("id", Id))
        if colors:
            params.append(_NamedArgument("colors", colors))
        if patterns:
            params.append(_NamedArgument("patterns", patterns))
        if markers:
            params.append(_NamedArgument("markers", markers))
        if thicknesses:
            params.append(_NamedArgument("thicknesses", thicknesses))
        if labelWithS is not None:
            params.append(_NamedArgument("labelWithS", labelWithS))
        if axes:
            params.append(_NamedArgument("axes", axes))
        self._call_dymola_function("plotParametricCurves", params)

    def plotSignalDifference(self, variablePath, startTime=0, stopTime=0, axis=1, Id=0):
        """
        Plots the discrete difference of a signal, defined as y(i)=u(i)-u(i-1).

        :param str variablePath: Variable path or legend name.
        :param float startTime: Start time. Default ``0``.
        :param float stopTime: Stop time (if equal to start time the full time range is used). Default ``0``.
        :param int axis: Vertical axis (0=left, 1=right). Default ``1``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(variablePath)
        params.append(startTime)
        params.append(stopTime)
        params.append(axis)
        params.append(Id)
        self._call_dymola_function("plotSignalDifference", params)

    def plotSignalOperator(self, variablePath, signalOperator, startTime, stopTime, period=0.0, Id=0):
        """
        .. raw:: html

           <html><p>The function plots a signal operator in the active diagram of a plot window. The following signal operators are presently available:</p>
           <pre>  <b>Signal operators:</b>
           SignalOperator.Min
           SignalOperator.Max
           SignalOperator.ArithmeticMean
           SignalOperator.RectifiedMean
           SignalOperator.RMS
           SignalOperator.ACCoupledRMS
           SignalOperator.SlewRate</pre>
           <p>Note that First Harmonic and Total Harmonic Distortion are not supported by this function, please see next function.</p>
           <p>The <code>id</code> is the identity of the plot window, where &ldquo;0&rdquo; is the last window, -1 the second last etc.</p>
           <p>The variable must be plotted for this command to work.</p>
           <p>The resulting signal operator is displayed in the plot, and the numerical result is output as <code>result</code>.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After running <b>File &GT; Demos &GT; Coupled clutches</b> by <b>Commands &GT; Simulate and Plot</b> and then plotting <code>J1.a</code></p>
           <pre>plotSignalOperator(&QUOT;J1.a&QUOT;, SignalOperator.RectifiedMean, 0.8, 1.2, 1);
           = 5.075379430627545</pre></html>

        :param str variablePath: Variable path or legend name.
        :param int signalOperator: Signal operator. See enumeration :class:`SignalOperator <dymola.dymola_enums.SignalOperator>` for available operators. Enumeration.
        :param float startTime: Start time.
        :param float stopTime: Stop time.
        :param float period: Obsolete. Use function plotSignalOperatorHarmonic for First Harmonic and Total Harmonic Distortion. Default ``0.0``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :returns: Returns the value of the signal operator
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(variablePath)
        params.append(signalOperator)
        params.append(startTime)
        params.append(stopTime)
        params.append(period)
        params.append(Id)
        result = self._call_dymola_function("plotSignalOperator", params)
        return self._parse_response_and_return(result, "float")

    def plotSignalOperatorHarmonic(self, variablePath, signalOperator, startTime, stopTime, period, intervalLength, window, harmonicNo, Id=0):
        """
        .. raw:: html

           <html><p>The function plots a signal operator in the active diagram of a plot window.</p>
           <p>Note, the package SignalOperators must be present in the package browser to be able to execute this function. The package can be opened by e.g. <code>import SignalOperators</code>.</p>
           <p>The following signal operators are presently supported for this function:</p>
           <pre>  SignalOperator.FirstHarmonic
           SignalOperator.THD</pre>
           <p>Compare with the function <code>plotSignalOperator</code> that supports other signal operators.</p>
           <p>The <code>window</code> is the windowing function for FFT, it can be set to any of</p>
           <pre>  SignalOperators.Windows.Windowing.Rectangular
           SignalOperators.Windows.Windowing.Hamming
           SignalOperators.Windows.Windowing.Hann
           SignalOperators.Windows.Windowing.FlatTop</pre>
           <p>The <code>harmonicNo</code> is the relevant harmonic number.</p>
           <p>The <code>id</code> is the identity of the plot window, where &ldquo;0&rdquo; is the last window, -1 the second last etc.</p>
           <p>The resulting signal operator is displayed in the plot, and the numerical result is output as <code>result</code>.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating <b>File &GT; Demos &GT; Coupled clutches</b> and plotting <code>J1.a</code></p>
           <pre>plotSignalOperatorHarmonic(&QUOT;J1.a&QUOT;, SignalOperator.FirstHarmonic, 0.8, 1.2, 0.2, 1e-3, SignalOperators.Windows.Windowing.Rectangular, 1);
           =&nbsp;9.313418460891956</pre></html>

        :param str variablePath: Variable path or legend name.
        :param int signalOperator: Signal operator. See enumeration :class:`SignalOperator <dymola.dymola_enums.SignalOperator>` for available operators. Enumeration.
        :param float startTime: Start time.
        :param float stopTime: Stop time.
        :param float period: Period length.
        :param float intervalLength: Sampling interval length.
        :param int window: Windowing function for FFT. Enumeration.
        :param float harmonicNo: Relevant harmonic number.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :returns: Returns the value of the signal operator
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(variablePath)
        params.append(signalOperator)
        params.append(startTime)
        params.append(stopTime)
        params.append(period)
        params.append(intervalLength)
        params.append(window)
        params.append(harmonicNo)
        params.append(Id)
        result = self._call_dymola_function("plotSignalOperatorHarmonic", params)
        return self._parse_response_and_return(result, "float")

    def plotText(self, extent, textString, fontSize=None, fontName=None, lineColor=None, textStyle=None, horizontalAlignment=None, Id=None):
        """
        .. raw:: html

           <html><p>Insert a text object in the active diagram. The text is rendered using diagram coordinates.</p>
           <p>&ldquo;Null-extent&rdquo; (both coordinates in the extent being the same) is possible; the text will be centered on the specific point.</p>
           p>If the fontSize attribute is 0 the text is scaled to fit its extents, otherwise the size specifies the absolute size. However, if a minimum font size is set; that size will be the smallest font size. This implies that to create a useful &ldquo;null-extent&rdquo; text, the minimum font size should be set. For setting of minimum font size, please see previous chapter, the command <b>Edit &GT; Options, Appearance</b> tab, the setting Restrict minimum font size.</p>
           <p>All installed fonts on the computer are supported.</p>
           <p>Available <code>textStyle</code> values are (by default none of these are activated)</p>
           <pre>TextStyle.Bold
           TextStyle.Italic
           TextStyle.UnderLine</pre>
           <p>Available <code>horizontalAlignment</code> values are (by default the text is centered)</p>
           <pre>TextAlignment.Left
           TextAlignment.Center
           TextAlignment.Right</pre>
           <p>The text is vertically centered in the extent.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>The text &ldquo;Note!&rdquo; is inserted in a plot using </p>
           <pre>plotText(extent={{0.85,13},{0.85,13}},textString=&QUOT;Note!&QUOT;, lineColor={255,0,0},textStyle={TextStyle.Italic,TextStyle.UnderLine},fontName=&QUOT;Courier&QUOT;);</pre></html>

        :param float[][] extent: Extent. Dimension ``[2, 2]``.
        :param str textString: Text string.
        :param int fontSize: Font size. Default ``0``.
        :param str fontName: Font family. Default ``""``.
        :param int[] lineColor: Text color. Dimension ``[3]``. Default ``[0, 0, 0]``.
        :param int[] textStyle: Text style. Available values are TextStyle.Bold, TextStyle.Italic, and TextStyle.UnderLine. Dimension ``[:]``. Default ``fill(TextStyle.Bold, 0)``. Enumeration.
        :param int horizontalAlignment: Horizontal alignment. Available values are TextAlignment.Left, TextAlignment.Center, TextAlignment.Right. Default ``TextAlignment.Center``. Enumeration.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if extent:
            params.append(_NamedArgument("extent", extent))
        params.append(_NamedArgument("textString", textString))
        if fontSize is not None:
            params.append(_NamedArgument("fontSize", fontSize))
        if fontName is not None:
            params.append(_NamedArgument("fontName", fontName))
        if lineColor:
            params.append(_NamedArgument("lineColor", lineColor))
        if textStyle:
            params.append(_NamedArgument("textStyle", textStyle))
        if horizontalAlignment is not None:
            params.append(_NamedArgument("horizontalAlignment", horizontalAlignment))
        if Id is not None:
            params.append(_NamedArgument("id", Id))
        result = self._call_dymola_function("plotText", params)
        return self._parse_response_and_return(result, "bool")

    def plotWindowSetup(self, _window):
        """
        .. raw:: html

           <html><p>Generate a <code>createPlot()</code> command of the plot window given by <code>_id</code>.</p></html>

        :param int _window: 
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(_window)
        result = self._call_dymola_function("plotWindowSetup", params)
        return self._parse_response_and_return(result, "bool")

    def printPlot(self, y, legends=None, plotInAll=None, colors=None, patterns=None, markers=None, thicknesses=None, axes=None):
        """
        .. raw:: html

           <html><p>Plot the variables and furthermore prints the resulting plot on the default printer.</p></html>

        :param str[] y: Variables. Dimension ``[:]``.
        :param str[] legends: Legends. Dimension ``[size(y, 1)]``. Default ``fill("", size(y, 1))``.
        :param bool plotInAll: Plot variable from all files. Default ``False``.
        :param int[][] colors: Line colors. Dimension ``[size(y, 1), 3]``. Default ``fill({-1, -1, -1}, size(y, 1))``.
        :param int[] patterns: Line patterns, e.g., LinePattern.Solid. Dimension ``[size(y, 1)]``. Default ``fill(-1, size(y, 1))``. Enumeration.
        :param int[] markers: Line markers, e.g., MarkerStyle.Cross. Dimension ``[size(y, 1)]``. Default ``fill(-1, size(y, 1))``. Enumeration.
        :param float[] thicknesses: Line thicknesses. Dimension ``[size(y, 1)]``. Default ``fill(0.25, size(y, 1))``.
        :param int[] axes: Vertical axes, 1=left, 2=right. Dimension ``[size(y, 1)]``. Default ``fill(1, size(y, 1))``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if y:
            params.append(_NamedArgument("y", y))
        if legends:
            params.append(_NamedArgument("legends", legends))
        if plotInAll is not None:
            params.append(_NamedArgument("plotInAll", plotInAll))
        if colors:
            params.append(_NamedArgument("colors", colors))
        if patterns:
            params.append(_NamedArgument("patterns", patterns))
        if markers:
            params.append(_NamedArgument("markers", markers))
        if thicknesses:
            params.append(_NamedArgument("thicknesses", thicknesses))
        if axes:
            params.append(_NamedArgument("axes", axes))
        result = self._call_dymola_function("printPlot", params)
        return self._parse_response_and_return(result, "bool")

    def printPlotArray(self, x, y, style=0, legend="", Id=0, color=[-1, -1, -1], pattern=LinePattern.Solid, marker=-1, thickness=0.25, erase=True, axis=1, unit=""):
        """
        .. raw:: html

           <html><p>Plot the variables using <code>plotArray</code> and furthermore prints the resulting plot on the default printer.</p></html>

        :param float[] x: X-values. Dimension ``[:]``.
        :param float[] y: Y-values. Dimension ``[size(x, 1)]``.
        :param int style: Deprecated. Replaced by color, pattern, marker, and thickness. Default ``0``.
        :param str legend: Legend describing plotted data. Default ``""``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :param int[] color: Line color. Dimension ``[3]``. Default ``[-1, -1, -1]``.
        :param int pattern: Line pattern, e.g., LinePattern.Solid. Default ``LinePattern.Solid``. Enumeration.
        :param int marker: Line marker, e.g., MarkerStyle.Cross. Default ``-1``. Enumeration.
        :param float thickness: Line thickness. Default ``0.25``.
        :param bool erase: Erase window content before plotting. Default ``True``.
        :param int axis: Vertical axis, 1=left, 2=right. Default ``1``.
        :param str unit: Unit. If the string has the format 'unit|displayunit' it sets the display unit too. For example, 'rad|deg'. Default ``""``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if x:
            params.append(x)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        if y:
            params.append(y)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        params.append(style)
        params.append(legend)
        params.append(Id)
        if color:
            params.append(color)
        else:
            params.append(_UnquotedString("fill(0, 0)"))
        params.append(pattern)
        params.append(marker)
        params.append(thickness)
        params.append(erase)
        params.append(axis)
        params.append(unit)
        result = self._call_dymola_function("printPlotArray", params)
        return self._parse_response_and_return(result, "bool")

    def printPlotArrays(self, x, y, style=None, legend=None, Id=None, title=None, colors=None, patterns=None, markers=None, thicknesses=None, axes=None, units=None):
        """
        .. raw:: html

           <html><p>Plot the variables using <code>plotArrays</code> and furthermore prints the resulting plot on the default printer.</p></html>

        :param float[] x: X-values. Dimension ``[:]``.
        :param float[][] y: Y-values. Dimension ``[size(x, 1), :]``.
        :param int[] style: Deprecated. Replaced by colors, patterns, markers, and thicknesses. Dimension ``[:]``. Default ``[0]``.
        :param str[] legend: Legends describing plotted data. Dimension ``[:]``. Default ``[""]``.
        :param int Id: Identity of window (0-means last). Default ``0``.
        :param str title: Plot heading. Use the command plotHeading to create a rich text plot heading. Default ``""``.
        :param int[][] colors: Line colors. Dimension ``[size(y, 2), 3]``. Default ``fill({-1, -1, -1}, size(y, 2))``.
        :param int[] patterns: Line patterns, e.g., LinePattern.Solid. Dimension ``[size(y, 2)]``. Default ``fill(LinePattern.Solid, size(y, 2))``. Enumeration.
        :param int[] markers: Line markers, e.g., MarkerStyle.Cross. Dimension ``[size(y, 2)]``. Default ``fill(MarkerStyle.None, size(y, 2))``. Enumeration.
        :param float[] thicknesses: Line thicknesses. Dimension ``[size(y, 2)]``. Default ``fill(0.25, size(y, 2))``.
        :param int[] axes: Vertical axes, 1=left, 2=right. Dimension ``[size(y, 2)]``. Default ``fill(1, size(y, 2))``.
        :param str[] units: Units. Dimension ``[size(y, 2)]``. Default ``fill("", size(y, 2))``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if x:
            params.append(_NamedArgument("x", x))
        if y:
            params.append(_NamedArgument("y", y))
        if style:
            params.append(_NamedArgument("style", style))
        if legend:
            params.append(_NamedArgument("legend", legend))
        if Id is not None:
            params.append(_NamedArgument("id", Id))
        if title is not None:
            params.append(_NamedArgument("title", title))
        if colors:
            params.append(_NamedArgument("colors", colors))
        if patterns:
            params.append(_NamedArgument("patterns", patterns))
        if markers:
            params.append(_NamedArgument("markers", markers))
        if thicknesses:
            params.append(_NamedArgument("thicknesses", thicknesses))
        if axes:
            params.append(_NamedArgument("axes", axes))
        if units:
            params.append(_NamedArgument("units", units))
        self._call_dymola_function("printPlotArrays", params)

    def readMatrix(self, fileName, matrixName, rows, columns):
        """
        .. raw:: html

           <html><p>Read a matrix from a file. The file must either be a Matlab v4-file or a textual file.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating the example <b>File &GT; Demos &GT; Coupled clutches</b> the result file <i>CoupledClutches.mat</i> should be available in the current dir. </p>
           <pre>readMatrixSize(&QUOT;CoupledClutches.mat&QUOT;,&nbsp;&QUOT;data_2&QUOT;)
           ={63,1522}</pre>
           <p>returns the size of the <code>data_2</code> matrix in the file <code>CoupledClutches.mat</code>, which is a 63 x 1522 matrix. This information is needed when calling <code>readMatrix</code>.</p>
           <pre>data=readMatrix(&QUOT;CoupledClutches.mat&QUOT;,&nbsp;&QUOT;data_2&QUOT;,&nbsp;63,&nbsp;1522)
           Declaring&nbsp;variable:&nbsp;Real&nbsp;data&nbsp;[63,&nbsp;1522];</pre>
           <p>to read the data_2 matrix and store it in the variable <code>data</code>.</p></html>

        :param str fileName: File containing the matrix, e.g. A.mat, dsin.txt.
        :param str matrixName: Name of the matrix on the file.
        :param int rows: Number of rows of the matrix - see :func:`readMatrixSize`.
        :param int columns: Number of column of the matrix - see :func:`readMatrixSize`.
        :returns: matrix
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(matrixName)
        params.append(rows)
        params.append(columns)
        result = self._call_dymola_function("readMatrix", params)
        return self._parse_response_and_return(result, "list2d")

    def readMatrixSize(self, fileName, matrixName):
        """
        .. raw:: html

           <html><p>Read the size of a matrix from a file. The file must either be a Matlab v4-file or a textual file. Can be used to declare the size of matrix returned by readMatrix</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating the example <b>File &GT; Demos &GT; Coupled clutches</b> the result file <i>CoupledClutches.mat</i> should be available in the current dir. </p>
           <pre>readMatrixSize(&QUOT;CoupledClutches.mat&QUOT;,&nbsp;&QUOT;data_2&QUOT;)
           ={63,1522}</pre>
           <p>returns the size of the <code>data_2</code> matrix in the file <code>CoupledClutches.mat</code>, which is a 63 x 1522 matrix.</p></html>

        :param str fileName: File containing the matrix, e.g. A.mat, dsin.txt.
        :param str matrixName: Name of the matrix on the file.
        :returns: Number of rows and columns of the matrix
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(matrixName)
        result = self._call_dymola_function("readMatrixSize", params)
        return self._parse_response_and_return(result, "list")

    def readStringMatrix(self, fileName, matrixName, rows):
        """
        .. raw:: html

           <html><p>Read a matrix from a file. The file must either be a Matlab v4-file or a textual file.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating the example <b>File &GT; Demos &GT; Coupled clutches</b> the result file <i>CoupledClutches.mat</i> should be available in the current dir. </p>
           <pre>readMatrixSize(&QUOT;CoupledClutches.mat&QUOT;,&nbsp;&QUOT;name&QUOT;)
           ={21,180}</pre>
           <p>returns the size of the <code>name</code> matrix in the file <i>CoupledClutches.mat</i>, which is a 21 x 180 matrix. This information is needed when calling <code>readStringMatrix</code>.</p>
           <pre>names=readStringMatrix(&QUOT;CoupledClutches.mat&QUOT;,&nbsp;&QUOT;name&QUOT;,&nbsp;21)
           Declaring&nbsp;variable:&nbsp;String&nbsp;names&nbsp;[21];</pre>
           <p>to read the <code>name</code> matrix and store it in the variable <code>names</code>. This function is not recommended to read names from a trajectory file since those names are stored transposed in the matrix.</p>
           <p>The example above will for example constain the first letter in of each variable name at index 1, the second letter of each variable name at index 2,...</p>
           <p>For such trajectory files a more suitable function to use is <code>readTrajectoryNames</code>. </p></html>

        :param str fileName: File containing the matrix, e.g. A.mat, dsin.txt.
        :param str matrixName: Name of the matrix on the file.
        :param int rows: Number of rows of the matrix - see :func:`readMatrixSize`.
        :returns: matrix
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(matrixName)
        params.append(rows)
        result = self._call_dymola_function("readStringMatrix", params)
        return self._parse_response_and_return(result, "list")

    def readTrajectory(self, fileName, signals, rows):
        """
        .. raw:: html

           <html><p>Returns all output points of a trajectory. Useful for post-processing.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating the example <b>File &GT; Demos &GT; Coupled clutches</b> the result file <i>CoupledClutches.mat</i> should be available in the current dir. </p>
           <p>Executing </p>
           <pre>readTrajectorySize(&QUOT;CoupledClutches.mat&QUOT;);
           &nbsp;=&nbsp;1522</pre>
           <p>to get the number of output points (needed as argument in addition to fileName and trajectory names which can be aquired by readTrajectoryNames) the function can be called to get one or more trajectories.</p>
           <p>Execute</p>
           <pre>signals=readTrajectory(&QUOT;CoupledClutches.mat&QUOT;,&nbsp;{&QUOT;freqHz&QUOT;,&nbsp;&QUOT;T2&QUOT;},&nbsp;1522)
           Declaring&nbsp;variable:&nbsp;Real&nbsp;signals&nbsp;[2,&nbsp;1522];</pre>
           <p>to get the trajectories for <code>freqHz</code> and <code>T2</code> and store in the variable <code>signals</code>.</p></html>

        :param str fileName: File containing a trajectory, e.g. dsres.mat.
        :param str[] signals: Vector of variable names, in Modelica-syntax, e.g a[1].b. Dimension ``[:]``.
        :param int rows: Number of time-points to return - preferably the result of readTrajectorySize.
        :returns: Values of the signals, duplicate times indicate before and after event
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        if signals:
            params.append(signals)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        params.append(rows)
        result = self._call_dymola_function("readTrajectory", params)
        return self._parse_response_and_return(result, "list2d")

    def readTrajectoryNames(self, fileName):
        """
        .. raw:: html

           <html><p>Returns the names of the trajectories in the file.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating the example <b>File &GT; Demos &GT; Coupled clutches</b> the result file <i>CoupledClutches.mat</i> should be available in the current dir. </p>
           <p>Executing</p>
           <pre>readTrajectoryNames(&QUOT;CoupledClutches.mat&QUOT;);
           &nbsp;=&nbsp;{&QUOT;Time&QUOT;, &QUOT;freqHz&QUOT;, &QUOT;T2&QUOT;, &QUOT;T3&QUOT;, ...}</pre>
           <p>returns the trajectory names found in the file.</p></html>

        :param str fileName: File containing a trajectory, e.g. dsres.mat.
        :returns: Names in trajectory file
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        result = self._call_dymola_function("readTrajectoryNames", params)
        return self._parse_response_and_return(result, "list")

    def readTrajectorySize(self, fileName):
        """
        .. raw:: html

           <html><p>Computes number of output points of trajectory. Useful for declaring the result of readTrajectory.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>After simulating the example <b>File &GT; Demos &GT; Coupled clutches</b> the result file <i>CoupledClutches.mat</i> should be available in the current dir. </p>
           <p>Executing</p>
           <pre>readTrajectorySize(&QUOT;CoupledClutches.mat&QUOT;);
           &nbsp;=&nbsp;1522</pre>
           <p>indicates that there are 1522 output points in the trajectory file.</p></html>

        :param str fileName: File containing a trajectory, e.g. dsres.mat.
        :returns: Number of time-points in the trajectory
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        result = self._call_dymola_function("readTrajectorySize", params)
        return self._parse_response_and_return(result, "int")

    def removePlots(self, closeResults=True):
        """
        .. raw:: html

           <html><p>Removes all plot windows and optionally closes all result files.</p></html>

        :param bool closeResults: Close all result files. Default ``True``.
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(closeResults)
        result = self._call_dymola_function("removePlots", params)
        return self._parse_response_and_return(result, "bool")

    def removeResults(self):
        """
        .. raw:: html

           <html><p>Remove all result files from the Variable Browser.</p></html>

        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        self._call_dymola_function("removeResults", params)

    def RunAnimation(self, immediate=True, loadFile="", ensureAnimationWindow=False, eraseOld=True):
        """
        .. raw:: html

           <html><p>Start an animation.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>RunAnimation()</pre>
           <p>Run all open animation windows.</p>
           <pre>RunAnimation(immediate=false)</pre>
           <p>Set the animation window to run when new data is loaded.</p>
           <pre>RunAnimation(loadFile=&QUOT;resultFile.mat&QUOT;)</pre>
           <p>Load <code>resultFile.mat</code> and run the animation.</p></html>

        :param bool immediate: if false the next time something is loaded we run the animation. Default ``True``.
        :param str loadFile: if non-empty: load this file first. Default ``""``.
        :param bool ensureAnimationWindow: if true ensure that one animation window. Default ``False``.
        :param bool eraseOld: Erase previous results. Default ``True``.
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(immediate)
        params.append(loadFile)
        params.append(ensureAnimationWindow)
        params.append(eraseOld)
        result = self._call_dymola_function("RunAnimation", params)
        return self._parse_response_and_return(result, "bool")

    def RunScript(self, script, silent=False):
        """
        .. raw:: html

           <html><p>Executes the specified script, see example in section &ldquo;Running a Modelica script file&rdquo; in Dymola User Manual. <code>silent</code> means that commands are not echoed if this setting is true.</p></html>

        :param str script: Script to execute.
        :param bool silent: Do not echo executed commands. Default ``False``.
        :returns: Command ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(script)
        params.append(silent)
        result = self._call_dymola_function("RunScript", params)
        return self._parse_response_and_return(result, "bool")

    def savelog(self, logfile="dymolalg.txt"):
        """
        .. raw:: html

           <html><p>The function saves the command log on a file. Please note that depending on file extension specified, filtering of the content saved is activated or not. If a <code>.txt</code> file extension is used, all text in the log is saved. If however a <code>.mos</code> extension (e. g. <code>&QUOT;fileName=MyLog.mos&QUOT;</code>) is used, neither outputs from Dymola (results etc.) nor commands that have no equivalent Modelica function will be included in the saved script file. This latter alternative corresponds to the<b> File &GT; Save</b>&hellip;command, ticking only the alternative <b>Command log</b>. </p>
           <p>Using the .mos extension (creating a script file) enables saving e. g. a promising sequence of interactive events for further reuse and development. The <code>.txt</code> extension can be used when documenting.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>savelog()</pre>
           <p>Saves the contents of the Commands Window to the default log file, <code>dymolalg.txt</code></p>
           <pre>savelog(&QUOT;logfile.txt&QUOT;)
           savelog(fileName=&QUOT;logfile.txt&QUOT;)</pre>
           <p>Saves the contents of the Commands Window to the file <code>logfile.txt</code></p></html>

        :param str logfile: File to store log in. Default ``"dymolalg.txt"``.
        :returns: Command ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(logfile)
        result = self._call_dymola_function("savelog", params)
        return self._parse_response_and_return(result, "bool")

    def saveSettings(self, fileName, storePlot=False, storeAnimation=False, storeSettings=False, storeVariables=False, storeInitial=True, storeAllVariables=True, storeSimulator=True, storePlotFilenames=False):
        """
        .. raw:: html

           <html><p>The function <code>saveSettings</code> corresponds to the command <b>File &GT; Generate Script&hellip;</b> except storing of the command log and storing the script file as a command in the model. (Storing of the command log can be handled by the function <code>savelog</code>.) Please see &QUOT;Dymola User Manual Volume 1&QUOT; for more information.</p>
           <p>Please note that if a script file should be created, the file extension must be <code>.mos</code> (e.g. <code>fileName=&QUOT;MyScript.mos&QUOT;</code>).</p>
           <p>When storing variable values, a condition is that <code>storeVariables=true</code> in the function call. <code>storeInitial=false</code> will store final values. <code>storeAllVariables=false</code> will store only parameters and states.</p>
           <p>If you want to store a plot with curves from different result files, set <code>storePlotFilenames</code> to <code>true</code>.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>saveSettings(fileName=&QUOT;mySettings.mos&QUOT;)</pre>
           <p>to save the selected settings to a Modelica script file <code>mySettings.mos</code>.</p></html>

        :param str fileName: File to store in.
        :param bool storePlot: Store plot commands. Default ``False``.
        :param bool storeAnimation: Store animation commands. Default ``False``.
        :param bool storeSettings: Store global flags. Default ``False``.
        :param bool storeVariables: Store current parameter setting. Default ``False``.
        :param bool storeInitial: Store variables at initial point. Default ``True``.
        :param bool storeAllVariables: Store all variables. Default ``True``.
        :param bool storeSimulator: Store simulator setup. Default ``True``.
        :param bool storePlotFilenames: Store result filenames in plot commands. Default ``False``.
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(storePlot)
        params.append(storeAnimation)
        params.append(storeSettings)
        params.append(storeVariables)
        params.append(storeInitial)
        params.append(storeAllVariables)
        params.append(storeSimulator)
        params.append(storePlotFilenames)
        result = self._call_dymola_function("saveSettings", params)
        return self._parse_response_and_return(result, "bool")

    def saveTotalModel(self, fileName, modelName):
        """
        .. raw:: html

           <html><p>This function corresponds to <b>File &GT; Save Total ...</b>.</p>
           <p>It saves a model and its dependencies (from non-encrypted libraries) as a modelica package for easy distribution.</p></html>

        :param str fileName: File to store in (remember: Modelica string quoting).
        :param str modelName: Top-level model.
        :returns: True if succesful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(modelName)
        result = self._call_dymola_function("saveTotalModel", params)
        return self._parse_response_and_return(result, "bool")

    def setClassText(self, parentName, fullText):
        """
        Sets the Modelica text for an existing or new class.

        :param str parentName: The package in which to add the class.
        :param str fullText: The Modelica text.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(parentName)
        params.append(fullText)
        result = self._call_dymola_function("setClassText", params)
        return self._parse_response_and_return(result, "bool")

    def SetDymolaCompiler(self, compiler, settings=[""]):
        """
        .. raw:: html

           <html><p>Set up the compiler and compiler options on Windows.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <h5>Visual Studio</h5>
           <pre>SetDymolaCompiler(&QUOT;vs&QUOT;, {&QUOT;CCompiler=MSVC&QUOT;,&QUOT;MSVCDir=C:/Program Files (x86)/Microsoft Visual Studio 10.0/Vc&QUOT;});</pre>
           <h5>GCC</h5>
           <pre>SetDymolaCompiler(&QUOT;gcc&QUOT;, {&QUOT;CCompiler=GCC&QUOT;,&QUOT;GCCPath=C:/MinGW/bin/gcc&QUOT;});</pre>
           <h5>Options</h5>
           <p>Set any of <code>DLL</code>, <code>DDE</code> or <code>OPC</code> to <code>1</code> to enable</p>
           <pre>SetDymolaCompiler(&QUOT;vs&QUOT;, {&QUOT;CCompiler=MSVC&QUOT;, &QUOT;MSVCDir=C:/Program Files (x86)/Microsoft Visual Studio 10.0/Vc&QUOT;, &QUOT;<b>DLL=0</b>&QUOT;, &QUOT;<b>DDE=0</b>&QUOT; , &QUOT;<b>OPC=0</b>&QUOT;});</pre>
           <h4><span style="color:#008000">Linux</span></h4>
           <p>This function is not supported on Linux.</p>
           <p>When executed it returns <code>ok</code> without performing any action.</p></html>

        :param str compiler: 
        :param str[] settings:  Dimension ``[:]``. Default ``[""]``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(compiler)
        if settings:
            params.append(settings)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        self._call_dymola_function("SetDymolaCompiler", params)

    def ShowComponent(self, path, components=None):
        """
        .. raw:: html

           <html><p>Highlights the given components in the diagram.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>ShowComponent(&QUOT;Modelica.Blocks.Examples.PID_Controller&QUOT;,&nbsp;{&QUOT;inertia1&QUOT;,&nbsp;&QUOT;inertia2&QUOT;})</pre>
           <p>will highlight <b>inertia1</b> and <b>inertia2</b> in the diagram layer of the example <code><b>Modelica.Blocks.Examples.PID_Controller</b></code>.</p>
           <p><b>Note</b> that the model (PID_Controller) must first be selected in the Package Browser.</p></html>

        :param str path: Path to component to show.
        :param str[] components: Optional list of subcomponents to highlight. Dimension ``[:]``. Default ``[]``.
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(_NamedArgument("path", path))
        if components:
            params.append(_NamedArgument("components", components))
        result = self._call_dymola_function("ShowComponent", params)
        return self._parse_response_and_return(result, "bool")

    def showMessageWindow(self, show):
        """
        .. raw:: html

           <html><p>Show or hide the message window.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>showMessageWindow(true)
           showMessageWindow(false)</pre>
           <p>to show or hide the message window.</p></html>

        :param bool show: 
        :returns: ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(show)
        result = self._call_dymola_function("showMessageWindow", params)
        return self._parse_response_and_return(result, "bool")

    def signalOperatorValue(self, variablePath, signalOperator, startTime=-1E+100, stopTime=1E+100):
        """
        Returns the value of a signal operator for a given variable. The last result file is used.

        :param str variablePath: Variable path or legend name.
        :param int signalOperator: Signal operator. See enumeration :class:`SignalOperator <dymola.dymola_enums.SignalOperator>` for available operators. Enumeration.
        :param float startTime: Start time. By default the entire simulated interval is used. Default ``-1E+100``.
        :param float stopTime: Stop time. By default the entire simulated interval is used. Default ``1E+100``.
        :returns: Returns the value of the signal operator
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(variablePath)
        params.append(signalOperator)
        params.append(startTime)
        params.append(stopTime)
        result = self._call_dymola_function("signalOperatorValue", params)
        return self._parse_response_and_return(result, "float")

    def simulateExtendedModel(self, problem=None, startTime=None, stopTime=None, numberOfIntervals=None, outputInterval=None, method=None, tolerance=None, fixedstepsize=None, resultFile=None, initialNames=None, initialValues=None, finalNames=None, autoLoad=None):
        """
        .. raw:: html

           <html><p>An extension of <code>simulateModel</code> (please see that routine, also for comparison between a number of similar routines). This routine gives the possibility to set parameters and startvalues before simulation and to get the final values at end-point of simulation. <code>autoLoad=true</code> is default. If false the result file is not loaded in the plot window (and variables are not replotted).</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <h5>Parameter studies of selected parameters</h5>
           <p>Consider the demo model <code>Modelica.Mechanics.Rotational.CoupledClutches</code>. The parameters J1.J and J2.J should be varied and the resulting <code>J1.w</code> and <code>J4.w</code> should be measured and saved at the end of the simulation. That will be the result of the following function call:</p>
           <p>Please note that you for this example first have to open the model (using <b>File &GT; Demos&hellip; &GT; Coupled Clutches</b>) since it is a read-only demo. Entering in the command input line (followed by enter):</p>
           <pre>simulateExtendedModel(&QUOT;Modelica.Mechanics.Rotational.Examples.CoupledClutches&QUOT;,initialNames={&QUOT;J1.J&QUOT;,&QUOT;J2.J&QUOT;},initialValues={2, 3},finalNames={&QUOT;J1.w&QUOT;,&QUOT;J4.w&QUOT;});</pre>
           <p>The output visible in the command window will be:</p>
           <pre>&nbsp;=&nbsp;true,&nbsp;{6.213412958654301,&nbsp;0.9999999999999936}</pre>
           <p>It can be seen that the function was executed successfully (<code>= true</code>); then the value of<code> J1.w</code> (6.213&hellip;) and <code>J4.w</code> (0.99999&hellip;) is presented.</p>
           <p>By changing <code>J1.J</code> and <code>J2.J</code> and simulating the resulting <code>J1.w</code> and <code>J4.w</code> can be studied.</p><p>Note that Integer and Boolean variables (coded as 0 and 1) are supported as well. However, structural parameters that are evaluated cannot be part of initialNames, use modifiers as described in simulateModel for them.</p><h4><span style="color: #008000">Python example</span></h4>
           <pre>ok, values = dymola.simulateExtendedModel(&quot;Modelica.Mechanics.Rotational.Examples.CoupledClutches&quot;, initialNames=[&quot;J1.J&quot;,&quot;J2.J&quot;], initialValues=[2, 3], finalNames=[&quot;J1.w&quot;,&quot;J4.w&quot;])</pre>
           </html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch. Default ``""``.
        :param float startTime: Start of simulation. Default ``0.0``.
        :param float stopTime: End of simulation. Default ``1.0``.
        :param int numberOfIntervals: Number of output points. Default ``0``.
        :param float outputInterval: Distance between output points. Default ``0.0``.
        :param str method: Integration method. Default ``"Dassl"``.
        :param float tolerance: Tolerance of integration. Default ``0.0001``.
        :param float fixedstepsize: Fixed step size for Euler. Default ``0.0``.
        :param str resultFile: Where to store result. Default ``"dsres"``.
        :param str[] initialNames: Parameters and start-values to set. Dimension ``[:]``. Default ``fill("", 0)``.
        :param float[] initialValues: Parameter values. Dimension ``[size(initialNames, 1)]``. Default ``fill(0.0, 0)``.
        :param str[] finalNames: Variables at end-point. Dimension ``[:]``. Default ``fill("", 0)``.
        :param bool autoLoad: Auto load result. Default ``True``.
        :returns: true if successful (``bool``), Values at end-point (``float[]``)
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if problem is not None:
            params.append(_NamedArgument("problem", problem))
        if startTime is not None:
            params.append(_NamedArgument("startTime", startTime))
        if stopTime is not None:
            params.append(_NamedArgument("stopTime", stopTime))
        if numberOfIntervals is not None:
            params.append(_NamedArgument("numberOfIntervals", numberOfIntervals))
        if outputInterval is not None:
            params.append(_NamedArgument("outputInterval", outputInterval))
        if method is not None:
            params.append(_NamedArgument("method", method))
        if tolerance is not None:
            params.append(_NamedArgument("tolerance", tolerance))
        if fixedstepsize is not None:
            params.append(_NamedArgument("fixedstepsize", fixedstepsize))
        if resultFile is not None:
            params.append(_NamedArgument("resultFile", resultFile))
        if initialNames:
            params.append(_NamedArgument("initialNames", initialNames))
        if initialValues:
            params.append(_NamedArgument("initialValues", initialValues))
        if finalNames:
            params.append(_NamedArgument("finalNames", finalNames))
        if autoLoad is not None:
            params.append(_NamedArgument("autoLoad", autoLoad))
        result = self._call_dymola_function("simulateExtendedModel", params)
        return self._parse_response_and_return(result, "list")

    def simulateModel(self, problem="", startTime=0.0, stopTime=1.0, numberOfIntervals=0, outputInterval=0.0, method="Dassl", tolerance=0.0001, fixedstepsize=0.0, resultFile="dsres"):
        """
        .. raw:: html

           <html><p>Simulate the model for the given time. <code>method</code> is a string with the name of the integration algorithm; the names correspond to the ones found in the popup-menu and the string is case insensitive. <code>fixedstepsize</code> is only used if the method Euler is selected. Note that file extension is automatically added to <code>resultFile</code> (normally <code>&QUOT;.mat&QUOT;</code>). For backwards compatibility the default for <code>resultFile</code> is <code>&QUOT;dsres&QUOT;</code>.</p>
           <p>The entire command corresponds to <b>Simulate</b> in the menus.</p>
           <p>Values specified in the model will be used unless the corresponding modifier is given in the <code>simulateModel</code> command.</p>
           <p>Note: <code>translateModel</code>, <code>simulateModel</code>, <code>simulateExtendedModel</code> , <code>simulateMultiExtendedModel</code>, and <code>simulateMultiResultsModel</code> have named arguments (as is indicated above) and the default for problem is &QUOT;&QUOT; corresponding to the most recently used model. Thus <code>simulateModel(stopTime=10,method=&QUOT;Euler&QUOT;);</code> corresponds to <code>simulateModel(&QUOT;&QUOT;, 0, 10, 0, 0, &QUOT;Euler&QUOT;, 1e-4);</code></p>
           <p>It is possible to specify a model name with modifiers for translateModel, simulateModel and simulateExtendedModel.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>for source in {&QUOT;Step&QUOT;,&QUOT;Constant&QUOT;,&QUOT;Ramp&QUOT;,&QUOT;Sine&QUOT;} loop
           simulateModel(&QUOT;TestSource(redeclare Modelica.Blocks.Sources.&QUOT;+source+&QUOT; Source)&QUOT;);
           end for;</pre>
           <p>to simulate the model below with different sources.</p>
           <p><code><font style="color: #0000ff; ">model</font>&nbsp;TestSource</code></p>
           <p><code>&nbsp;&nbsp;<font style="color: #ff0000; ">Modelica.Blocks.Sources.Step</font>&nbsp;Source</code></p>
           <p><code><font style="color: #0000ff; ">end&nbsp;</font>TestSource;</code></p>
           <h4><span style="color: #008000">Python example</span></h4>
           <pre>for source in [&quot;Step&quot;,&quot;Constant&quot;,&quot;Ramp&quot;,&quot;Sine&quot;]:
           dymola.simulateModel(&quot;TestSource(redeclare Modelica.Blocks.Sources.&quot;+source+&quot; Source)&quot;)
           </pre></html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch. Default ``""``.
        :param float startTime: Start of simulation. Default ``0.0``.
        :param float stopTime: End of simulation. Default ``1.0``.
        :param int numberOfIntervals: Number of output points. Default ``0``.
        :param float outputInterval: Distance between output points. Default ``0.0``.
        :param str method: Integration method. Default ``"Dassl"``.
        :param float tolerance: Tolerance of integration. Default ``0.0001``.
        :param float fixedstepsize: Fixed step size for Euler. Default ``0.0``.
        :param str resultFile: Where to store result. Default ``"dsres"``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(problem)
        params.append(startTime)
        params.append(stopTime)
        params.append(numberOfIntervals)
        params.append(outputInterval)
        params.append(method)
        params.append(tolerance)
        params.append(fixedstepsize)
        params.append(resultFile)
        result = self._call_dymola_function("simulateModel", params)
        return self._parse_response_and_return(result, "bool")

    def simulateMultiExtendedModel(self, problem=None, startTime=None, stopTime=None, numberOfIntervals=None, outputInterval=None, method=None, tolerance=None, fixedstepsize=None, resultFile=None, initialNames=None, initialValues=None, finalNames=None):
        """
        .. raw:: html

           <html><p>An extension of <code>simulateModel</code> (please see that routine, also for comparison between a number of similar routines). The function handles a number of simulations. For each simulation it is possible to set parameters and start-values before simulation and to get the final values at end-point of simulation.</p>
           <p>The function is valuable e.g. when wanting to study the best parameter setup or the robustness of a parameter setup for a static simulation (no states involved).</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>Entering in the command input line (followed by enter):</p>
           <pre>simulateMultiExtendedModel(&QUOT;Modelica.Mechanics.Rotational.Examples.CoupledClutches&QUOT;, initialNames={&QUOT;J1.J&QUOT;,&QUOT;J2.J&QUOT;}, initialValues=[2,3;3,4;4,5], finalNames={&QUOT;J1.w&QUOT;, &QUOT;J4.w&QUOT;})</pre><p>The output visible in the command window will be:</p>
           <pre>&nbsp;=&nbsp;true,&nbsp;
           [6.213412958654301,&nbsp;0.9999999999999936;
           7.483558191010656,&nbsp;1.0000000000000024;
           8.107446379737777,&nbsp;0.9999999999999951]</pre>
           <h4><span style="color: #008000">Python example</span></h4>
           <pre>ok, values = dymola.simulateMultiExtendedModel(&quot;Modelica.Mechanics.Rotational.Examples.CoupledClutches&quot;, initialNames=[&quot;J1.J&quot;,&quot;J2.J&quot;], initialValues=[[2,3],[3,4],[4,5]], finalNames=[&quot;J1.w&quot;, &quot;J4.w&quot;])</pre>
           </html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch. Default ``""``.
        :param float startTime: Start of simulation. Default ``0.0``.
        :param float stopTime: End of simulation. Default ``1.0``.
        :param int numberOfIntervals: Number of output points. Default ``0``.
        :param float outputInterval: Distance between output points. Default ``0.0``.
        :param str method: Integration method. Default ``"Dassl"``.
        :param float tolerance: Tolerance of integration. Default ``0.0001``.
        :param float fixedstepsize: Fixed step size for Euler. Default ``0.0``.
        :param str resultFile: Where to store result. Default ``"dsres"``.
        :param str[] initialNames: Parameters and start-values to set. Dimension ``[:]``. Default ``fill("", 0)``.
        :param float[][] initialValues: Parameter values. Dimension ``[:, size(initialNames, 1)]``. Default ``fill(0.0, 0, 0)``.
        :param str[] finalNames: Variables at end-point. Dimension ``[:]``. Default ``fill("", 0)``.
        :returns: true if successful (``bool``), Values at end-point (``float[][]``)
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        if problem is not None:
            params.append(_NamedArgument("problem", problem))
        if startTime is not None:
            params.append(_NamedArgument("startTime", startTime))
        if stopTime is not None:
            params.append(_NamedArgument("stopTime", stopTime))
        if numberOfIntervals is not None:
            params.append(_NamedArgument("numberOfIntervals", numberOfIntervals))
        if outputInterval is not None:
            params.append(_NamedArgument("outputInterval", outputInterval))
        if method is not None:
            params.append(_NamedArgument("method", method))
        if tolerance is not None:
            params.append(_NamedArgument("tolerance", tolerance))
        if fixedstepsize is not None:
            params.append(_NamedArgument("fixedstepsize", fixedstepsize))
        if resultFile is not None:
            params.append(_NamedArgument("resultFile", resultFile))
        if initialNames:
            params.append(_NamedArgument("initialNames", initialNames))
        if initialValues:
            params.append(_NamedArgument("initialValues", initialValues))
        if finalNames:
            params.append(_NamedArgument("finalNames", finalNames))
        result = self._call_dymola_function("simulateMultiExtendedModel", params)
        return self._parse_response_and_return(result, "list")

    def simulateMultiResultsModel(self, problem, startTime, stopTime, numberOfIntervals, outputInterval, method, tolerance, fixedstepsize, resultFile, initialNames, initialValues, resultNames):
        """
        .. raw:: html

           <html><p>An extension of <code>simulateModel</code> (please see that routine, also for comparison between a number of similar routines).</p>
           <p>Compared to <code>simulateMultiExtendedModel</code> this function stores the full trajectories of several simulations instead of just the endpoints.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>(storing the output in the two variables <code>ok</code> and <code>traj</code> to avoid cluttering the Commands window)</p>
           <pre>(ok,traj)=simulateMultiResultsModel(&QUOT;Modelica.Mechanics.Rotational.Examples.CoupledClutches&QUOT;, stopTime=1.2, numberOfIntervals=10, resultFile=&QUOT;CoupleCluches&QUOT;, initialNames={&QUOT;freqHz&QUOT;}, initialValues=[0.1;0.2;0.3;0.4], resultNames={&QUOT;J1.w&QUOT;,&QUOT;J3.w&QUOT;});</pre>
           <p>results in</p>
           <pre>Declaring&nbsp;variable:&nbsp;Boolean&nbsp;ok&nbsp;;
           Declaring&nbsp;variable:&nbsp;Real&nbsp;traj&nbsp;[4,&nbsp;2,&nbsp;11];</pre>
           <p>where <code>traj</code> contains the two trajectories for <code>J1.w</code> and <code>J3.w</code> (11 result points) for the 4 caseses of initialvalues of <code>freqHz</code>.</p></html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch.
        :param float startTime: Start of simulation.
        :param float stopTime: End of simulation.
        :param int numberOfIntervals: Number of output points.
        :param float outputInterval: Distance between output points.
        :param str method: Integration method.
        :param float tolerance: Tolerance of integration.
        :param float fixedstepsize: Fixed step size for Euler.
        :param str resultFile: Where to store result.
        :param str[] initialNames: Parameters and start-values to set. Dimension ``[:]``.
        :param float[][] initialValues: Parameter values. Dimension ``[:, size(initialNames, 1)]``.
        :param str[] resultNames: Variables during simulation. Dimension ``[:]``.
        :returns: true if successful (``bool``), Values at end-point (``float[][][]``)
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(_NamedArgument("problem", problem))
        params.append(_NamedArgument("startTime", startTime))
        params.append(_NamedArgument("stopTime", stopTime))
        params.append(_NamedArgument("numberOfIntervals", numberOfIntervals))
        params.append(_NamedArgument("outputInterval", outputInterval))
        params.append(_NamedArgument("method", method))
        params.append(_NamedArgument("tolerance", tolerance))
        params.append(_NamedArgument("fixedstepsize", fixedstepsize))
        params.append(_NamedArgument("resultFile", resultFile))
        if initialNames:
            params.append(_NamedArgument("initialNames", initialNames))
        if initialValues:
            params.append(_NamedArgument("initialValues", initialValues))
        if resultNames:
            params.append(_NamedArgument("resultNames", resultNames))
        result = self._call_dymola_function("simulateMultiResultsModel", params)
        return self._parse_response_and_return(result, "list")

    def system(self, _command):
        """
        .. raw:: html

           <html><p>Execute system commands.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>Execute</p>
           <pre>system(&QUOT;time&nbsp;/t&nbsp;&GT;&GT;&nbsp;time.txt&QUOT;);</pre>
           <p>to print the current time to a file, <code>time.txt</code>, in the current directory.</p></html>

        :param str _command: Command to execute.
        :returns: Command ok
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(_command)
        result = self._call_dymola_function("system", params)
        return self._parse_response_and_return(result, "bool")

    def trace(self, variables=False, statements=False, calls=False, onlyFunction="", profile=False):
        """
        .. raw:: html

           <html><p>Function to trace execution of interactive functions, helps in finding errors.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>For the following small function</p>
           <p><font style="color: #0000ff; ">function</font>&nbsp;Test</p>
           <p>&nbsp;&nbsp;<font style="color: #0000ff; ">input&nbsp;</font><font style="color: #ff0000; ">Real</font>&nbsp;val;</p>
           <p>&nbsp;&nbsp;<font style="color: #0000ff; ">output&nbsp;</font><font style="color: #ff0000; ">Real</font>&nbsp;out1,out2;</p>
           <p><font style="color: #0000ff; ">algorithm&nbsp;</font></p>
           <p>&nbsp;&nbsp;out1:=<font style="color: #ff0000; ">sin</font>(val);</p>
           <p>&nbsp;&nbsp;out2:=<font style="color: #ff0000; ">cos</font>(val);</p>
           <p><font style="color: #0000ff; ">end&nbsp;</font>Test;</p>
           <p>Setting trace(variables=true,&nbsp;statements=true,&nbsp;calls=true,&nbsp;profile=true) and then executing Test(0.3); </p>
           <p><code>Trace&nbsp;statement:&nbsp;Test(0.3);</code></p>
           <pre>Trace&nbsp;in&nbsp;Test&nbsp;:&nbsp;start&nbsp;of&nbsp;call.
           Trace&nbsp;in&nbsp;Test&nbsp;variable:&nbsp;out1&nbsp;=&nbsp;0.0
           Trace&nbsp;in&nbsp;Test&nbsp;variable:&nbsp;out2&nbsp;=&nbsp;0.0
           <p><code></p><p>Trace&nbsp;in&nbsp;Test&nbsp;statement:&nbsp;out1&nbsp;:=&nbsp;<a href="Modelica://sin">sin</a>(val);</code></p>
           <p>Trace&nbsp;in&nbsp;Test&nbsp;variable:&nbsp;out1&nbsp;=&nbsp;0.29552020666133955
           <p><code></p><p>Trace&nbsp;in&nbsp;Test&nbsp;statement:&nbsp;out2&nbsp;:=&nbsp;<a href="Modelica://cos">cos</a>(val);</code></p>
           <p>Trace&nbsp;in&nbsp;Test&nbsp;variable:&nbsp;out2&nbsp;=&nbsp;0.955336489125606
           Trace&nbsp;in&nbsp;Test&nbsp;:&nbsp;end&nbsp;of&nbsp;call.
           &nbsp;=&nbsp;0.29552020666133955,&nbsp;0.955336489125606</pre>
           <p>Output of result above.</p></html>

        :param bool variables: Trace assignments to variables. Default ``False``.
        :param bool statements: Trace all statements. Default ``False``.
        :param bool calls: Trace function calls. Default ``False``.
        :param str onlyFunction: Name of function this is limited to. Default ``""``.
        :param bool profile: Profile function (time and #calls). Default ``False``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(variables)
        params.append(statements)
        params.append(calls)
        params.append(onlyFunction)
        params.append(profile)
        self._call_dymola_function("trace", params)

    def translateModel(self, problem):
        """
        .. raw:: html

           <html><p>Compile the model (with current settings). This corresponds to <b>Translate</b> (Normal) in the menus.</p></html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(problem)
        result = self._call_dymola_function("translateModel", params)
        return self._parse_response_and_return(result, "bool")

    def translateModelExport(self, modelName):
        """
        .. raw:: html

           <html><p>Translates the active model to code executable on any platform without a Dymola license at the target system.</p>
           <p>This built-in function corresponds to the command <b>Simulation &GT; Translate &GT; Export</b>, and corresponding drop-down selection of the <b>Translate</b> button.</p>
           <p>This functionality demands license. For more information, please see the manual &ldquo;Dymola User Manual Volume 2&rdquo;, chapter 6 &ldquo;Other Simulation Environments&rdquo;, section &ldquo;Code and Model Export&rdquo;.</p></html>

        :param str modelName: Model to open.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(modelName)
        result = self._call_dymola_function("translateModelExport", params)
        return self._parse_response_and_return(result, "bool")

    def translateModelFMU(self, modelToOpen, storeResult=False, modelName="", fmiVersion="1", fmiType="all", includeSource=False):
        """
        .. raw:: html

           <html><p>Translates a model to an FMU. The input string <code>model</code> defines the model to open in the same way as the traditional <code>translateModel</code> command in Dymola.</p>
           <p>The Boolean input <code>storeResult</code> is used to specify if the FMU should generate a result file (<code>dsres.mat</code>). If <code>storeResult</code> is true, the result is saved in <code>&LT;model id&GT;</code>.mat when the FMU is imported and simulated, where<code> &LT;model id&GT;</code> is given at FMU initialization. (If empty, <code>&ldquo;dsres&rdquo;</code> is used instead.) This is useful when importing FMUs with parameter <code>allVariables = false</code>, since it provides a way to still obtain the result for all variables. Simultaneous use of result storing and source code inclusion (see below) is not supported.</p>
           <p>The input string <code>modelName</code> is used to select the FMU model identifier. If the string is empty, the model identifier will be the name of the model, adapted to the syntax of model identifier (e.g. dots will be exchanged with underscores).The name must only contain letters, digits and underscores. It must not begin with a digit.</p>
           <p>The input string <code>fmiVersion</code> controls the FMI version (<code>&QUOT;1&QUOT;</code> or <code>&QUOT;2&QUOT;</code>) of the FMU. The default is <code>&QUOT;1&QUOT;</code>.</p>
           <p>The input string <code>fmiType</code> define whether the model should be exported as</p>
           <ul>
           <li>Model exchange (<code>fmiType=&QUOT;me&QUOT;</code>)</li>
           <li>Co-simulation using Cvode (<code>fmiType=&QUOT;cs&QUOT;</code>)</li>
           <li>Both model exchange, and Co-simulation using Cvode (<code>fmiType=&QUOT;all&QUOT;</code>)</li>
           <li>Co-simulation using Dymola solvers (<code>fmiType=&QUOT;csSolver&QUOT;</code>).</li>
           </ul>
           <p>The default setting is <code>fmiType=&QUOT;all&QUOT;</code>. This parameter primarily affects modelDescription.xml. For the three first choices binary and source code always contains both model exchange and Co-simulation. For the last choice the binary code only contains Co-simulation. Note &ndash; Co-simulation using Dymola solvers requires Binary Model Export license. For this option it might also be noted that also the selected tolerance in Dymola will be used by the Cosimulation FMU, and source code generation FMU is not supported by this alternative.</p>
           <p>The Boolean input <code>includeSource</code> is used to specify if source code should be included in the FMU. The default setting is that it is not included (<code>includeSource=false</code>). Simultaneous use of result storing (see above) and source code inclusion is not supported.</p>
           <p>The function outputs a string <code>FMUName</code> containing the FMU model identifier on success, otherwise an empty string.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>Translating the Modelica CoupledClutches demo model to an FMU with result file generation, is accomplished by the function call</p>
           <pre>translateModelFMU(&QUOT;Modelica.Mechanics.Rotational.Examples. CoupledClutches&QUOT;, true);</pre>
           <p>After successful translation, the generated FMU (with file extension .fmu) will be located in the current directory. Exporting an FMU using the 64-bit version of Dymola will create both32-bit and 64-bit binaries if possible.</p>
           <p>The <code>translateModelFMU</code> command will generate an FMU that supports both the FMI for Model Exchange specification and the FMI for Co-Simulation slave interface (all functions will be present in the DLL).</p>
           <p>On Linux, note that FMU export requires the Linux utility &ldquo;zip&rdquo;. If not already installed, please install using your packaging manager (e.g. apt-get) or see e.g. http://infozip.org/Zip.html.</p>
           <p>This built-in function corresponds to the commands <b>Simulation &GT; Translate &GT; FMU</b> and corresponding drop-down selections of the <b>Translate</b> button.</p>
           <p>For more information about FMI, please see the manual &ldquo;Dymola User Manual Volume 2&rdquo;, chapter 6 &ldquo;Other Simulation Environments&rdquo;, section &ldquo;FMI Support in Dymola&rdquo;.</p></html>

        :param str modelToOpen: Model to open.
        :param bool storeResult: Whether to store result in mat file from within FMU. Default ``False``.
        :param str modelName: User-selected FMU modelIdentifier (also used as modelName). Default ``""``.
        :param str fmiVersion: FMI version, 1 or 2. Default ``"1"``.
        :param str fmiType: FMI type, me (model exchange), cs (co-simulation), all or csSolver (using Dymola solver).  Only affects modelDescription.xml; binary and source code always contain both. Default ``"all"``.
        :param bool includeSource: Whether to include source code in FMU. Default ``False``.
        :returns: FMI model identifier on success, empty string on failure
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(modelToOpen)
        params.append(storeResult)
        params.append(modelName)
        params.append(fmiVersion)
        params.append(fmiType)
        params.append(includeSource)
        result = self._call_dymola_function("translateModelFMU", params)
        return self._parse_response_and_return(result, "str")

    def variables(self, filename="", variables=["*"]):
        """
        .. raw:: html

           <html><p>Works as the function <code>list</code>, but does not list interactive settings of translator switches. See <code>list</code> for more documentation</p></html>

        :param str filename:  Default ``""``.
        :param str[] variables: Select a subset of the variables. Wildcards * and ? may be used. Dimension ``[:]``. Default ``["*"]``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(filename)
        if variables:
            params.append(variables)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        self._call_dymola_function("variables", params)

    def visualize3dModel(self, problem):
        """
        .. raw:: html

           <html><p>Make a 3d visualization of the initial configuration of a model, same functionality as <b>Simulation &GT; Visualize</b>.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <pre>visualize3dModel(&QUOT;Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum&QUOT;)</pre>
           <p>to make a 3d visualization of the DoublePendulum model.</p></html>

        :param str problem: Name of model, e.g. Modelica.Mechanics.Rotational.Components.Clutch.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(problem)
        result = self._call_dymola_function("visualize3dModel", params)
        return self._parse_response_and_return(result, "bool")

    def writeMatrix(self, fileName, matrixName, matrix, append=False):
        """
        .. raw:: html

           <html><p>Write one real-valued matrix expression to a file. Vectors and scalar expression must be converted by enclosing them in [ ]. Arrays of matrices cannot currently be written. The file format is Matlab v4.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>Execute <code>writeMatrix(&QUOT;A.mat&QUOT;,&nbsp;&QUOT;data&QUOT;,&nbsp;[1,&nbsp;2;&nbsp;3,&nbsp;4])</code> to write [1, 2; 3, 4] to a matrix <code>data</code> in the file <code>A.mat</code>.</p>
           <p>Execute <code>writeMatrix(&QUOT;A.mat&QUOT;,&nbsp;&QUOT;data_2&QUOT;,&nbsp;[5,&nbsp;6;&nbsp;7,&nbsp;8], true)</code> to write [5, 6; 7, 8] to a matrix <code>data_2</code> and append it in the file <code>A.mat</code>.</p>
           <p><code>A.mat</code> now contains both <code>data</code> and <code>data_2.</code></p>
           <p>Execute <code>writeMatrix(&QUOT;A.mat&QUOT;,&nbsp;&QUOT;data_2&QUOT;,&nbsp;[5,&nbsp;6;&nbsp;7,&nbsp;8])</code> (without the last argument append=true) will overwrite the content of A.mat and it will now only contain data_2.</p></html>

        :param str fileName: File that will contain the matrix, e.g. A.mat.
        :param str matrixName: Name of the matrix in the file.
        :param float[][] matrix: Data to be written, use [A] to convert vector or scalar to matrix. Dimension ``[:, :]``.
        :param bool append: Append data to file. Default ``False``.
        :returns: true if successful
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        params.append(matrixName)
        if matrix:
            params.append(matrix)
        else:
            params.append(_UnquotedString("fill(0, 0, 0)"))
        params.append(append)
        result = self._call_dymola_function("writeMatrix", params)
        return self._parse_response_and_return(result, "bool")

    def writeTrajectory(self, fileName, signals, values):
        """
        .. raw:: html

           <html><p>Writes a trajectory file based on values. Useful for generating input signals.</p>
           <h4><span style="color:#008000">Example in Dymola</span></h4>
           <p>Execute</p>
           <pre>writeTrajectory(&QUOT;A.mat&QUOT;,&nbsp;{&QUOT;Time&QUOT;,&nbsp;&QUOT;u1&QUOT;},&nbsp;[0,&nbsp;0;&nbsp;0.1,&nbsp;0.099;&nbsp;0.2,&nbsp;0.198;&nbsp;0.3,&nbsp;0.295;&nbsp;0.4,&nbsp;0.389;&nbsp;0.5,&nbsp;0.479;&nbsp;0.5,&nbsp;0.479;&nbsp;0.6,&nbsp;0.564;&nbsp;0.7,&nbsp;0.644;&nbsp;0.8,&nbsp;0.717;&nbsp;0.9,&nbsp;0.783;&nbsp;1.0,&nbsp;0.841])</pre>
           <p>to write the trajectory sin(linspace(0:1:11)) as a variable <code>u1</code> to a file <code>A.mat</code> with an event at Time=0.5 (duplicate trajectory points).</p></html>

        :param str fileName: File to store trajectory in, e.g. dsu.txt.
        :param str[] signals: Vector of variable names, in Modelica-syntax, e.g a[1].b. Dimension ``[:]``.
        :param float[][] values: Values of the signals, duplicate times indicate before and after event. Dimension ``[:, size(signals, 1)]``.
        :raises: :class:`DymolaException <dymola.dymola_exception.DymolaException>`
        """
        params = []
        params.append(fileName)
        if signals:
            params.append(signals)
        else:
            params.append(_UnquotedString("fill(\"\", 0)"))
        if values:
            params.append(values)
        else:
            params.append(_UnquotedString("fill(0, 0, 0)"))
        self._call_dymola_function("writeTrajectory", params)
