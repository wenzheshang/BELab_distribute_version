"""
===============================
First framework by Wenzhe Shang @TJU
7/Dec/2022
Exe by Wenzhe Shang @TJU
7/Feb/2023
FMI support by Wenzhe Shang @TJU
5/Mar/2023
===============================
This is a python script for co-simulation between Modelica and Fluent;

The script was convert into EXE for spread and also as a soluation for a real project
in this way users could utilize this script without extra python konwledge;

JModelica could be used to produce FMU file for our couple simulation;
"""

from signal import signal
from PyQt5.QtWidgets import QApplication, QWidget,QSplashScreen
from PyQt5.QtGui import QPixmap, QCloseEvent, QImage
from string_gen import id_generator
from tkinter import filedialog
from dymola.dymola_interface import DymolaInterface
from buildingspy.io.outputfile import Reader
from software_back import Ui_Form
from fluent_corba import CORBA
from pyfmi import load_fmu

import numpy as np
import matplotlib.pyplot as plt
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd
import tkinter as tk
import time
import pathlib
import os, sys
import subprocess
import shutil
import csv


class LoadWin(QSplashScreen):
    def any(self):
        pass


class Win(QWidget,Ui_Form):
    def __init__(self, parent = None):
        super(Win, self).__init__(parent)
        self.setupUi(self)

        #初始化dymola设定记录
        dict_dymola_setName = {1:[]}
        dict_dymola_setValue = {1:[]}
       
        RoomSelect = {1:[]}

        dict_MFpassValue = {}
        dict_FMpassValue = {}

        #msh改变文件保存信号
        signalmsh = {1:[-1]}
        
        #代码仅执行一次标志
        smash_signal = [0]
        signal_simu_time = [1]

        #需要记录的热流字典
        fluxes_dict = {}

        #将热流字典里的量取出保存
        fluxesFloor_tocsv = []
        fluxesFront_tocsv = []
        T_tocsv = []
        p_tocsv = []

        #写一个字典型把exd导进去
        EXD = {'MF':[], 'FM':[]}

        use_file = '.fmu'

        self.cal_progressBar.setRange(0,100)
        

        #怎么做两个房间？同时运行Fluent吗？思考
        def RoomSwitch():
            self.mesh_input_line.setText('')
            self.boundary_TlineEdit.setText('')
            self.boundary_VlineEdit.setText('')
            self.cas_line.setText('')
            self.dat_line.setText('')
            self.outputV_line.setText('')
            signalmsh[1][0] = -signalmsh[1][0]#当两个房间切换时信号的变化
          
        def MeshButton_click():
            try:
                root = tk.Tk()
                root.withdraw()
                Filepath = filedialog.askopenfilename()
                self.mesh_input_line.setText(Filepath)
                scheme.execScheme(f'(read-case "{Filepath}")')

                #fluent 提前设置
                scheme.doMenuCommand("/define/model viscous ke-rng yes")
                scheme.doMenuCommand("/define/model energy yes no no no no")
                scheme.doMenuCommand("/define/operating-conditions gravity yes 0 9.8")
                #scheme.doMenuCommand("/mesh/scale 0.01 0.01 0.01")
            except:
                return

            result = scheme.execSchemeToString('(grid-check)')
            result = scheme.doMenuCommandToString("/mesh/check")
            ms =  open(os.path.join(workPath,'meshcheck.txt'),'w')
            ms.write(result)
            ms.close()
     
        def editChanged():
            textA = self.boundary_TlineEdit.text().strip()
            if textA == '':
                signalA = False
            else:
                signalA = True
            textB = self.boundary_VlineEdit.text().strip()
            if textB == '':
                signalB = False
            else:
                signalB = True
            self.boundaryInputButton.setEnabled(signalA and signalB)
            self.set_status_label.setText('Do set')
                
        def boundarySelectText():
            self.boundary_VlineEdit.setText('')
            self.boundary_TlineEdit.setText('')#槽函数，改变comboxbox时将box清空
            BoundaryName = self.Boundary_select.currentText()
            if self.NegitiveP.isChecked() == True:
                if BoundaryName.find('inlet') != -1:
                    self.Boundary_Vlabel.setText('请输入0')
                    self.Boundary_Tlabel.setText('送风温度(K))')  
                elif BoundaryName.find('wall') != -1:
                    self.Boundary_Tlabel.setText('壁面温度(K)')
                    self.Boundary_Vlabel.setText('请输入0')
                elif BoundaryName.find('outlet') != -1:
                    self.Boundary_Vlabel.setText('请输入0')
                    self.Boundary_Tlabel.setText('请输入0')
                else:
                    self.Boundary_Vlabel.setText('A U CRZ?')
                    self.Boundary_Tlabel.setText('HA HA HA')
            else:
                if BoundaryName.find('inlet') != -1:
                    self.Boundary_Vlabel.setText('请输入0')
                    self.Boundary_Tlabel.setText('请输入0')  
                elif BoundaryName.find('wall') != -1:
                    self.Boundary_Tlabel.setText('壁面温度(K)')
                    self.Boundary_Vlabel.setText('请输入0')
                elif BoundaryName.find('outlet') != -1:
                    self.Boundary_Vlabel.setText('请输入0')
                    self.Boundary_Tlabel.setText('请输入0')


        def boundarySetButton_click():#version1.0中实现手动输入边界名称，version2.0中希望能够自动识别
            try:
                BoundaryName = self.Boundary_select.currentText()
                MFKey = list(dict_MFpassValue.keys())
                #当inlet作为自由入口时,即房间负压设置生效时
                if self.NegitiveP.isChecked() == True:
                    if BoundaryName.find('inlet') != -1:
                        BoundaryT = self.boundary_TlineEdit.text().strip()
                        scheme.doMenuCommand("/define/boundary/inlet-vent "+BoundaryName+' yes no 0 no 0 no '+BoundaryT+' no yes yes no 0.06 no 0.04')#TUI命令实现,需要注意设置k,epsilon和压力损耗
                    elif BoundaryName.find('outlet') != -1:
                        for i in MFKey:
                            if i.find('outlet') != -1:
                                if i.find('.v') != -1:
                                    BoundaryV = dict_MFpassValue[i]
                        scheme.doMenuCommand("/define/boundary/mass-flow-outlet "+BoundaryName+' yes yes no '+str(BoundaryV))
                    elif BoundaryName.find('wall') != -1:
                        BoundaryT = self.boundary_TlineEdit.text().strip()
                        scheme.doMenuCommand('/define/boundary/wall '+BoundaryName+' 0 no 0 no yes temperature no '+ BoundaryT)
                #当outlet作为自由出口时
                else:
                    if BoundaryName.find('inlet') != -1:
                        for i in MFKey:
                            if i.find('inlet') != -1:
                                if i.find('.v') != -1:
                                    BoundaryV = dict_MFpassValue[i]
                                elif i.find('.T') != -1:
                                    BoundaryT = dict_MFpassValue[i]
                       #print(BoundaryT, BoundaryV)
                        scheme.doMenuCommand("/define/boundary/velocity-inlet "+BoundaryName+' no no yes yes no '+str(BoundaryV)+' no 0 no '+str(BoundaryT)+' no no yes 5 10')#TUI命令实现,需要注意最后两个数值用于设置湍流
                    elif BoundaryName.find('outlet') != -1:
                        scheme.doMenuCommand("/define/boundary/zone-type "+BoundaryName+" outflow")
                    elif BoundaryName.find('wall') != -1:
                        BoundaryT = self.boundary_TlineEdit.text().strip()
                        scheme.doMenuCommand("/define/boundary/wall "+BoundaryName+' 0 no 0 no yes temperature no '+ BoundaryT)
                
            except:
                self.set_status_label.setText('Set Error')
                return
            finally:
                self.set_status_label.setText('Set Down')
                
        def startSimulation_click():
            try:
                scheme.doMenuCommand("/solve/initialize/compute-defaults/all-zones")
                
                fluentUnit.setNrIterations(100)
                fluentUnit.calculate()
                self.cd_file_downloadButton.setEnabled(True)
               
                run_id = id_generator()
                
                for exd in range(len(EXD['FM'])):
                    FMName = EXD['FM'][exd]
                    FMName = FMName.split()
                    toModelicaName = FMName[1]
                    FluentName = FMName[0]

                    if FluentName.find('RoomT') != -1:
                        scheme.doMenuCommandToString('/report/volume-integrals/mass-avg cell-fuild () temperature yes simuT_'+run_id+'.txt')
                        Tem = open(os.path.join(workPath,'simuT_'+run_id+'.txt'), 'r', encoding='utf-8')
                        l_T = Tem.read()
                        item_T = l_T.split()
                        T_index = item_T.index('cell-fuild')+1

                        T_tocsv.append(float(item_T[T_index]))

                        dict_FMpassValue[toModelicaName] = float(item_T[T_index])

                    if FluentName.find('outlet_massflow') != -1:
                        scheme.doMenuCommandToString('/report/fluxes/mass-flow no outlet* () yes simu_'+run_id+'.txt')#保存到文件里
                        f = open(os.path.join(workPath,'simu_'+run_id+'.txt'), 'r', encoding='utf-8')
                        line = f.read()
                        item = line.split()
                        mf_index = item.index('outlet')+1
                        mass_flow = item[mf_index]
                        dict_FMpassValue[toModelicaName] = float(mass_flow)#增加出口处质量流量值
                    
                    if FluentName.find('inlet_pressureDifference') != -1:
                        scheme.doMenuCommandToString('/report/surface-integrals/area-weighted-avg inlet () pressure yes simuP_'+run_id+'.txt')#保存到文件里
                        pressure = open(os.path.join(workPath,'simuP_'+run_id+'.txt'), 'r', encoding='utf-8')
                        l_p = pressure.read()
                        item_p = l_p.split()
                        p_index = item_p.index('inlet')+1

                        p_tocsv.append(float(item_p[p_index]))
                        dict_FMpassValue[toModelicaName] = float(item_p[p_index])

                    if FluentName.find('fluxes') != -1:
                        scheme.doMenuCommandToString('/report/fluxes/heat-transfer yes yes simufluxes_'+run_id+'.txt')
                        fluxes = open(os.path.join(workPath,'simufluxes_'+run_id+'.txt'), 'r', encoding='utf-8')
                        l_fluxes = fluxes.read()
                        item_fluxes = l_fluxes.split()
                        for fluxes_name in('inlet', 'outlet', 'wall-ceiling', 'wall-floor', 'wall-front'):
                            fluxes_index = item_fluxes.index(fluxes_name)+1
                            fluxes_dict[fluxes_index] = float(item_fluxes[fluxes_index])

                            dict_FMpassValue[toModelicaName+fluxes_name] = float(item_fluxes[fluxes_index])

                            fluxesFloor_tocsv.append(fluxes_dict['wall-floor'])
                            fluxesFront_tocsv.append(fluxes_dict['wall-front'])
 
            except:
                self.set_status_label.setText('Simulation error, please check input')
                return
            # scheme.doMenuCommand()
            # scheme.doMenuCommand("/solve/set/time-step 0.01")
            # scheme.doMenuCommand("/solve/set/number-of-time-steps 350")
            # scheme.doMenuCommand("/solve/set/max-iterations-per-time-step 10")
            

        def fileDownload_click():
            try:
                scheme.doMenuCommand("f c n wcd test")
                if signalmsh[1][0] == 1:
                    FilePath_cas = os.path.join(r1wp,'test.cas')
                    FilePath_dat = os.path.join(r1wp,'test.dat')
                    shutil.move(str(workPath)+'/test.cas',FilePath_cas)
                    shutil.move(str(workPath)+'/test.dat',FilePath_dat)
                elif signalmsh[1][0] == -1:
                    FilePath_cas = os.path.join(r2wp,'test.cas')
                    FilePath_dat = os.path.join(r2wp,'test.dat')
                    shutil.move(str(workPath)+'/test.cas',FilePath_cas)
                    shutil.move(str(workPath)+'/test.dat',FilePath_dat)
                self.cas_line.setText(FilePath_cas)
                self.dat_line.setText(FilePath_dat)
                #outlet_Temperature = scheme.doMenuCommandToString("/report/heat-exchanger/outlet-temperature")
                
            except:
                self.cas_line.setText('Output error')
                self.dat_line.setText('Output error')
                self.outputV_line.setText('Output error')
                return

        def dymolaButton_click():
            root = tk.Tk()
            root.withdraw()
            Filepath = filedialog.askopenfilename()
            self.mulitzone_line.setText(Filepath)
            
        def RoomT_swich():
            self.Room_T_line.setText('')

        def RoomT_editchanged():
            textC = self.Room_T_line.text().strip()
            if textC == '':
                signalC = False
            else:
                signalC = True
            self.Room_T_Button.setEnabled(signalC)

        def RoomT_Input_click():
            RoomName = self.Room_select_box.currentText()+'.T'
            RoomT = float(self.Room_T_line.text())
            if RoomName in dict_dymola_setName[1]:
                dict_dymola_setValue[1][dict_dymola_setName[1].index(RoomName)] = RoomT
            else:
                dict_dymola_setName[1].append(RoomName)
                dict_dymola_setValue[1].append(RoomT)
        #用于记录设定参数
        
        def Door_swich():
            self.Door_leakage_line.setText('')
            self.cd_line.setText('')
            self.m_line.setText('')

        def Door_editchanged():
            textD = self.Door_leakage_line.text().strip()
            textE = self.cd_line.text().strip()
            textF = self.m_line.text().strip()
            signalD = False
            signalE = False
            signalF = False
            text = [textD, textE, textF]
            signal = [signalD,signalE,signalF]
            for i in range(3):
                if text[i] == '':
                    signal[i] = False
                else:
                    signal[i] = True
            self.doorButton.setEnabled(signal[0] and signal[1] and signal[2])

        def doorButton_click():
            doorNameleakage = self.door_select_box.currentText()+'.LClo'
            doorNamecd = self.door_select_box.currentText()+'.CDClo'
            doorNamem = self.door_select_box.currentText()+'.mClo'
            leakage = float(self.Door_leakage_line.text())
            cd = float(self.cd_line.text())
            m = float(self.m_line.text())
            if doorNameleakage in dict_dymola_setName[1]:
                dict_dymola_setValue[1][dict_dymola_setName[1].index(doorNameleakage)] = leakage
            else:
                dict_dymola_setName[1].append(doorNameleakage)
                dict_dymola_setValue[1].append(leakage)

            if doorNamecd in dict_dymola_setName[1]:
                dict_dymola_setValue[1][dict_dymola_setName[1].index(doorNamecd)] = cd
            else:
                dict_dymola_setName[1].append(doorNamecd)
                dict_dymola_setValue[1].append(cd)

            if doorNamem in dict_dymola_setName[1]:
                dict_dymola_setValue[1][dict_dymola_setName[1].index(doorNamem)] = m
            else:
                dict_dymola_setName[1].append(doorNamem)
                dict_dymola_setValue[1].append(m)

        def curve_Button_able():
            textG = self.curve_a_line.text().strip()
            if textG == '':
                signalG = False
            else:
                signalG = True
            textH = self.curve_a_line.text().strip()
            if textH == '':
                signalH = False
            else:
                signalH = True
            self.curve_Button.setEnabled(signalG and signalH)

        def cleaner_switch():
            self.curve_a_line.setText('')
            self.curve_b_line.setText('')

        def cleaner():
            CleanerNameL = self.Cleaner_selectbox.currentText()+'.A'
            a = float(self.curve_a_line.text())
            b = float(self.curve_b_line.text())
            m = b
            L = 20*(1.2/a)**(1/b)
            if CleanerNameL in dict_dymola_setName[1]:
                dict_dymola_setValue[1][dict_dymola_setName[1].index(CleanerNameL)] = L
            else:
                dict_dymola_setName[1].append(CleanerNameL)
                dict_dymola_setValue[1].append(L)
        #   净化模块

        # def CFD_room():    
        #     dict_dymola_setName[1].append('roomCFD.mflow_out')
        #     dict_dymola_setValue[1].append(-float(self.outputV_line.text()))
        #     #   CFD计算结果导入模块
        
        def end_button():
            textI = self.endtime_line.text().strip()
            textJ = self.interval_line.text().strip()
            if textI == '':
                signalI = False
            else:
                signalI = True
            if textJ == '':
                signalJ = False
            else:
                signalJ = True
            self.endtimeButton.setEnabled(signalI)
            self.intervalButton.setEnabled(signalJ)

        def simulate_time():
            endtime = float(self.endtime_line.text())
            return endtime
        
        def interval():
            intervals = int(self.interval_line.text())
            self.simstartButton.setEnabled(True)
            return intervals
        
        def dt_read():
            dt_use = float(self.dt_line.text())
            return dt_use
            

        def EXDconfirmButton():
            textMF = self.MFEXD1.text().strip()
            textFM = self.FMEXD1.text().strip()
            if textMF == '':
                signalMF = False
            else:
                signalMF = True

            if textFM == '':
                signalFM = False
            else:
                signalFM = True
            self.MFEXDconfirm.setEnabled(signalMF)
            self.FMEXDconfirm.setEnabled(signalFM)

        
        def ExchangeDataDistribute():
            FM = self.FMEXD1.text().strip()
            MF = self.MFEXD1.text().strip()
            FM = FM.split(';')
            MF = MF.split(';')
            EXD['FM'] = FM
            EXD['MF'] = MF

        def FMU_simulate(fmu_file, end_time, communicate_time, set_variable, set_value):
            self.multi_result_path_label.setText('Start Simu')
            Tstart = 0 # The start time.
            Tend = end_time
            
            model = load_fmu(fmu_file)

            model.set(set_variable, set_value)

            model.setup_experiment(start_time = Tstart) # Set the start time to Tstart
            model.enter_initialization_mode()
            model.exit_initialization_mode()
            eInfo = model.get_event_info()
            eInfo.newDiscreteStatesNeeded = True
            #Event iteration
            # while eInfo.newDiscreteStatesNeeded == True:
            #     model.enter_event_mode()
            #     model.event_update()
            #     eInfo = model.get_event_info() #这一部分似乎没啥用处
            
            model.enter_continuous_time_mode()

            # Get Continuous States
            x = model.continuous_states
            # Get the Nominal Values
            x_nominal = model.nominal_continuous_states
            # Get the Event Indicators
            event_ind = model.get_event_indicators()
            
            # Values for the solution
            # Retrieve the valureferences for the values 'CFD_roo.Room_MeanT'
            try:
                MFKey = list(EXD['MF'])
                FMKey = list(EXD['FM'])
                var1 = MFKey[0].split()[0]
                var2 = FMKey[0].split()[1]
                vref = [model.get_variable_valueref(var1)]+ \
                        [model.get_variable_valueref(var2)]
                t_sol = [Tstart]
                sol = [model.get_real(vref)]
            except:
                self.multi_result_path_label.setText('Name Error')
                return

            time = Tstart
            Tnext = Tend # Used for time events
            dt = dt_read()
            #value = 283.15
            
            number = 0
            processData = 0

            self.cal_progressBar.setValue(processData)
                

            while time < Tend and not model.get_event_info().terminateSimulation:
                #set progress bar
                #Compute the derivative of the previous step f(x(n), t(n))
                dx = model.get_derivatives()
                
                # Advance
                h = min(dt, Tnext-time)
                time = time + h
                
                # Set the time
                model.time = time
                
                # Set the inputs at the current time (if any)
                #model.set(vref, value)
                
                # Set the states at t = time (Perform the step using x(n+1)=x(n)+hf(x(n), t(n))
                # 对状态的更新是必须的，不可以省略
                x = x + h*dx 
                model.continuous_states = x

                # Get the event indicators at t = time
                try:
                    event_ind_new = model.get_event_indicators()
                except:
                    self.multi_result_path_label.setText('Step Number Error')
                    return
                
                # Inform the model about an accepted step and check for step events
                step_event = model.completed_integrator_step()
                
                # Check for time and state events
                time_event = abs(time-Tnext) <= 1.e-10
                state_event = True if True in ((event_ind_new>0.0) != (event_ind>0.0)) else False

                # Event handling
                if step_event or time_event or state_event:
                    model.enter_event_mode()
                    eInfo = model.get_event_info()
                    eInfo.newDiscreteStatesNeeded = True

                    if number >= communicate_time:

                        processData += int(Tend/communicate_time)
                        self.cal_progressBar.setValue(processData)

                        for exd in range(len(EXD['MF'])):
                            MFName = EXD['MF'][exd]
                            MFName = MFName.split()
                            toFluentName = MFName[1]
                            ModelicaName = MFName[0]

                            dict_MFpassValue[toFluentName] = model.get_real([model.get_variable_valueref(ModelicaName)])[0]
                            """注意需要将Modelica中单位和Fluent中单位做统一，如果没统一的话，需要将从Modelica中算出的参数在Modelcia
                               内进行相关处理后在输出"""

                            #dict_MFpassValue['supply_velocity'] = model.get_real([model.get_variable_valueref('SupplyAir.m_flow')])[0]/(1.2*0.1)
                        
                        boundarySetButton_click()
                        startSimulation_click()
                        (fM_variable, fM_data) = (list(dict_FMpassValue.keys()), list(dict_FMpassValue.values()))

                        for i in range(len(fM_variable)):
                            model.set(fM_variable[i], fM_data[i])
                        
                        number = 0
                    number = number + 0.001
                    
                    # Event iteration
                    while eInfo.newDiscreteStatesNeeded:
                        model.event_update('0') # Stops at each event iteration
                        eInfo = model.get_event_info()
                    # Retrieve solutions (if needed)
                if eInfo.newDiscreteStatesNeeded:
                    pass
                
                # Check if the event affected the state values and if so sets them
                if eInfo.valuesOfContinuousStatesChanged:
                    x = model.continuous_states
                
                # Get new nominal values.
                # if eInfo.nominalsOfContinuousStatesChanged:
                #     atol = 0.01*rtol*model.nominal_continuous_states
                
                # Check for new time event
                if eInfo.nextEventTimeDefined:
                    Tnext = min(eInfo.nextEventTime, Tend)
                else:
                    Tnext = Tend
                model.enter_continuous_time_mode()

                event_ind = event_ind_new
            
                # Retrieve solutions at t=time for outputs
                # bouncing_fmu.get_real,get_integer,get_boolean,get_string (valueref)
            
                t_sol += [time]
                sol += [model.get_real(vref)]

            # model.get_model_variables()
            # res = model.simulate(final_time=720)
            # t = res['time']
            # x1 = res['SupplyAir.T_in']
            mydataframe_fluent1 = pd.DataFrame({'FluxesFloorValue':fluxesFloor_tocsv})
            mydataframe_fluent2 = pd.DataFrame({'FluxesFront': fluxesFront_tocsv})
            mydataframe_fluent3 = pd.DataFrame({'TValue':T_tocsv})
            mydataframe_fluent4 = pd.DataFrame({'PValue':p_tocsv})
            mydataframe_fluent1.to_csv(os.path.join(dir_result, 'FluxesFloorV_general.csv'))
            mydataframe_fluent2.to_csv(os.path.join(dir_result, 'FluxesFrontV_general.csv'))
            mydataframe_fluent3.to_csv(os.path.join(dir_result, 'TV_general.csv'))
            mydataframe_fluent4.to_csv(os.path.join(dir_result, 'P_general.csv'))
            plt.subplot(211)
            plt.plot(t_sol,np.array(sol)[:,0])
            plt.subplot(212)
            plt.plot(t_sol,np.array(sol)[:,1])
            plt.savefig(os.path.join(dir_result, 'FMU_result.svg'))
            image = QImage(os.path.join(dir_result, 'FMU_result.svg'))
            self.Reslut_label.setPixmap(QPixmap.fromImage(image))
            self.Reslut_label.setScaledContents(True)

            
        def simulateButton_click():#这部分代码应当由dymola.egg更改为FMU
            if use_file == '.mo':
                try:
                    smash_signal[0] = smash_signal[0] + 1
                    ResultValue = []
                    
                    modelicaPath = pathlib.Path(os.environ["DymolaPath"])
                    #Library import
                    dirBuilding = os.path.join(modelicaPath,"Modelica/Library/Buildings-v8.0.0/Buildings 8.0.0")
                    #open Library
                    dymola.openModel(path=os.path.join(dirBuilding, 'package.mo'))
                    dymola.openModel(path=self.mulitzone_line.text())
                    problemName = 'Plant.plant_rectify_0105_correct'
                    endT = simulate_time()
                    intervals = interval()
                    step_time = endT/intervals
                        
                    #第一次执行模拟时采用输入的初始变量进行初始化
                    if signal_simu_time[0] == 1:
                        dymola_setName = dict_dymola_setName[1]
                        dymola_setValue = dict_dymola_setValue[1]
                        demo_name = 'demo_results'
                    #后面动态模拟采用根据fluent计算更改后的结果
                    else:
                        (dymola_setName, dymola_setValue) = (list(dict_FMpassValue.keys()), list(dict_FMpassValue.values()))
                        demo_name = 'demo_results'+str(signal_simu_time[0])    

                    result = dymola.simulateExtendedModel(
                        problem= problemName,
                        startTime=0,
                        stopTime=step_time,
                        numberOfIntervals=0,
                        outputInterval=0.0,
                        method="Dassl",
                        tolerance=0.0001,
                        fixedstepsize=0.0,
                        resultFile=os.path.join(dir_result,demo_name),
                        initialNames=dymola_setName,
                        initialValues=dymola_setValue,
                        autoLoad=True
                        )

                    #self.multi_result_path_label.setText(demo_name)

                except:
                    print('error1')
                    log = dymola.getLastError()
                    f =  open(os.path.join(dir_result,'error1.txt'),'w')
                    f.write(log)
                    f.close()
                    return

                try:
                    status = result[0]

                except: 
                    print('error2')
                    log = dymola.getLastError()
                    f =  open(os.path.join(dir_result,'error2.txt'),'w')
                    f.write(log)
                    f.close()
                    return
                    
                if not status:
                    print('error3')
                    log = dymola.getLastError()
                    f =  open(os.path.join(dir_result,'error3.txt'),'w')
                    f.write(log)
                    f.close()
                    return
                else:
                    #成功模拟后输出结果部分,加保存excel功能
                    #以下代码保存excel文件
                    result_path = os.path.join(dir_result,demo_name+'.mat')
                    r = Reader(result_path,'dymola')

                    result_name = 'reslut'+str(signal_simu_time[0])
                    signal_simu_time[0] = signal_simu_time[0] + 1
                
                    ResultVarName = r.varNames() #获取所有结果变量名
                    for i in range(len(ResultVarName)):
                        (t,r_ser) = r.values(ResultVarName[i])
                        ResultValue.append(r_ser[-1])
                    mydataframe = pd.DataFrame({'VarName':ResultVarName,'Value':ResultValue})
                    mydataframe.to_csv(os.path.join(dir_result, result_name+'.csv'))#将所有结果保存到.csv文件中，以备下次读取

                    
                    for exd in range(len(EXD['MF'])):
                        MFName = EXD['MF'][exd]
                        MFName = MFName.split()
                        toFluentName = MFName[1]
                        ModelicaName = MFName[0]
                        (time_a, value_a) = r.values(ModelicaName)
                        dict_MFpassValue[toFluentName] = value_a[-1]

                    # (time_1,SupplyV) = r.values('SupplyAir.m_flow')
                    # (time_2,SupplyT) = r.values('SupplyAir.T_in')
                    # dict_MFpassValue['supply_T'] = SupplyT[-1]
                    # dict_MFpassValue['supply_velocity'] = SupplyV[-1]/(1.2*0.1)

                    #以下代码传出需要进行CFD联合计算的房间名，仅需要执行一次  
                    if smash_signal[0] == 1:
                        try:
                            room = r.varNames('CFD_')
                            RoomName = []
                            for i in range(len(room)):
                                rName = room[i].split('_')
                                RoomName.append(rName[1])
                            RoomName = list(set(RoomName))
                            self.r1_checkBox.setText(RoomName[0])
                            self.r2_checkBox_2.setText(RoomName[1])
                        except:
                            self.multi_result_path_label.setText('VarName set Error, Please Check .mo')
                    else:
                        return
                
            else:
                dymola_setName = dict_dymola_setName[1]
                dymola_setValue = dict_dymola_setValue[1]
                t_all = simulate_time()
                t_c = interval()
                file_name = self.mulitzone_line.text()
                FMU_simulate(file_name, t_all, t_c, dymola_setName, dymola_setValue)


        def Room1_select():
            if self.r1_checkBox.isChecked() == True:
                RoomSelect[1].append(self.r1_checkBox.text())
                self.rs_comboBox.addItem(self.r1_checkBox.text())
            else:
                RoomSelect[1].remove(self.r1_checkBox.text())
                self.rs_comboBox.removeItem(self.rs_comboBox.findText(self.r1_checkBox.text()))
        def Room2_select():
            if self.r2_checkBox_2.isChecked() == True:
                RoomSelect[1].append(self.r2_checkBox_2.text())
                self.rs_comboBox.addItem(self.r2_checkBox_2.text())
            else:
                RoomSelect[1].remove(self.r2_checkBox_2.text())
                self.rs_comboBox.removeItem(self.rs_comboBox.findText(self.r2_checkBox_2.text()))
        #思考如果未知房间个数该怎么办？
        
        def RoomSelect_result():
            try:
                rho = 1.2
                result_path = os.path.join(dir_result,'demo_results.mat')
                r = Reader(result_path,'dymola')
                rcy = len(RoomSelect[1])
                if rcy > 0:
                    for i in range(rcy):
                        #判断房间名称属于哪一个 
                        (time, v_flow) = r.values('sen'+RoomSelect[1][i][1:]+'.V_flow')
                        if RoomSelect[1][i][1:] in self.r1_checkBox.text():
                            dict_MFpassValue[self.r1_checkBox.text()] = v_flow[-1]*rho
                            
                        if RoomSelect[1][i][1:] in self.r2_checkBox_2.text():
                            dict_MFpassValue[self.r2_checkBox_2.text()] = v_flow[-1]*rho #计算两个房间中传递的参数             
                else:
                    self.multi_result_path_label.setText('Please select Coupling room')
                    return
            except:
                return
        
        # def Dynamic_Coupling_Control():
        #     intervals = interval()

        #     for simulate_times in range(intervals):
        #         startSimulation_click()
        #         simulateButton_click() 
        #         boundarySetButton_click()
            #print(fluxesFloor_tocsv,T_tocsv)
            # mydataframe_fluent = pd.DataFrame({'FluxesFloorValue':fluxesFloor_tocsv, 'FluxesFront': fluxesFront_tocsv, 'TValue':T_tocsv})
            # mydataframe_fluent.to_csv(os.path.join(dir_result, 'room_general.csv'))#将所有结果保存到.csv文件中，以备下次读取


        
        #设置按钮不可用
        self.cd_file_downloadButton.setEnabled(False)
        self.boundaryInputButton.setEnabled(False)
        self.Room_T_Button.setEnabled(False)
        self.doorButton.setEnabled(False)
        self.curve_Button.setEnabled(False)

        self.cal_progressBar.setValue(0)
        self.endtimeButton.setEnabled(False)
        self.intervalButton.setEnabled(False)
        self.simstartButton.setEnabled(False)

        self.MFEXDconfirm.setEnabled(False)
        self.FMEXDconfirm.setEnabled(False)

        self.r1_checkBox.setText('')
        self.r2_checkBox_2.setText('')

        #控件连接：
        self.MeshButton.pressed.connect(MeshButton_click)

        self.Boundary_select.currentIndexChanged.connect(boundarySelectText)
        self.boundary_TlineEdit.textChanged.connect(editChanged)
        self.boundary_VlineEdit.textChanged.connect(editChanged)
        self.boundaryInputButton.pressed.connect(boundarySetButton_click)

        #self.fluentSimuButton.pressed.connect(Dynamic_Coupling_Control)
        self.cd_file_downloadButton.pressed.connect(fileDownload_click)

        self.mulitzone_selectButton.pressed.connect(dymolaButton_click)
        self.Room_select_box.currentIndexChanged.connect(RoomT_swich)
        self.Room_T_line.textChanged.connect(RoomT_editchanged)
        self.Room_T_Button.pressed.connect(RoomT_Input_click)

        self.door_select_box.currentIndexChanged.connect(Door_swich)
        self.Door_leakage_line.textChanged.connect(Door_editchanged)
        self.cd_line.textChanged.connect(Door_editchanged)
        self.m_line.textChanged.connect(Door_editchanged)
        self.doorButton.pressed.connect(doorButton_click)
        self.curve_a_line.textChanged.connect(curve_Button_able)
        self.curve_b_line.textChanged.connect(curve_Button_able)
        self.Cleaner_selectbox.currentIndexChanged.connect(cleaner_switch)
        self.curve_Button.pressed.connect(cleaner)
        
        self.endtime_line.textChanged.connect(end_button)
        self.interval_line.textChanged.connect(end_button)
        self.endtimeButton.pressed.connect(simulate_time)
        self.intervalButton.pressed.connect(interval)

        self.simstartButton.pressed.connect(simulateButton_click)

        self.r1_checkBox.stateChanged.connect(Room1_select)
        self.r2_checkBox_2.stateChanged.connect(Room2_select)
        #self.Rs_Button.pressed.connect(RoomSelect_result)

        self.rs_comboBox.currentIndexChanged.connect(RoomSwitch)

        self.MFEXD1.textChanged.connect(EXDconfirmButton)
        self.FMEXD1.textChanged.connect(EXDconfirmButton)
        self.MFEXDconfirm.pressed.connect(ExchangeDataDistribute)
        self.FMEXDconfirm.pressed.connect(ExchangeDataDistribute)

        dymola = DymolaInterface()
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        fluentProcess.kill()
        return super().closeEvent(a0)


if __name__=='__main__': 
    app=QApplication(sys.argv)
    #w1=Loding()
    splash=LoadWin()
    cur_path_ =  os.path.abspath(os.path.dirname(__file__))
    root_path_ = cur_path_
    splash.setPixmap(QPixmap(root_path_+'\load_pic.png')) 
    splash.showMessage('Fluenlica is loading...')
    splash.show()

    ##############################################################################
    # 获取根目录，定义Fluent工作目录
    now_time = time.strftime('%Y-%m-%d_%H-%M', time.localtime())
    cur_path =  os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path
    workPath =pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time)
    r1wp = pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time+"/room1")#r1wp means room1 workpath
    r2wp = pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time+"/room2")#r2wp means room2 wprkpath
    folder1 = os.path.exists(workPath)
    folder2 = os.path.exists(r1wp)
    folder3 = os.path.exists(r2wp)
    if not folder1:
        os.makedirs(pathlib.Path(root_path+"/Workdata/Fluent_Python/"+now_time))
    if not folder2:
        os.makedirs(r1wp)
    if not folder3:
        os.makedirs(r2wp)

    #定义Modelica工作目录
    dir_result =root_path+"/Workdata/Dymola_python/"+now_time
    folder = os.path.exists(dir_result)
    if not folder:
        os.makedirs(dir_result)

    # 清除之前存在的aaS*.txt文件
    aasFilePath = workPath/"aaS_FluentId.txt"
    for file in workPath.glob("aaS*.txt"):
        file.unlink()

    #fluent设置
    root_name = ["AWP_ROOT222","AWP_ROOT221","AWP_ROOT212","AWP_ROOT211","AWP_ROOT202","AWP_ROOT201","AWP_ROOT192","AWP_ROOT191",
                    "AWP_ROOT182","AWP_ROOT181","AWP_ROOT172","AWP_ROOT171","AWP_ROOT162","AWP_ROOT161","AWP_ROOT152","AWP_ROOT151"]
    fluent_exist = False
    for rn in root_name:
        env_exist = os.getenv(rn,'null')
        if env_exist != 'null':
            ansysPath = pathlib.Path(os.environ[str(rn)])
            fluent_exist = True
            break
    
    fluentExe = str(ansysPath/"fluent"/"ntbin"/"win64"/"fluent.exe")

    # 启动Fluent软件,使用-hidden可以隐藏fluent的GUI界面
    if fluent_exist:
        fluentProcess = subprocess.Popen(f'"{fluentExe}" 3ddp -aas -hidden', shell=True, cwd=str(workPath))#-hidden
    else:
        error = 'no right fluent verison exist on this machine'
        starterror =  open(os.path.join(workPath,'startError.txt'),'w')
        starterror.write(error)
        starterror.close()
        sys.exit()

    # 监控aaS_FluentId.txt文件生成，等待corba连接
    while True:
        try:
            if not aasFilePath.exists():
                time.sleep(0.2)
                continue
            else:
                if "IOR:" in aasFilePath.open("r").read():
                    break
        except KeyboardInterrupt:
            sys.exit()
    # 初始化orb环境
    orb = CORBA.ORB_init()
    # 获得Fluent实例单元
    fluentUnit = orb.string_to_object(aasFilePath.open("r").read())
    scheme = fluentUnit.getSchemeControllerInstance()
    ##############################################################################

    app.processEvents()  # 处理主进程事件
    #主窗口
    window = Win()
    window.show()
    splash.deleteLater()
    sys.exit(app.exec())
    
    


    