addpath('../../MyLake/v12/v12_1')
addpath('../../MATSEDLAB-IsM')
addpath('.')

%% short input for testing
m_start0 = [2010, 1, 1];
m_stop0 = [2013, 12, 31];
m_start1 = [2010, 1, 1];
m_stop1 = [2017, 12, 31];


run_INCA = 0; % 1- MyLake will run INCA, 0- No run

dummyparfile = '../input/LAE_para_dz05.txt';
dummyinitfile = '../input/LAE_init_basin3.txt';

listing = dir('intermediate/id/0*');

dt = 1.0;

m_start = m_start0;
m_stop = m_stop0;
makeDeposition % creates Deposition -- actually not used

global sed_par_file
sed_par_file = 'params.txt';


% for r = 1:length(listing)
for r = template

    % skip folders or files starting with a dot '.'
    if listing(r).name(1) == '.'
        disp(['skipping ', listing(r).name])
    
    else
        disp([listing(r).name])
        p1 = ['intermediate/id/', listing(r).name];
        p2 = ['simulations/idtest/', listing(r).name]; % this folder made earlier



        m_start = m_start0;
        m_stop = m_stop0;

        [In_Z,In_Az,tt,In_Tz,In_Cz,In_Sz,In_TPz,In_DOPz,In_Chlz,In_DICz,...
         In_DOCz,In_TPz_sed,In_Chlz_sed,In_O2z,In_NO3z,In_NH4z,In_SO4z,...
         In_HSz,In_H2Sz,In_Fe2z,In_Ca2z,In_pHz,In_CH4z,In_Fe3z,In_Al3z,...
         In_SiO4z,In_SiO2z,In_diatomz,In_FIM,Ice0,Wt,Inflw,...
         Phys_par,Phys_par_range,Phys_par_names,...
         Bio_par,Bio_par_range,Bio_par_names] = ...
            modelinputs_v2(m_start,m_stop, dummyinitfile, 'duh', ...
                           [p1, '/input.txt'], 'duh', ...
                           dummyparfile, 'duh', dt);
        Bio_par(38) = 1.7;
        Bio_par(39) = 0.0001;
        Bio_par(40) = 4.4897;
        
        
        
        
        
        %% will fake the four-year inputs (weather and inflow) to a century
        %% long input
        
        % original 2010-01-01 to 2013-12-31, 1461 days including ends
        % 21st century 2001-01-01 to 2100-12-31, 36524 days
        % this is 25 times original MINUS 1 day
        
        Wt = [Wt; Wt; Wt];
        Inflw = [Inflw; Inflw; Inflw];
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
        m_start = m_start1;
        m_stop = m_stop1;
        tt = datenum(m_start):datenum(m_stop);
   
        
        
        
        
        try 
            
            [zz,Az,Vz,tt,Qst,Kzt,Tzt,Czt,Szt,Pzt,Chlzt,PPzt,DOPzt,DOCzt,DICzt,...
             CO2zt,O2zt,NO3zt,NH4zt,SO4zt,HSzt,H2Szt,Fe2zt,Ca2zt,pHzt,CH4zt,...
             Fe3zt,Al3zt,SiO4zt,SiO2zt,diatomzt,O2_sat_relt,O2_sat_abst,BODzt,...
             Qzt_sed,lambdazt,P3zt_sed,P3zt_sed_sc,His,DoF,DoM,MixStat,Wt,...
             surfaceflux,O2fluxt,CO2_eqt,K0t,O2_eqt,K0_O2t,...
             CO2_ppmt,dO2Chlt,dO2BODt,testi1t,testi2t,testi3t,...
             MyLake_results_basin1, sediment_data_basin1] = ...
                solvemodel_v2(m_start,m_stop,dummyinitfile, 'duh', ...
                              [p1, '/input.txt'], 'duh', ...
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
            
            csvwrite([p2, '/t.csv'], Tzt')
            csvwrite([p2, '/lambda.csv'], lambdazt')
            csvwrite([p2, '/His.csv'], His')
            csvwrite([p2, '/chl.csv'], Chlzt')  
            csvwrite([p2, '/O2abs.csv'], O2_sat_abst')
            % csvwrite([p2, '/O2rel.csv'], O2_sat_relt')
            csvwrite([p2, '/totp.csv'], (Czt + Pzt + Chlzt + PPzt + ...
                                                DOPzt)')
            csvwrite([p2, '/Qst.csv'], Qst')  
            
            % csvwrite([p2, '/sedO2.csv'], sediment_data_basin1{1, 1}')
            % csvwrite([p2, '/sedOM.csv'], sediment_data_basin1{9, 1}')
            % csvwrite([p2, '/sedOMb.csv'], sediment_data_basin1{10, 1}')
            % csvwrite([p2, '/sedOMS.csv'], sediment_data_basin1{11, 1}')
            % csvwrite([p2, '/sedpH.csv'], sediment_data_basin1{31, 1}')
            
            % sf = sediment_data_basin1{41, 1};
            % sf10 = [sf{1, 1} ; 
            %         sf{2, 1} ;
            %         sf{3, 1} ;
            %         sf{4, 1} ;
            %         sf{5, 1} ;
            %         sf{6, 1} ;
            %         sf{7, 1} ;
            %         sf{8, 1} ;
            %         sf{9, 1} ;
            %         sf{10, 1}]; 
            % csvwrite([p2, '/sedfluxes.csv'], sf10')
            
            
        catch me
            disp('model crashing; skipping')
            
        end
        
    end
    
end