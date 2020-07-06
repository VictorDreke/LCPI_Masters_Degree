% StepinformationKPI
% Este script permite obtener las volares de la respuesta temporal del
% sistema.En este caso es usado particularmente para ser utilizados con
% la simulaciones de los MPC sin ruido.
clear all


StepInformationH=cell(3150,1);
StepInformationPH=cell(3150,1);

load('index_KPI.mat')

for i=1:length(StepInformationH)

    if (index_finalH{i,2}~="NaN")
        Head="MPCh_SimC_20200205_";    
        load(Head+string(i),'PV_Nivel') 
        StepInformationH{i,1}=stepinfo(PV_Nivel(2999:1:9999)-PV_Nivel(2999),0:1:7000,'SettlingTimeThreshold',...
                                            0.02,'RiseTimeThreshold',[0.05 0.95]);
    end
    
    if (index_finalPH{i,2}~="NaN")
        Head="MPCph_SimC_20200205_";                                 
        load(Head+string(i),'PV_PH')                                 
        StepInformationPH{i,1}=stepinfo(PV_PH(2999:1:9999)-PV_PH(2999),0:1:7000,'SettlingTimeThreshold',...
                                            0.02,'RiseTimeThreshold',[0.05 0.95]);
    end

end