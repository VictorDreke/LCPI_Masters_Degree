function  DinConPerformance=perfomanceTemp(CV_H,SP_H,MV_H)
%  Funcin para calcular los KPI de una respuesta determinada. Los valores
%  de tstart est�n definidos para los resultados de las simulaciones de los
%  MPC con los modelos originales com se muestran en las figura de la
%  carpeta: E:\Victor Reyes\20200205_Backup_From_DELL\
%               20200205_PNpH_Victor_OW01\
%                   6. Simulacion del MPC con Modelos Originales\2. Figures
%%

tstart=3000; 
tend=5000+4999; 
T=1;
CV=CV_H;
SP=SP_H;   
MV=MV_H;
[ess1,Inestability_flage,ess]=erroSState(CV(tstart:tend), SP(tend-1));
              
Target=SP(tend-1)+ess1;
                
Trise=timeRiseIdent(CV(tstart:tend-1), Target);
[Ts,Inestability_flag]=timeSettleIdent(CV(tstart:tend-1), Target,SP(tstart:tend-1),0.02);
if isinf(Trise)||isinf(Ts)||(Trise-Ts)==0
    Mp=0;
else
    Mp=overShootIdent (CV(tstart:tend), Target,[Trise Ts]);
end
r_wi=watchDogIdent(CV(tstart:tend),SP(tstart:tend));
pi=prfcIndex(CV(tstart:tend));
[~,IAU]=IntAbsError(MV,MV-MV,T);

% ----------------Agregado en la versi�n 2.0--------------
[std_vd_pers,var_2,var]=dinmcVaribility(CV(tstart:tend)+2,...
                                            SP(tstart:tend)+2);
% --------------------------------------------------------
 

% -------------- StepInformation -------------------------

t=stepinfo(CV(4999:1:9999)-CV(4999),0:1:5000,'SettlingTimeThreshold',...
                                            0.02,'RiseTimeThreshold',[0.05 0.95]);
% --------------------------------------------------------
DinConPerformance=[pi, r_wi, IAU, ess, t.RiseTime, t.SettlingTime-41,...
                    t.Overshoot,...
                     Inestability_flage+Inestability_flag,...
                        std_vd_pers,var_2,var];
 DinConPerformance = array2table(DinConPerformance,'VariableNames', ...
     {'Harris','Watchdog', 'IAU','Ess','Rise Time','Settling Time',...
     'Overshoot','Flag','MESR','MRSR','Variability'});               
                

end
                
