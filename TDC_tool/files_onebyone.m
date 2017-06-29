clear all;

folder_name = [uigetdir('../') '/'];
fs = dir(folder_name);

% [filename, path, filterindex] = uigetfile('*.*');
% fn = strcat(path,filename)
% time_interval = str2num(filename(1:length(filename)-3));
[pathstr,name,ext] = fileparts(filename);
time_x = str2num(name);


tdc_2;

std_vs_time(end+1,:)=[time_x, mean_ave(20, 2), std_ave(20, 2)];
fclose all;
  