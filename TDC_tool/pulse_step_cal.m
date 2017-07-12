% clear all;
clear std_vs_time;
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
%     hist(std_hist);
%     print('-painters', '-dpng', '-r1200', strcat(fn(1:end-3), 'png'))
%     csvwrite(strcat(fn, '_measure.csv'), std_hist);
    
    std_vs_time(end+1,:)=[mean_ave(20, 2), std_ave(20, 2)];
end
std_vs_time=sortrows(std_vs_time(2:end,:), 1);

if ~ exist('pulse_steps', 'var')
    pulse_steps = std_vs_time(end/2:-1:1, 1);
else
    pulse_steps=[pulse_steps std_vs_time(end/2:-1:1, 1)];
end
pulse_steps=[pulse_steps std_vs_time(end/2+1:end, 1)];

abs_steps = diff(pulse_steps);

mean_steps = mean(abs_steps(1:end,:));

% result=abs_steps./(mean_steps'*ones(1,nr))';

if ~ exist('DNL', 'var')
    DNL = (abs_steps(:, 1)-mean_steps(1, 1))/mean_steps(1, 1);
%     DNL = abs_steps/mean_steps;
%     DNL = abs_steps./(mean_steps'*ones(1,nr))';
%     INL = cumsum(DNL);
else
    DNL = [DNL (abs_steps(:, 1)-mean_steps(1, 1))/mean_steps(1, 1)];
%     DNL = [DNL abs_steps./(mean_steps'*ones(1,nr))'];
%     INL = [INL cumsum(DNL)];
end

for i=size(mean_steps'):size(mean_steps')
    DNL = [DNL (abs_steps(:, i)-mean_steps(1, i))/mean_steps(1, i)];
end
INL = cumsum(DNL);

dlmwrite([folder_name 'pulse_steps.csv'], pulse_steps, 'precision', '%0.8f'); 
dlmwrite([folder_name 'pulse_DNL.csv'], DNL, 'precision', '%0.8f');
dlmwrite([folder_name 'pulse_INL.csv'], INL, 'precision', '%0.8f');
% csvwrite(strcat(folder_name, 'pulse_steps.csv'), pulse_steps);
% csvwrite(strcat(folder_name, 'pulse_DNL.csv'), DNL);
% csvwrite(strcat(folder_name, 'pulse_INL.csv'), INL);
% clear std_vs_time;