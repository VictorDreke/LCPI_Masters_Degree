function tiempo=timeRiseIdent(CV, Target)
%% calculando el tiempo de subida de la respuesta del MPC
% la idea principal es tomar pequeñas ventansa de tiempo y ver aquella en
% la cual el promedio se el valor estable en este caso y que la variancia
% se mantenga dentro de un valor de tolerancia
%% Date: 08/05/2019
% Version 2.0 Date: 12/07/2019 
% by Victor
%%

step=4; % Amplitud del tramo para ejecutar la función.

Tramos=zeros(ceil(length(CV)/step),2);% se crea una matrix para almacenar los
%                                     valores de media y variancia de los
%                                     tramos previstos. Importante destacar
%                                     que la amplitud de estos tramos son
%                                     10 segundos.
Tolerancia=-0.02*Target;               % este valor escalar nos da el rango 
%                                     de tolerancia del error de la media
%                                     que se quiere alcanzar
% Tramos=zeros(length(Tsim),1);
j=1;
for i=1:step:(ceil(length(CV))-step)
    
    Tramos(j,1)=mean(CV(i:(step+i)));
    Tramos(j,2)=var(CV(i:(step+i)));
    j=j+1;
end

tiempo=find((Tramos(:,1)-Target)>=Tolerancia,1,'first'); % Escoger el primer
%                                       tramo  con media mas cercano al
%                                       objetivo al setpoint.
tiempo=(tiempo*step)-(step-1);                   % Obteniendo el valor de tiempo real

if isempty(tiempo)
    tiempo=Inf;
end


    
end