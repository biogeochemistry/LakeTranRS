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
dz = 0.1; 

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


% m_start = [2001, 1, 1];
% m_stop = [2100, 12, 31];
% Wt0 = [Wt; Wt; Wt; Wt; Wt; ...
%        Wt; Wt; Wt; Wt; Wt; ...
%        Wt; Wt; Wt; Wt; Wt; ...
%        Wt; Wt; Wt; Wt; Wt; ...
%        Wt; Wt; Wt; Wt; Wt];
% Wt = Wt0(1:(end-1), :);
% Inflw0 = [Inflw; Inflw; Inflw; Inflw; Inflw; ...
%        Inflw; Inflw; Inflw; Inflw; Inflw; ...
%        Inflw; Inflw; Inflw; Inflw; Inflw; ...
%        Inflw; Inflw; Inflw; Inflw; Inflw; ...
%        Inflw; Inflw; Inflw; Inflw; Inflw];
% Inflw = Inflw0(1:(end-1), :);
% tt = datenum(m_start):datenum(m_stop);

m_start = [2010, 1, 1];
m_stop = [2013, 12, 31];
tt = datenum(m_start):datenum(m_stop);


for century = 0:3
    %% repeat 20th century but starting with the last run of 20th century    
    if century == 0
    [zz,Az,Vz,tt,Qst,Kzt,Tzt,Czt,Szt,Pzt,Chlzt,PPzt,DOPzt,DOCzt,DICzt,...
     CO2zt,O2zt,NO3zt,NH4zt,SO4zt,HSzt,H2Szt,Fe2zt,Ca2zt,pHzt,CH4zt,...
     Fe3zt,Al3zt,SiO4zt,SiO2zt,diatomzt,O2_sat_relt,O2_sat_abst,BODzt,...
     Qzt_sed,lambdazt,P3zt_sed,P3zt_sed_sc,His,DoF,DoM,MixStat,Wt,...
     surfaceflux,O2fluxt,CO2_eqt,K0t,O2_eqt,K0_O2t,...
     CO2_ppmt,dO2Chlt,dO2BODt,testi1t,testi2t,testi3t,...
     MyLake_results_basin1, sdb] = ...
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
                      Deposition, 1, [0; 0]);
    else
    [zz,Az,Vz,tt,Qst,Kzt,Tzt,Czt,Szt,Pzt,Chlzt,PPzt,DOPzt,DOCzt,DICzt,...
     CO2zt,O2zt,NO3zt,NH4zt,SO4zt,HSzt,H2Szt,Fe2zt,Ca2zt,pHzt,CH4zt,...
     Fe3zt,Al3zt,SiO4zt,SiO2zt,diatomzt,O2_sat_relt,O2_sat_abst,BODzt,...
     Qzt_sed,lambdazt,P3zt_sed,P3zt_sed_sc,His,DoF,DoM,MixStat,Wt,...
     surfaceflux,O2fluxt,CO2_eqt,K0t,O2_eqt,K0_O2t,...
     CO2_ppmt,dO2Chlt,dO2BODt,testi1t,testi2t,testi3t,...
     MyLake_results_basin1, sdb] = ...
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
                      Deposition, 0, sediment_concs);
    end
    
    century = num2str(century)
    csvwrite(['results2/', century, 'zz.csv'], zz)
    csvwrite(['results2/', century, 'Az.csv'], Az)
    csvwrite(['results2/', century, 'Vz.csv'], Vz)
    csvwrite(['results2/', century, 't.csv'], Tzt')
    csvwrite(['results2/', century, 'chl.csv'], Chlzt')  
    csvwrite(['results2/', century, 'O2abs.csv'], O2_sat_abst')
    csvwrite(['results2/', century, 'totp.csv'], (Czt + Pzt + Chlzt + PPzt + DOPzt)')
    csvwrite(['results2/', century, 'oldTPdsed.csv'], P3zt_sed(:,:,1)')
    csvwrite(['results2/', century, 'oldTPssed.csv'], P3zt_sed(:,:,2)')
    csvwrite(['results2/', century, 'oldChldsed.csv'], P3zt_sed(:,:,3)')
    csvwrite(['results2/', century, 'oldFIM.csv'], P3zt_sed(:,:,4)')
    csvwrite(['results2/', century, 'sedPO4.csv'], sdb{16, 1}')
    csvwrite(['results2/', century, 'sedPO4adsa.csv'], sdb{17, 1}')
    csvwrite(['results2/', century, 'sedO2.csv'], sdb{1, 1}')
    csvwrite(['results2/', century, 'sedOM.csv'], sdb{9, 1}')
    csvwrite(['results2/', century, 'sedOMb.csv'], sdb{10, 1}')
    csvwrite(['results2/', century, 'sedOMS.csv'], sdb{11, 1}')
    csvwrite(['results2/', century, 'sedNO3.csv'], sdb{19, 1}')
    csvwrite(['results2/', century, 'sedNH4.csv'], sdb{20, 1}')

    %% prepare for the next century
    %% 2016-12-01 Koji
    In_Z = [zz; zz(end)+dz]; %% should fix issues with trimming the end
    %% actually this line falty %% In_Az = Az;  %% volume should be okay without changing but
                 %% double check
    In_Tz = Tzt(:, end);
    In_Cz = Czt(:, end);
    In_Sz = Szt(:, end);
    TPzt = Czt + Pzt + Chlzt + PPzt + DOPzt;
    In_TPz = TPzt(:, end);
    In_DOPz = DOPzt(:, end);
    In_Chlz = Chlzt(:, end);
    In_DOCz = DOCzt(:, end);
    In_DICz = DICzt(:, end);
    In_O2z = O2zt(:, end);
    In_NO3z = NO3zt(:, end);
    In_NH4z = NH4zt(:, end);
    In_SO4z = SO4zt(:, end);
    In_HSz = HSzt(:, end);
    In_H2Sz = H2Szt(:, end);
    In_Fe2z = Fe2zt(:, end);
    In_Ca2z = Ca2zt(:, end);
    In_pHz = pHzt(:, end);
    In_CH4z = CH4zt(:, end);
    In_Fe3z = Fe3zt(:, end);
    In_Al3z = Al3zt(:, end);
    In_SiO4z = SiO4zt(:, end);
    In_SiO2z = SiO2zt(:, end);
    In_diatomz = diatomzt(:, end);
    In_TPz_sed = P3zt_sed(:,end,1) + P3zt_sed(:,end,2);
    In_Chlz_sed = P3zt_sed(:,end,3);
    In_FIM = P3zt_sed(:,end,4);
 
    
% 1  % sediment_results = {O2_sediment_zt,     'Oxygen (aq)';
% 2  %     FeOH3_sediment_zt,   'Iron hydroxide pool 1 Fe(OH)3 (s)';
% 3  %     FeOOH_sediment_zt,   'Iron Hydroxide pool 2 FeOOH (s)';
% 4  %     SO4_sediment_zt,     'Sulfate SO4(2-) (aq)';
% 5  %     Fe2_sediment_zt,     'Iron Fe(2+) (aq)';
% 6  %     H2S_sediment_zt,     'Sulfide H2S (aq)';
% 7  %     HS_sediment_zt,      'Sulfide HS(-) (aq)';
% 8  %     FeS_sediment_zt,     'Iron Sulfide FeS (s)';
% 9  %     OM_sediment_zt,      'Organic Matter pool 1 OMa (s)';
% 10 %     OMb_sediment_zt,     'Organic Matter pool 2 OMb (s)';
% 11 %     OMS_sediment_zt,     'Sulfured Organic Matter (s)';
% 12 %     AlOH3_sediment_zt,   'Aluminum oxide Al(OH)3 (s)';
% 13 %     S0_sediment_zt,      'Elemental sulfur S(0) (aq)';
% 14 %     S8_sediment_zt,      'Rhombic sulfur S8 (s)';
% 15 %     FeS2_sediment_zt,    'Pyrite FeS2 (s)';
% 16 %     PO4_sediment_zt,     'Phosphate PO4(3-) (aq)';
% 17 %     PO4adsa_sediment_zt, 'Solid phosphorus pool a PO4adsa (s)';
% 18 %     PO4adsb_sediment_zt, 'Solid phosphorus pool b PO4adsb (s)';
% 19 %     NO3_sediment_zt,     'Nitrate NO3(-) (aq)';
% 20 %     NH4_sediment_zt,     'Ammonium NH4(+) (aq)';
% 21 %     H_sediment_zt,       'H+ concentration';
% 22 %     Ca2_sediment_zt,     'Calcium Ca(2+) (aq)';
% 23 %     Ca3PO42_sediment_zt, 'Apatite Ca3PO42 (s)';
% 24 %     H_sediment_zt,       'H(+)(aq)';
% 25 %     OH_sediment_zt,      'OH(-)(aq)';
% 26 %     CO2_sediment_zt,     'CO2(aq)';
% 27 %     CO3_sediment_zt,     'CO3(2-)(aq)';
% 28 %     HCO3_sediment_zt,    'HCO3(-)(aq)';
% 29 %     NH3_sediment_zt,     'NH3(aq)';
% 30 %     H2CO3_sediment_zt,   'H2CO3(aq)';
% 31 %     pH_sediment_zt,      'pH in sediment';
% 32 %     deltaO2,             'dO2';
% 33 %     deltaPz,             'dPz';
% 34 %     w_chl,               'Chl settling velocity m day-1';
% 35 %     Mass_Ratio_C_Chl,    'Mass ratio C:Chl';
% 36 %     z_sediment,         'z';
% 37 %     R_values_sediment_zt,'R values';
% 38 %     Bioirrigation_sediment_zt, 'Fluxes of bioirrigation';
% 39 %     MyLake_params,       'MyLake Params important for sediment';
% 40 %     sediment_params,     'Sediments params';
% 41 %     SWI_fluxes_sediment_zt, 'SWI fluxes from WC to sediments';
% 42 %      sediment_integrated_over_depth_fluxes_t, 'Flux integrated over depth';
% 43 %     };    
    sediment_concs = { ...
        sdb{1, 1}(:, end),  'Oxygen';   
        sdb{9, 1}(:, end),  'OM1';      
        sdb{10, 1}(:, end), 'OM2';      
        sdb{19, 1}(:, end), 'NO3';      
        sdb{2, 1}(:, end),  'FeOH3';    
        sdb{4, 1}(:, end),  'SO4';      
        sdb{20, 1}(:, end), 'NH4';      
        sdb{5, 1}(:, end),  'Fe2';      
        sdb{3, 1}(:, end),  'FeOOH';    
        sdb{6, 1}(:, end),  'H2S';      
        sdb{7, 1}(:, end),  'HS';       
        sdb{8, 1}(:, end),  'FeS';      
        sdb{13, 1}(:, end), 'S0';       
        sdb{16, 1}(:, end), 'PO4';      
        sdb{14, 1}(:, end), 'S8';       
        sdb{15, 1}(:, end), 'FeS2';     
        sdb{12, 1}(:, end), 'AlOH3';    
        sdb{17, 1}(:, end), 'PO4adsa';  
        sdb{18, 1}(:, end), 'PO4adsb';  
        sdb{22, 1}(:, end), 'Ca2';      
        sdb{23, 1}(:, end), 'Ca3PO42';  
        sdb{11, 1}(:, end), 'OMS';      
        sdb{24, 1}(:, end), 'H';        
        sdb{25, 1}(:, end), 'OH';       
        sdb{26, 1}(:, end), 'CO2';      
        sdb{27, 1}(:, end), 'CO3';      
        sdb{28, 1}(:, end), 'HCO3';     
        sdb{29, 1}(:, end), 'NH3';      
        sdb{30, 1}(:, end), 'H2CO3'   
    };
    sediment_concs = containers.Map({sediment_concs{:,2}},{sediment_concs{:,1}});
    
end






