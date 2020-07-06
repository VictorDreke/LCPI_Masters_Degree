function [std_vd_pers,var_2,var]=dinmcVaribility(CV,SP)
%% dinmcVaribility(CV,SP)
%  Esta funci�n se utiliza para calcular los �ndices de variabilidad de la
%  modelo utilizado para simular e implementar en el mpc, basado en las
%  m�tricas de desviaci�n estandar, variabilidad, watchdog y harris.
%% Normalizar, debido al hecho que los valores pueden promediar cero y  se 
% invalidan todos estas m�tricas, propuestas. 

% Temp=Norm_Christiam([CV;SP],2,6);
% CV=Temp(1:length(CV),1);
% SP=Temp(length(CV)+1:end,1);
% plot([CV,SP])
% SP=Norm_Christiam(SP,2,6)
%%
% Formula para calcular la variabilidad 
var=std(CV)/mean(CV);


%%
% Basado en Harris y en Watchdog se plantea esta m�trica de variabilidad
% relativa. La idea aqu� es encontrar el promedio error relativos con
% respecto al setpoint de la variaci�n de la se�al examinda. Desglozando en
% pasos se calcula la sumatoria de los errores absolutos de la difernecia 
% de la se�al en el instante i actual con respecto al instante anterior, 
% dividida por el promedio del setpoint para los dos valores 
% seleccionados


var_2=(1/(length(CV)-1))*sum(abs(CV(1:length(CV)-1)-CV(2:end))./((SP(1:length(CV)-1)+SP(2:end))/2));

%%
% Se caluala la desviaci�n estandar pero con una leve alteraci�n, sustiuir
% el promedio de la se�al por el setpoint 


std_vd_pers=(1/length(CV))*sum(abs((CV-SP)./SP)); % Revisarlo no me gustan el rango valores var�a muy poc

end
