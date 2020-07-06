% This script simulated the pH Neutralization plant controlled with a MPC.
% In this case, the variable Modelo_PH_C and Modelo_NIVEL_C are the models
% used by the MPC to control pH and Level control loop of the plant, 
% respectivily. If you want to use a proposed model go to the Porposed
% Model section.

%% ---------------------------- Cleaning Memory ------------------------ %%

clc; clear all;

%% ------------------------------- Add Path ---------------------------- %%

addpath('2. Data')
addpath('1. KPI functions')
%% ------------------ Initialization of the Simulation ----------------- %%

load('Modelo_LCPI.mat', 'Modelo_LCPI') % Loading Models 
A=1;
B=Modelo_LCPI.pH.p7.B{1,3};
C=Modelo_LCPI.pH.p7.C;
D=1;
F=Modelo_LCPI.pH.p7.F{1,3};
NoiseVariance=Modelo_LCPI.pH.p7.NoiseVariance;
Ts=15;

Modelo_PH=idpoly(A,B,C,D,F,NoiseVariance,Ts);
Modelo_PH=d2d(tf(Modelo_PH),1);
Modelo_PH=Modelo_PH/dcgain(Modelo_PH);

% 
A=1;
B=Modelo_LCPI.Nivel.p7.B{1,1};
C=1;
D=1;
F=Modelo_LCPI.Nivel.p7.F{1,1};
NoiseVariance=Modelo_LCPI.Nivel.p7.NoiseVariance;
Ts=30;

Modelo_NIVEL=idpoly(A,B,C,D,F,NoiseVariance,Ts);            
Modelo_NIVEL=d2d(tf(Modelo_NIVEL),1);
Modelo_NIVEL=Modelo_NIVEL/dcgain(Modelo_NIVEL);

%% ---------------------- Loading the Digital Twin --------------------- %%

% Modelo_PH_C = Modelo_PH;       % Use this models to control the pH control 
%   with digital twin of the plant.
Modelo_NIVEL_C = Modelo_NIVEL; % Do not change, please. 

%% --------------------- Proposed Model ------------------------------- %%
% In this section, we declare the new model proposed to be used on the MPC.
kp=0.4; tau=126; zeta = 0.75;
Modelo_PH_C = tf(kp,[15 1]);%[tau^2, 2*zeta*tau, 1]); % Use this models to control
%   the pH control loop with the new model.

%% --------------------- MPC Initialization --------------------------- %%
Tim_MPC = 60;       % MPC's sample time

MPCScriptNivel      % MPC of the Level Control Loop
MPCScriptPH         % MPC of the pH Control Loop

Tsim=30000;         % Simulation Time

%% ---------------------- Simulation of the Plant --------------------- %%

sim('MPC_de_referencia_Sim.slx')

%% ------------------------- Visualization ---------------------------- %%
fig_1 = figure;
stairs(SP_pH, '--r', 'LineWidth', 2);
hold on
plot(CV_pH, 'b', 'LineWidth', 2);
hold off
grid on
xlabel('Time(s)', 'FontSize', 12)
ylabel('pH', 'FontSize', 12)
title('Response of the plant controlled by the MPC', 'FontSize', 14)
axis([4500 7000 min(CV_pH(4500:7000))-0.1  max(CV_pH(4500:7000))+0.1])
legend('Setpoint', 'Plant Response', 'location', 'best')
%% ------------------------- KPI calculation -------------------------- %%
DinConPerformance=perfomanceTemp(CV_pH,SP_pH,MV_pH)
