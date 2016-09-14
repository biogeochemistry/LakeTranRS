%% Response surfaces input generator
clear all
tic

m_start=[1983, 1, 4]; % 1973 1 1 is the earliest possible given the provided input files8
m_stop=[2014, 5, 31]; % 2012, 12, 31 is the latest possible given the provided input files

num_days_2nd_half =(datenum(m_stop)-datenum(m_start))/2 ; % for the 2nd half of the run where we reduce TP inputs
days_frac_2nd_half = 100/(num_days_2nd_half);

%% config
total_runs = 0; %just initializing parameters
T_Air_loop = 0;
TP_loop = 0;
TP_red_loop = 0;
grid_size = 100.0 / (5 - 1); % give in percent (5.2 works with 8000 runs)
% grid_size = 5.2; % give in percent (5.2 works with 8000 runs)
scaling_TP_red_vec = [1:num_days_2nd_half];
scaling_TP_red_mat = zeros((datenum(m_stop)-datenum(m_start)+1),8000);

%% air temperature T_Air
min_T_Air = -5;
max_T_Air = 10;

step_T_Air = (max_T_Air - min_T_Air) / (100/grid_size);

%% TP load
% this one is a log scale
min_TP = 0; % 0.01
max_TP = 3.3; % 
step_TP = (max_TP - min_TP) / (100/grid_size); % thus in log units

%% TP reduction
% this one is a log scale
max_TP_red = 10^max_TP/num_days_2nd_half/100; % this is the reduction per day needed max
step_TP_red = 2 * max_TP_red /(100/grid_size); % we will either increase or decrease

open_template_input_file_RS_sediment % matlab generated script to open baseline time series and put them in memory


%% generating input array
for scaling_T_Air = min_T_Air:step_T_Air:max_T_Air
    T_Air_loop = T_Air_loop + 1;
    
    %correction
    storeINCAPinputbaseline_mat(:,6) = storeINCAPinputbaseline_mat(:,6) + scaling_T_Air;
    
    for new_TP_conc = min_TP:step_TP:max_TP
        TP_loop = TP_loop + 1;
        
        storeINCAPinputbaseline_mat(:,15) = 10^new_TP_conc;
        
       for scaling_TP_red = -max_TP_red:step_TP_red:max_TP_red % loop for the reduction or increase of TP in the 2nd half of the sim
            
            TP_red_loop = TP_red_loop + 1;
            
            % computing scaling vector for TP time-series in the 2nd half of the run
            scaling_TP_red_vec(1) = 10^new_TP_conc; % setting the initial TP from the outer loop
            for i = 2:length(scaling_TP_red_vec) % creating the rolling reduction vector ... sure it can be vectorized
                scaling_TP_red_vec(i) = scaling_TP_red_vec(i-1)-(scaling_TP_red_vec(1)*scaling_TP_red/100) ; % from the initial TP, creating the temporal trends
            end
            
            storeINCAPinputbaseline_mat(end-length(scaling_TP_red_vec)+1:end,15) = scaling_TP_red_vec;
            
            total_runs = total_runs + 1; % run counter
            scaling_TP_red_mat(:,total_runs)=storeINCAPinputbaseline_mat(:,15); % stores the TP reduction for post-processing
          
          
            %% creating full input array
            
            all_input_files{total_runs} = storeINCAPinputbaseline_mat;
            
            new_filename = strcat('Koji-5x5x5/input/input_',num2str(T_Air_loop),'_',num2str(TP_loop),'_',num2str(TP_red_loop),'.txt');
            list_input_file{total_runs,1} = new_filename;
            
        end
        TP_red_loop = 0;
    end
    TP_loop = 0;
end

%% sending to write out
MyLAke_response_surface_input_write_5x5x5

clearvars -except list_input_file K_values* m_* scaling_TP_red_mat min_T_Air max_T_Air min_TP max_TP
toc