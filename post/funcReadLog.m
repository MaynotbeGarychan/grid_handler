function [numericData, stringData] = funcReadLog(log_dir)
% Define the format of your data
formatSpec = '%f %f %f %f %f %s';

% Open the file for reading
fileID = fopen(log_dir, 'r');

% Read the data from the file
data = textscan(fileID, formatSpec, 'Delimiter', ' ', 'CollectOutput', true);

% Close the file
fclose(fileID);

% Extract the numeric and string data
numericData = data{1};
stringData = data{2};

end