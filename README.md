# BELab
## Introduction
BELab is a script tool developed based on Python for implementing **coupling simulation** between CFD and Modelica.
The published version of BELab is 1.0, and this version could achieve:

*    orifice pressure data coupling between multi-zone model origanzed in Modelica and room model based on Fluent.
*    Inlet velocity and temperature data coupling.
*    Room mean temperature data coupling.

The file was origanized as fellow:
--BELab
&nbsp;&nbsp;&nbsp;&nbsp;--FMU
&nbsp;&nbsp;&nbsp;&nbsp;--dymola
&nbsp;&nbsp;&nbsp;&nbsp;--buildingspy
&nbsp;&nbsp;&nbsp;&nbsp;--fluent_CORBA
&nbsp;&nbsp;&nbsp;&nbsp;--main_code.py
&nbsp;&nbsp;&nbsp;&nbsp;--software.py
&nbsp;&nbsp;&nbsp;&nbsp;--string_gen.py
In which, the *"FMU"* is a file dictionary include some validation FMU models. *"dymola"* is a Python package supported by Dymola as an interface between python and dymola. *"buildingspy"* is a Python package supported by LBL to get simulation data of Modelica. *"fluent_CORBA"* is a Python package from [author: ansys-dev](https://github.com/ansys-dev/fluent_corba). *"main_code.py"* is the main part of this project, implements the feature of data exchange, coupling simulation and control the whole workflow. And *"software_back.py"* is the ui.
## Implemention
### Machine environment
To use BELab, you have to get the below preparations on your machine:
*    Fluent (**Not** less than version 2015_1)
*    Well-posed FMU model generate by JModelica (or you can generate it by Dymola, but in this way you should get the Dynamic_lic from Dymola)
*    .msh file that could be used in Fluent

The EXE version would also be published, so you don't need to worried about the confusing Python environment and numerous packages. But if you'd like to contribute to this project and revised the source code to make BELab adapt to yourselves problems, then you need the follows:
*    Basic Python environment (include some basic packages like pandas, numpy, version just use the newest)
*    Python package pyfmi version 2.9.8 (you can download this package by anaconda)

### Work flow
The typical work flow of BELab is below:
*    First open the GUI of BELab. 
>    For EXE version, you should open the .exe file. For source code version, you should run main_code.py in a Python IDE.

*    Second load the .fmu file and .msh file from the UI.
>    ![Load files](https://github.com/wenzheshang/BELab/blob/main/image_for_readme/load_file.png)

*    Then set basic parameter for the two models
>    ![Set parameter](https://github.com/wenzheshang/BELab/blob/main/image_for_readme/set_parameter.png)
>    **Notice**: The name of parameters should be set obey some specific rules. different name of room temperature in multi room should be set as "fixedTemperature1", "fixedTemperature2"...the orifices' name should be "ori1", "ori2"...the name of inlet should be "inlet", outlet should be "outlet", the walls should set as "wall_left", "wall_right", "wall_ceiling", "wall_floor", "wall_back", "wall_front". You can modify the source code to make it adapt to your problem.
>    **Notice**: In this version, The CFD could only receive the inlet velocity, temperature and outlet velocity data from Modelica. And if you want to give data to CFD from Modelica, please remain the variable you want to exchange(inlet or outlet) in the select box. Generally, for the positive pressure room, you should remain "inlet" in your select box, for the negative pressure room the "outlet" should be remain and the "switch negative pressure room" should be checked.

*    Then set the variables that would be exchanged between Modelica and CFD
>    ![Exchange data](https://github.com/wenzheshang/BELab/blob/main/image_for_readme/exchange_variable.png)
>    **Notice**: The exchange variables' name from .fmu file should just be the variables' name in Modelica language, such as "SupplyAir.T". And the order of variables is very important, for example, if you want to send the data of "SupplyAir.T" from Modelica to "inlet.T" in Fluent, you have to write "SupplyAir.T inlet.T" in the Modelica side. The same thing is also true in the CFD side. And if there are many groups of exchange data, you should use ";" to split different group.

*    Then set time parameter in Modelica side
>    ![Time parameter](https://github.com/wenzheshang/BELab/blob/main/image_for_readme/set_time.png)
>    You should identify the simulate time and the interval of data exchange.

*    Finally cilck "Start Co-Simu" button and wait.
>    You can find the result saved in the file dictionary "Workdata\Fluent_Python" and "Workdata\Dymola_python", if you want to save more result, you can modify the source code to save what you want.

## Result
Here are some results for the BELab:
![Result1](https://github.com/wenzheshang/BELab/blob/main/image_for_readme/result1.png)
This is the result of coupling supply air velocity and temperature.
![Result2](https://github.com/wenzheshang/BELab/blob/main/image_for_readme/result2.png)
This is the result of coupling pressure difference between multi-zones.# BELab_distribute_version
