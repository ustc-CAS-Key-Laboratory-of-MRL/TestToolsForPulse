clear all;
load_cab_data;

folder_name = [uigetdir('../data/') '/'];
fs = dir(folder_name);

fnames = {};
for i = 1:length(fs)
    if length(fs(i).name) > 3 && strcmp(fs(i).name(end-2:end), 'dat')
        fnames(end+1) = cellstr([folder_name fs(i).name]);
    end
end;
if ~ exist('std_vs_time', 'var')
    std_vs_time = [0., 0.]
end

pnum = 10000;

% filename = [folder_name '0.txt']
% tdc_2;
for filename=fnames
%     filename = [folder_name num2str(j*10^i)]
    fn=char(filename)
    [pathstr,name,ext] = fileparts(char(filename));
%     time_interval = str2num(name);
    
    tdc_2;
    hist(std_hist);
%     print('-painters', '-dpng', '-r1200', strcat(fn(1:end-3), 'png'))
    csvwrite(strcat(fn, '_measure.csv'), std_hist);
    
    std_vs_time(end+1,:)=[mean_ave(20, 2), std_ave(20, 2)];
end
std_vs_time=sortrows(std_vs_time(2:end,:), 1);
csvwrite(strcat(folder_name, 'std_vs_time.csv'), std_vs_time);
% clear std_vs_time;