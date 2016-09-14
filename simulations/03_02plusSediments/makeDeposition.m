filename = 'Deposition.txt';
delimiter = '\t';
startRow = 3;
formatSpec = '%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%f%[^\n\r]';
fileID = fopen(filename,'r');
Deposition_all_dates = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'EmptyValue' ,NaN,'HeaderLines' ,startRow-1, 'ReturnOnError', false);
fclose(fileID);
deposition_dates=datenum([Deposition_all_dates{:,1} Deposition_all_dates{:,2} Deposition_all_dates{:,3}]);
Deposition_all_dates(1:3)=[];
Deposition_all_dates(23)=[];
cd ..
clearvars filename delimiter startRow formatSpec fileID  ans;
% matching dates from deposition files with m_start and m_stop

MyL_dates = linspace(datenum(m_start),datenum(m_stop),(datenum(m_stop)-datenum(m_start)+1))';

[v,loc_dep_dates,loc_MyL_dates] = intersect(deposition_dates, MyL_dates); % returns the matched datum, and the index for obs and sim vector
for i = 1:length(Deposition_all_dates)
Deposition(:,i)= (Deposition_all_dates{i}(loc_dep_dates,:));
end