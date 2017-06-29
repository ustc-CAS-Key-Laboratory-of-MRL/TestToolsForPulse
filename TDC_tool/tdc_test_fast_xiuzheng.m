pnum = 100000;
period = 4000;
tnum=47;
snum=20;
bnum=28;
binnum=200;
binnum=200;
x1=zeros(binnum,4,snum);
x2=zeros(binnum,4,snum);
yy1=zeros(binnum,4);
yy2=zeros(binnum,4);
y=zeros(pnum,snum);
z=zeros(pnum,snum);
mean_ave=zeros(snum,2);
std_ave=zeros(snum,2);
temp_array=zeros(pnum,1);
dif_binsize1=zeros(1,20);
dif_binsize2=zeros(1,20);
load('temp_mean_b1.mat');
load('temp_mean_25_b1.mat');
load('temperature_b1.mat');
load('temp_binsize_b1_p1.mat');
load('temp_binsize_b1_p2.mat');

temp_binsize1_ave=zeros(tnum,1);
temp_binsize2_ave=zeros(tnum,1);
for t=1:tnum
    for i=1:snum
        temp_binsize1_ave(t,1)=temp_binsize1_ave(t,1)+temp_binsize1_figure(t,i);
        temp_binsize2_ave(t,1)=temp_binsize2_ave(t,1)+temp_binsize2_figure(t,i);
    end
end
temp_binsize1_ave(:,1)=temp_binsize1_ave(:,1)/snum;
temp_binsize2_ave(:,1)=temp_binsize2_ave(:,1)/snum;

dif_binsize1(1,:)=temp_binsize1_figure(24,:)-temp_binsize1_ave(24,1);
dif_binsize2(1,:)=temp_binsize2_figure(24,:)-temp_binsize2_ave(24,1);
binsize1_correction=0;
binsize2_correction=0;
mean_cor=0;


for t=1:tnum
    
%     if t<=6
%         time_interval=10^t
% %         time_interval=t-1
%     else
%         time_interval=(10^(t-6))*5
% %         time_interval=t-8
%     end
    
    time_interval=2*(t-1)-21
    
%     fname=['tdc_20ch_4ns_crs_b1_bit_data_inc_1s_' num2str(time_interval) '.csv'];
    fname=['tdc_20ch_4ns_crs_b1_bit_data_' num2str(time_interval) '_0.5m.csv'];
    fid = fopen(fname);
    for s=1:snum
        filename1=['tdc_20ch_4ns_crs_b1_bit_25_ch' num2str(s) '_code1.csv'];
        filename2=['tdc_20ch_4ns_crs_b1_bit_25_ch' num2str(s) '_code2.csv'];
        yy1=csvread(filename1);
        yy2=csvread(filename2);
        x1(:,:,s)=yy1;
        x2(:,:,s)=yy2;
    end

    for i=1:pnum
        for s=1:snum
            temp=fread(fid,1,'ubit16','b');
            coase1=fread(fid,1,'ubit32','b');
            coase2=fread(fid,1,'ubit32','b');
            fine1=fread(fid,1,'ubit20','b');
            fine2=fread(fid,1,'ubit12','b');
            fine_data1= x1(fine1,4,s);
            fine_data2= x2(fine2,4,s);
            if temp > 32768
                temp=(temp/128-512)/2;
            else 
                temp=temp/256;
            end
            for m=1:tnum
                if temperature2(m,1)>=temp
                    if m==1
                        binsize1_correction=temp_binsize1_figure(1,s)-(temp_binsize1_figure(2,s)-temp_binsize1_figure(1,s))*(temperature2(1,1)-temp)/(temperature2(2,1)-temperature2(1,1));
                        binsize2_correction=temp_binsize2_figure(1,s)-(temp_binsize2_figure(2,s)-temp_binsize2_figure(1,s))*(temperature2(1,1)-temp)/(temperature2(2,1)-temperature2(1,1));

                    else
                        binsize1_correction=temp_binsize1_figure(m-1,s)+(temp_binsize1_figure(m,s)-temp_binsize1_figure(m-1,s))*(temp-temperature2(m-1,1))/(temperature2(m,1)-temperature2(m-1,1));
                        binsize2_correction=temp_binsize2_figure(m-1,s)+(temp_binsize2_figure(m,s)-temp_binsize2_figure(m-1,s))*(temp-temperature2(m-1,1))/(temperature2(m,1)-temperature2(m-1,1));

                    end
                    break
                else
                    binsize1_correction=temp_binsize1_figure(tnum,s)+(temp_binsize1_figure(tnum,s)-temp_binsize1_figure(tnum-1,s))*(temp-temperature2(tnum,1))/(temperature2(tnum,1)-temperature2(tnum-1,1));
                    binsize2_correction=temp_binsize2_figure(tnum,s)+(temp_binsize2_figure(tnum,s)-temp_binsize2_figure(tnum-1,s))*(temp-temperature2(tnum,1))/(temperature2(tnum,1)-temperature2(tnum-1,1));

                end
            end
            mean_cor=mean_correction(t,s);
            fine_data1=fine_data1*(binsize1_correction)/temp_binsize1_figure(24,s);
            if fine_data1>4000
                fine_data1=4000;
            end
            fine_data2=fine_data2*(binsize2_correction)/temp_binsize2_figure(24,s);
            if fine_data2>4000
                fine_data2=4000;
            end
            time_data=fine_data1+(coase2-coase1)*period-fine_data2;
            time_data=time_data-mean_cor*1000;
            y(i,s)=time_data/1000;
        end
        temp_array(i,1)=temp;

    end


    for i=1:pnum
        for s=1:snum
            if s==1
                z(i,s)=y(i,s);
            else
                z(i,s)=z(i,(s-1))+y(i,s);
            end 
        end 
        for s=1:snum
            z(i,s)=z(i,s)/s;
        end
    end
 

    for s=1:snum
        mean_ave(s,1)=s;
        mean_ave(s,2)=mean(z(:,s));
        mean_ave(s,3)=mean(y(:,s));
        std_ave(s,1)=s;
%         std_ave(s,2)=std(z(:,s))*1000;
        sum=0;
        for i=1:pnum
            sum=sum+(z(i,s)-t25_mean(1,s))^2;
        end
        std_ave(s,2)=1000*sqrt(sum/pnum);
        single_ave(s,1)=s;
%         single_ave(s,2)=std(y(:,s))*1000;
        sum1=0;
        for i=1:pnum
            sum1=sum1+(y(i,s)-t25_mean(2,s))^2;
        end
        single_ave(s,2)=1000*sqrt(sum1/pnum);
    end
    mean_b1_ch_crs_xiuzheng(t,:)=mean_ave(:,2);
    mean_single_ch_crs_xiuzheng(t,:)=mean_ave(:,3);
    std_b1_ch_crs_xiuzheng(t,:)=std_ave(:,2);
    temperature1(:,t)=temp_ave;
    single_b1_ch_xiuzheng(t,:)=single_ave(:,2);
end


fclose all;
  