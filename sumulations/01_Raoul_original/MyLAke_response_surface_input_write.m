try
    parpool('local',4)
catch me 
end
 
 for current_run = 1:length(list_input_file)
    
    
    %% uncomment for writing
    current_filename = list_input_file{current_run};
    storeINCAPinputbaseline_mat = all_input_files(current_run);
    
    fileID = fopen(current_filename,'za');
    %fileID = fopen(current_filename,'w');
    formatSpec = '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s \r\n';
    fprintf(fileID,formatSpec,storeINCAPinputbaseline_header{1,:}); % writing header
    fprintf(fileID,formatSpec,storeINCAPinputbaseline_header{2,:}); % writing header
    dlmwrite(current_filename,storeINCAPinputbaseline_mat,'-append','delimiter','\t')
    fclose(fileID);
    
end
