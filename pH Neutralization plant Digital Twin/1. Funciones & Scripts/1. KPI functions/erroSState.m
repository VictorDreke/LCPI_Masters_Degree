function [ess1,Inestability_flag,ess]=erroSState(CV, Target)
%% [ess,inestability_flag]=erroSState(CV, Target)
%  Se calcula el error de estado estacionario de la planta Clarke
%  controlada tanto con MPC como controlador PI. Este valor es calculado de
%  se toma el valor promedio de los ultimos 320 segundos de simulación. 
%  Y además se calcula que estos tramos 
%  Nota importante: trabajar siempre con un target diferente de 0.
%% Date: 08/05/2019
% Version 2.0 Date: 12/07/2019 
% by Victor
%%
 
 step=floor(length(CV)/10); % Distancia del paso para realizar la funcion
%                                 divido la secuencia en diez tramos
%                                 iguales
 
 
ess1=(mean(CV(length(CV)-(2*step):end))-Target); % se calcula la media de los ultimos 320s
ess=abs(ess1);
%                                   
% std_total=std(CV);

% Calculo de la media y desviacion standar de los ultimos 4 tramos de 80s 
 
 tramo_start=length(CV)-(4*step);
 tramo_end=length(CV)-(3*step);
 
ess_tramo1=abs(mean(CV(tramo_start:tramo_end,1))-Target);
std_ss_tramo1=std(CV(tramo_start:tramo_end));

tramo_start=length(CV)-(3*step);
tramo_end=length(CV)-(2*step);
 
ess_tramo2=abs(mean(CV(tramo_start:tramo_end,1))-Target);
std_ss_tramo2=std(CV(tramo_start:tramo_end,1));

tramo_start=length(CV)-(2*step);
tramo_end=(length(CV)-(1*step));

ess_tramo3=abs(mean(CV(tramo_start:tramo_end,1))-Target);
std_ss_tramo3=std(CV(tramo_start:tramo_end,1));

tramo_start=length(CV)-(1*step);
tramo_end=length(CV);


ess_tramo4=abs(mean(CV(tramo_start:tramo_end,1))-Target);
std_ss_tramo4=std(CV(tramo_start:tramo_end,1));

if (ess_tramo1>=ess_tramo2 && ess_tramo2>=ess_tramo3 && ess_tramo3>=ess_tramo4)
%     Comprobar que la media de los tramos vayan decreciendo secuencialmente,
%     demostrando estabilidad del sistema.
    Inestability_flag=0;
elseif (ess_tramo1<ess_tramo2 && ess_tramo2<ess_tramo3 && ess_tramo3<ess_tramo4)
%     Comprobar que la media de los tramos vayan creciendo secuencialmente,
%     demostrando inestabilidad del sistema.    
    Inestability_flag=1;
elseif (std_ss_tramo1<std_ss_tramo2 && std_ss_tramo2<std_ss_tramo3 && std_ss_tramo3<std_ss_tramo4)
%     Comprobar que la std de los tramos vayan creciendo secuencialmente,
%     demostrando inestabilidad del sistema.       
    Inestability_flag=1;
elseif ((abs(ess-ess_tramo4)/(ess+Target))>0.1)
%     Comprobar que último tramo tenga un error mayor del 10% con respecto 
%     a la media total, demostrando inestabilidad del sistema.           
    Inestability_flag=1;
elseif ((abs(ess-ess_tramo4)/(ess+Target))<0.1)
%     Comprobar que último tramo tenga un error menor del 10% con respecto 
%     a la media total, demostrando estabilidad del sistema.      
    Inestability_flag=0;
else
    Inestability_flag=2;
end
end