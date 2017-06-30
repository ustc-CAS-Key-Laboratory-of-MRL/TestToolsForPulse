files = dir;
fname = {};
for i = 1:length(files)
    fname(i) = cellstr(files(i).name);
end;

% y1 = xlsread('code_density_path1_v1.xlsx');
% y2 = xlsread('code_density_path2_v1.xlsx');
y1 = csvread('TDC_PATH1_CRS_V1.csv');
y2 = csvread('TDC_PATH2_CRS_V2.csv');

% fid = fopen('1000000000.txt');
for file_index = 3:length(fname)
    
    fff = char(fname(file_index))
    if ~ strcmp(fff(length(fff)-2:length(fff)), 'txt')
        continue
    end
    fid = fopen(fff);
    test = fscanf(fid, '%s\n'); 
    pnum = length(test)/16;
    tt = fi(0,0,32,0);
    ff = fi(0,0,32,0);
    hh = fi(0,0,32,0);
    gg = fi(0,0,32,0);
    x = zeros(pnum,7);
    z = zeros(1,pnum);
    


    for i = 1:pnum
    tt.hex = test((16*i-5):(16*i-3));
    x(i,1)=tt.data;
    ff.hex = test((16*i-2):16*i);
    x(i,2)=ff.data;
    hh.hex = test((16*i-15):(16*i-8));
    x(i,3)=hh.data;
    gg.hex = test((16*i-7):(16*i-6));
    x(i,7)=gg.data;
    for n = 1:370
        if x(i,1) == y1(n,1)
           x(i,4)=y1(n,3);
        end 
        if x(i,2) == y2(n,1)
           x(i,5)=y2(n,3);
        end; 
    end;
    % if x(i,3)==1 & x(i,4) > x(i,5)
    %     x(i,6)=x(i,4)-(x(i,5)+x(i,3)*8000);
    % else x(i,6)=x(i,4)+x(i,3)*8000-x(i,5);
    % end
    if x(i,7) == 0
        x(i,6)=x(i,4)+x(i,3)*8000-x(i,5);
    else
        x(i,6)=x(i,4)-(x(i,3)*8000+x(i,5));
    end 
    z(1,i) = x(i,6)/1000; 
    % if z(1,i) > 8;
    %     a = i
    % end;
    end
    z2 = mean(z);
    z(1,:) = z(1,:)- z2;
    z1 = std(z)*1000

    ma=max(z);
    mi=min(z);
    binsize=0.02
    y=mi-0.01:binsize:ma+0.01;
    fclose('all');
    jitter(file_index-2, 1) = str2num(fff(1:length(fff)-3));
    jitter(file_index-2, 2) = z1;
    jitter(file_index-2, 3) = z2;
%     hist(z,y);
%     print('-painters', '-dpng', '-r1200', strcat('Z',fff(1:length(fff)-3), 'png'))
%     close all;
    
end
jitter=sortrows(jitter,1)