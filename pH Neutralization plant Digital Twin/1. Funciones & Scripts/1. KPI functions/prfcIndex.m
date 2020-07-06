function pi=prfcIndex(CV)
% A Perfomance Index is implemented based on the () thesis. In this
% implementation wsa used to ohters main index: one was rising time (tr)and
% the other one was Variability Index (vi). In the case, of the is a
% normalized scalar value between 0 & 100% been 100% the optimal value of a
% good controller.
% 
% clear ; close all; clc
% load ('examgrades')

% y=grades(:,2);
n=length(CV);
sensibility=0.001*max(CV);

% dsv_std_fbc -> minimum theoric deviation
% dsv_std_cap -> standar deviation capacity function
% dsv_std_tot -> standar deviation's total
% vi ->Variability Index
% sensibility -> is a sensibility fator normally considered 0,1% of the scale
% pi -> perofmance index (Harris's index)

dsv_std_tot=std(CV);
dsv_std_cap=sqrt(sum((CV(2:end)-CV(1:n-1)).^2)/(2*n-2));

dsv_std_fbc=dsv_std_cap*sqrt(2-(dsv_std_cap/dsv_std_tot)^2);

vi=100*(1-((dsv_std_fbc+sensibility)/(dsv_std_tot+sensibility)));

pi=100-vi;
end

