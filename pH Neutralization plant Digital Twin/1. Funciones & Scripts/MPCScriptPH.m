%% create MPC controller object with sample time
mpcpH_VD = mpc(Modelo_PH_C, Tim_MPC);
%% specify prediction horizon
mpcpH_VD.PredictionHorizon = 60;
%% specify control horizon
mpcpH_VD.ControlHorizon = 10;
%% specify nominal values for inputs and outputs
mpcpH_VD.Model.Nominal.U = 7;
mpcpH_VD.Model.Nominal.Y = 7;
%% specify constraints for MV and MV Rate
mpcpH_VD.MV(1).Min = 0;
mpcpH_VD.MV(1).Max = 14;
mpcpH_VD.MV(1).RateMin = -5;
mpcpH_VD.MV(1).RateMax = 5;
%% specify constraints for OV
mpcpH_VD.OV(1).Min = 0;
mpcpH_VD.OV(1).Max = 14;
%% specify weights
mpcpH_VD.Weights.MV = 0;
mpcpH_VD.Weights.MVRate = 0.4;  % Segun los trabajos de Manuel
mpcpH_VD.Weights.OV = 0.6;      % Segun los trabajos de Manuel
mpcpH_VD.Weights.ECR = 100000;
%% specify simulation options
% options = mpcsimopt();
% options.Model = Modelo_PH_S_1;
% options.RefLookAhead = 'off';
% options.MDLookAhead = 'off';
% options.Constraints = 'on';
% options.OpenLoop = 'off';
% %% run simulation
% sim(mpc1, 3001, mpc1_RefSignal_2, mpc1_MDSignal_2, options);
