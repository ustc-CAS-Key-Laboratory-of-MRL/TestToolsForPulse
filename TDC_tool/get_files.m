
[filename, path, filterindex] = uigetfile('*.*');
fn = strcat(path,filename)
fname = fn;
% if isdir(fn)
%     flist=dir(fn);
% end

tdc_2;
hist(std_hist);
print('-painters', '-dpng', '-r1200', strcat(fn(1:end-3), 'png'))
csvwrite(strcat(fn, '_measure.csv'), std_hist);

% folder_name = uigetdir(start_path);
% flist=dir(folder_name);
% fname = {};
% for i = 1:length(flist)
%     fname(i) = cellstr(flist(i).name);
% end;