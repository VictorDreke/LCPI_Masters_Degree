%% create MPC controller object with sample time
mpcNivel_VD = mpc(Modelo_NIVEL_C, Tim_MPC);
%% specify prediction horizon
mpcNivel_VD.PredictionHorizon = 60;
%% specify control horizon
mpcNivel_VD.ControlHorizon = 10;
%% specify nominal values for inputs and outputs
mpcNivel_VD.Model.Nominal.U = 65;
mpcNivel_VD.Model.Nominal.Y = 65;
%% specify constraints for MV and MV Rate
mpcNivel_VD.MV(1).Min = 0;
mpcNivel_VD.MV(1).Max = 85;
mpcNivel_VD.MV(1).RateMin = -5;
mpcNivel_VD.MV(1).RateMax = 5;
%% specify constraints for OV
mpcNivel_VD.OV(1).Min = 45;
mpcNivel_VD.OV(1).Max = 85;
%% specify weights
mpcNivel_VD.Weights.MV = 0;
mpcNivel_VD.Weights.MVRate = 0.3;   % Segun los trabajos de Manuel
mpcNivel_VD.Weights.OV = 0.7;       % Segun los trabajos de Manuel
mpcNivel_VD.Weights.ECR = 100000;
%% specify simulation options
% options = mpcsimopt();
% options.Model = Modelo_NIVEL_S;
% options.RefLookAhead = 'off';
% options.MDLookAhead = 'off';
% options.Constraints = 'on';
% options.OpenLoop = 'off';
% %% run simulation
% sim(mpcNivel_VD, 3001, mpc1_RefSignal, mpc1_MDSignal, options);
