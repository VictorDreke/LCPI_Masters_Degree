function r_wi=watchDogIdent(CV,SP)
%%
% Esta funci�n se usa para implementar el �dice denominado Watchdog Index,
% proposto visto en la tesis del PECE de Christiam Alvarado.En teor�a este
% valor r_wi se deber�a mantener menor que 3.
%% Date: 12/07/2019
% Last Checkup: 12/07/2019 
% by Victor
%%
s1_square=(1/(length(CV)-1))*sum((CV-SP).^2);
s2_square=(1/2)*(1/(length(CV)-1))*sum((CV(1:length(CV)-1)-CV(2:end)).^2);

r_wi=s1_square/s2_square;

end