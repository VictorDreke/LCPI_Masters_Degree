function Mp=overShootIdent (CV, Target,Tempo)
%% function overShootIdent (CV, Target,Tempo)
%  Esta función devuelve el máximo sobrepico en porciento con respecto al
%  erro de estado estacionario del sistema. Para implementar esta función
%  es necesario entrar como datos el vector con los datos del sistema
%  (CV),el valor final (Target) y el arreglo Tempo=[Tr Ts] que está compuesto  
%  porel tiempo de subida y el tiempo de establecimiento.  Como esta
%  señales tiene presencia marcada de ruido se trbaja con los valores
%  promedios con una ventana de 10 segundos.
%% Date: 12/07/2019
% Last Checkup: 12/07/2019 
% by Victor
%%
step=4; % Amplitud del tramo para ejecutar la función.
% EL step original era 10 pero fue modificado para tener un mejor 
% resultado en la identificación de la respuesta ante un paso escalón de
% los modelos (26/09/2019 fecha de la modificación)
Tramos=zeros(ceil(length(CV)/step),2);% se crea una matrix para almacenar los
%                                     valores de media y variancia de los
%                                     tramos previstos. Importante destacar
%                                     que la amplitud de estos tramos son
%                                     10 segundos.
%Tolerancia=-0.02*Target;               % este valor escalar nos da el rango 
%                                     de tolerancia del error de la media
%                                     que se quiere alcanzar
% Tramos=zeros(length(Tsim),1);
j=1;
for i=1:step:(ceil(length(CV))-step)
    
    Tramos(j,1)=mean(CV(i:(step+i)));
    Tramos(j,2)=var(CV(i:(step+i)));
    j=j+1;
end

%%
if (Tempo(1)<=Tempo(2))
    
    Mp=max(Tramos(ceil(Tempo(1)/step):ceil(Tempo(2)/step),1))-(Target);
    Mp=Mp/(Target);
%     Mp=max(Tramos(ceil(Tempo(1)/step):ceil(Tempo(2)/step),1));
else
    Mp=0;
end

end