function [Ts,Inestability_flag]=timeSettleIdent(CV,Target,SP,por)
%% calculando el tiempo de establecimiento de la respuesta del MPC
% la idea principal es tomar pequeñas ventanas de tiempo y ver aquella en
% la cual el promedio es el valor estable que cumpla con el criterio del 5%
% El procedimiento es encontrar el momento a partir el cual todos los 
% tramos que le siguen  tienen la media en un rango determinado.
% Este funcion devuelve el instante de tiempo en el cual se cumple el
% la señal se mantiene en promedio por debajo de un valor de % determinado 
% por la variable por.
% 
%% Date: 08/05/2019
% Version 2.0 Date: 12/07/2019 
% by Victor
%%
step=10; %4 % EL step original era 10 pero fue modificado (4) para tener un mejor 
% resultado en la identificación de la respuesta ante un paso escalón de
% los modelos (26/09/2019 fecha de la modificación)
Tramos=zeros(ceil(length(CV)/step)-1,2);% se crea una matrix para almacenar los
%                                     valores de media y variancia de los
%                                     tramos previstos. Importante destacar
%                                     que la amplitud de estos tramos son
%                                     10 segundos.
% Tolerancia=0.05*Target;             % este valor escalar nos da el rango 
%                                     de tolerancia del error de la media
%                                     que se quiere alcanzar
% ToleranciaVar=0.15;
% Tramos=zeros(length(Tsim),1);
j=0;
for i=1:step:(ceil(length(CV))-step)
    j=j+1;
    Tramos(j,1)=mean(CV(i:(step+i)));
    Tramos(j,2)=var(CV(i:(step+i)));
    
end


%%
Ts_tramos=find(abs((round(Tramos(:,1),3)-(Target)))<(por*(SP(end)-SP(1))));
% Ts_tramos=find(abs((round(Tramos(:,1),3)-(Target))/(Target))<0.02); % te devuele los tiempos 
%  este método solo sirve para Tiempo de muestreo de un segundo donde la
%  posicion coincide con el tiempo

Ts=Inf;

for i=1:length(Ts_tramos)

x=Ts_tramos(i);

if length(Ts_tramos(i:end))==length(Tramos(x:end,1))
    Ts=(Ts_tramos(i)*step);%-(step-1);
    break
end

end

Inestability_flag=0;

if isinf(Ts)
    Inestability_flag=1;
end

end