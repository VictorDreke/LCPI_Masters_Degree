function [IAE,ITAE]=IntAbsError(x1,x2,T)
%% [IAE ITAE]=IntAbsError(x1,x2,T) es algoritmo para calcular los índices 
% IAE, ITAE. 
%  x1 valor estimado
%  x2 valor medido
%  Tiempo de muestreo
%% Date: 08/06/2019
% Version 2.0 Date: 10/07/2019 
% by Victor
%% Acomodacion de los datos
 % Asegurandome que los datos sea un array de tipo N by 1 para los datos
if (size(x1,1)~=1 && size(x1,2)~=1)
    error('x1 need to be N by 1 vector')
else
    if(size(x1,2)~=1)
        x1=x1';
    end
end

if (size(x2,1)~=1 && size(x2,2)~=1)
    error('x2 need to be N by 1 vector')
else
    if(size(x2,2)~=1)
        x2=x2';
    end
end

if (length(x1)~=length(x2)) % Creando vectores con la misma dimension
    fprintf('Vector´s dimension are different, it may cause error\n \n')
    nwLngth=min([length(x1), length(x2)]);
    x1=x1(1:nwLngth); x2=x2(1:nwLngth);
    t=1:T:nwLngth;
else
    t=1:T:length(x1); % este vector contiene los valores de tiempo
end

%%
IAE=sum(abs(x1-x2))/length(t);
ITAE=sum(t*abs(x1-x2))/length(t);

end
