clear all;
load_cab_data;

folder_name = [uigetdir('../data/') '/'];
% fs = dir(folder_name);
if ~ exist('std_vs_time', 'var')
    std_vs_time = [0., 0., 0.]
end
% [filename, path, filterindex] = uigetfile('*.*');
% fn = strcat(path,filename)
% time_interval = str2num(filename(1:length(filename)-3));
pnum = 10;
obo_loopi=0
fn=[folder_name num2str(obo_loopi) '.dat']
while exist(fn, 'file') ~= 0
    [pathstr,name,ext] = fileparts(fn);
    time_x = str2num(name);
    tdc_2;
    std_vs_time(end+1,:)=[time_x, mean_ave(20, 2), std_ave(20, 2)];
    obo_loopi=obo_loopi+1;
    fn=[folder_name num2str(obo_loopi) '.dat']
end
% csvwrite([folder_name '_a_main.csv'], std_vs_time(2:end,:));
dlmwrite([folder_name '_a_main.csv'], std_vs_time(2:end,:), 'precision', '%0.8f') 
fclose all;
  