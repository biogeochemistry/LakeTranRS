addpath('../../MyLake/v12/v12_1')
addpath('../../MATSEDLAB-IsM')
addpath('.')

% MyLake_parameters % prepares parameter files
m_start=[2010, 1, 1]; 
m_stop=[2013, 12, 31];

run_INCA = 0; % 1- MyLake will run INCA, 0- No run

dummyparfile = '../input/LAE_para_all.txt';
dummyinitfile = '../input/LAE_init_basin3.txt';

listing = dir('intermediate/id');

dt = 1.0;

makeDeposition % creates Deposition -- actually not used

global sed_par_file
sed_par_file = 'params.txt';

[In_Z,In_Az,tt,In_Tz,In_Cz,In_Sz,In_TPz,In_DOPz,In_Chlz,In_DICz,...
 In_DOCz,In_TPz_sed,In_Chlz_sed,In_O2z,In_NO3z,In_NH4z,In_SO4z,...
 In_HSz,In_H2Sz,In_Fe2z,In_Ca2z,In_pHz,In_CH4z,In_Fe3z,In_Al3z,...
 In_SiO4z,In_SiO2z,In_diatomz,In_FIM,Ice0,Wt,Inflw,...
 Phys_par,Phys_par_range,Phys_par_names,...
 Bio_par,Bio_par_range,Bio_par_names] = ...
    modelinputs_v2(m_start,m_stop, dummyinitfile, 'duh', ...
                   '../input/LAE_input.txt', 'duh', ...
                   dummyparfile, 'duh', dt);
Bio_par(38) = 1.7;
Bio_par(39) = 0.0001;
Bio_par(40) = 4.4897;
        
%% will fake the four-year inputs (weather and inflow) to a century
%% long input

% original 2010-01-01 to 2013-12-31, 1461 days including ends
% 21st century 2001-01-01 to 2100-12-31, 36524 days
% this is 25 times original MINUS 1 day

m_start = [2001, 1, 1];
m_stop = [2100, 12, 31];
Wt0 = [Wt; Wt; Wt; Wt; Wt; ...
       Wt; Wt; Wt; Wt; Wt; ...
       Wt; Wt; Wt; Wt; Wt; ...
       Wt; Wt; Wt; Wt; Wt; ...
       Wt; Wt; Wt; Wt; Wt];
Wt = Wt0(1:(end-1), :);
Inflw0 = [Inflw; Inflw; Inflw; Inflw; Inflw; ...
       Inflw; Inflw; Inflw; Inflw; Inflw; ...
       Inflw; Inflw; Inflw; Inflw; Inflw; ...
       Inflw; Inflw; Inflw; Inflw; Inflw; ...
       Inflw; Inflw; Inflw; Inflw; Inflw];
Inflw = Inflw0(1:(end-1), :);
tt = datenum(m_start):datenum(m_stop);


for century = 0:9
    %% repeat 20th century but starting with the last run of 20th century    
    [zz,Az,Vz,tt,Qst,Kzt,Tzt,Czt,Szt,Pzt,Chlzt,PPzt,DOPzt,DOCzt,DICzt,...
     CO2zt,O2zt,NO3zt,NH4zt,SO4zt,HSzt,H2Szt,Fe2zt,Ca2zt,pHzt,CH4zt,...
     Fe3zt,Al3zt,SiO4zt,SiO2zt,diatomzt,O2_sat_relt,O2_sat_abst,BODzt,...
     Qzt_sed,lambdazt,P3zt_sed,P3zt_sed_sc,His,DoF,DoM,MixStat,Wt,...
     surfaceflux,O2fluxt,CO2_eqt,K0t,O2_eqt,K0_O2t,...
     CO2_ppmt,dO2Chlt,dO2BODt,testi1t,testi2t,testi3t,...
     MyLake_results_basin1, sediment_data_basin1] = ...
        solvemodel_v2(m_start,m_stop,dummyinitfile, 'duh', ...
                       '../input/LAE_input.txt', 'duh', ...
                      dummyparfile, 'duh', ...
                      In_Z,In_Az,tt,In_Tz,In_Cz,In_Sz,In_TPz,In_DOPz,...
                      In_Chlz,In_DOCz,In_DICz,In_O2z,In_NO3z,In_NH4z,...
                      In_SO4z,In_HSz,In_H2Sz,In_Fe2z,In_Ca2z,In_pHz,...
                      In_CH4z,In_Fe3z,In_Al3z,In_SiO4z,In_SiO2z,...
                      In_diatomz,In_TPz_sed,In_Chlz_sed,In_FIM, ...
                      Ice0,Wt,Inflw,...
                      Phys_par,Phys_par_range,Phys_par_names,...
                      Bio_par,Bio_par_range,Bio_par_names, ...
                      Deposition);
    
    csvwrite(['results', '/', century, 't.csv'], Tzt')
    csvwrite(['results', '/', century, 'chl.csv'], Chlzt')  
    csvwrite(['results', '/', century, 'O2abs.csv'], O2_sat_abst')
    csvwrite(['results', '/', century, 'totp.csv'], (Czt + Pzt + Chlzt + PPzt + DOPzt)')

    %% prepare for the next century
    In_Tz = Tzt(:, end)
    In_Cz = Czt(:, end)
    In_Sz = Szt(:, end)
    In_TPz = TPzt(:, end)
    In_DOPz = DOPzt(:, end)
    In_Chlz = Chlzt(:, end)
    In_DOCz = DOCzt(:, end)
    In_DICz = DICzt(:, end)
    In_O2z = O2zt(:, end)
    In_NO3z = NO3zt(:, end)
    In_NH4z = NH4zt(:, end)
    In_SO4z = SO4zt(:, end)
    In_HSz = HSzt(:, end)
    In_H2Sz = H2Szt(:, end)
    In_Fez = Fezt(:, end)
    In_Ca2z = Ca2zt(:, end)
    In_pHz = pHzt(:, end)
    In_CH4z = CH4zt(:, end)
    In_Fe3z = Fe3zt(:, end)
    In_Al3z = Al3zt(:, end)
    In_SiO4z = SiO4zt(:, end)
    In_SiO2z = SiO2zt(:, end)
    In_diatomz = diatomzt(:, end)
    In_TPz_sed = ???
    In_Chlz_sed = ???
    In_FIM = ???
    
    
end






