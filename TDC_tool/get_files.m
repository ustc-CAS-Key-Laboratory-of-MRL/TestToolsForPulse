
[filename, path, filterindex] = uigetfile('*.*');
fn = strcat(path,filename)
fname = fn;
% if isdir(fn)
%     flist=dir(fn);
% end
folder_name = uigetdir(start_path);
flist=dir(folder_name);
fname = {};
for i = 1:length(flist)
    fname(i) = cellstr(flist(i).name);
end;