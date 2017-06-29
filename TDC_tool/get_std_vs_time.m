clear all;

folder_name = [uigetdir('../data/') '/'];
fs = dir(folder_name);

fnames = {};
for i = 1:length(fs)
    if length(fs(i).name) > 3
        fnames(end+1) = cellstr([folder_name fs(i).name]);
    end
end;
if ~ exist('std_vs_time', 'var')
    std_vs_time = [0., 0., 0.]
end
% filename = [folder_name '0.txt']
% tdc_2;
for filename=fnames
%     filename = [folder_name num2str(j*10^i)]
    fn=char(filename)
    [pathstr,name,ext] = fileparts(char(filename));
    time_interval = str2num(name);
    tdc_2;
    std_vs_time(end+1,:)=[time_interval, mean_ave(20, 2), std_ave(20, 2)];
end

csvwrite(strcat(fn, 'std_vs_time.csv'), std_vs_time(2:end,:));
clear std_vs_time;