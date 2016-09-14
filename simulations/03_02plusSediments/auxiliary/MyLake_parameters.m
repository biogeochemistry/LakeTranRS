% Generating Prior structure. For this application we will have an entry
% into the Prior even for parameters not varied. Put in a switch for that.


K_values_sediment ...
    = {1,  'k_OM1';  % 1
    0.1,  'k_OM2';  % 0.01
    0.0123,'Km_O2';
    0.01,  'Km_NO3';
    3.92,  'Km_Fe(OH)3';
    2415,  'Km_FeOOH';
    0.0293,'Km_SO4';
    0.001, 'Km_oxao';
    0.1,   'Km_amao';
    0.3292,'Kin_O2';
    0.1,   'Kin_NO3';
    0.1,   'Kin_FeOH3';
    0.1,   'Kin_FeOOH';
    2000,  'k_NH4ox';
    8.7e4, 'k_Feox';
    0.1,   'k_Sdis';
    2500,  'k_Spre';
    3.17,  'k_FeS2pre';
    0.1,   'k_alum';
    1.35,  'k_pdesorb_a';
    1.35,  'k_pdesorb_b';
    6500,  'k_rhom';
    0.1,   'k_tS_Fe';
    2510,  'Ks_FeS';
    0.001, 'k_Fe_dis';
    21.3,  'k_Fe_pre';
    0.37,  'k_apa';
    3e-6,  'kapa';
    0.3134,'k_oms';
    1000,  'k_tsox';
    0.001, 'k_FeSpre';
    30,    'accel';

    1e-6,   'f_pfe';
    1.35,   'k_pdesorb_c';

    % Added porosity modeling parameters:
    0.98,   'fi_in';
    0.85,   'fi_f';
    0.5,    'X_b';
    1,      'tortuosity';

    10,      'w';
    64,     'n';
    15,     'depth';
    0.26,   'F';
    14.4,   'alfa0';

    % OM composition
    112,    'Cx1';
    10,     'Ny1';
    1,      'Pz1';
    200,    'Cx2';
    20,     'Ny2';
    1,      'Pz2';

    0.001,  'ts';
    };

calibration_k_values = [(1:50)',cell2mat(K_values_sediment(:,1)) ];
dlmwrite(sed_par_file, calibration_k_values,'delimiter','\t');



K_values_lake =      ...
   {0,      'I_scT'; 	% 
    1,      'I_scDOC'; 	% 
    0.2,    'w_s'; 		% 
    0.2,    'w_chl';    % 
    1,      'Y_cp'      %
    0.2,    'm_twty'    %
    1.5     'g_twty'     %
    2e-4    'k_sed_twty' %
    0       'k_dop_twty' %    
    0.2     'P_half'     %
    0.01,   'oc_DOC'; 	 % 
    0.1,    'qy_DOC'; 	 % 
    0.1,    'k_BOD'; 	 % 
    1.05,   'theta_bod';	 % 
    1.13,   'theta_bod_ice'; 	% 
    4,      'theta_T';     % 
    1,      'I_scO'}; 	% 

