

% [filename, path, filterindex] = uigetfile('*.*');
% fn = strcat(path,filename)
% time_interval = str2num(filename(1:length(filename)-3));






y=zeros(pnum,snum);
z=zeros(pnum,snum);
mean_ave=zeros(snum,2);
std_ave=zeros(snum,2);
temp_array=zeros(pnum,1);

for t=1
    
%     if t<=6
%         time_interval=10^t
% %         time_interval=t-1
%     else   
%         time_interval=(10^(t-6))*5
% %         time_interval=t-8
%     end
    
%     time_interval=6000
    
%     fname=['tdc_20ch_4ns_crs_v23_' num2str(time_interval) 'ns_wait_outclkIOA_wizard_div_bit.csv.csv']
%     fname=['tdc_20ch_4ns_crs_v23_' num2str(time_interval) 'ns_wait_outclkIOA_wizard_div_bit.csv']
%     fname=['tdc_20ch_4ns_crs_b1_bit_data_' num2str(time_interval) '_0.5m.csv'];
%     fid = fopen(fname);
    fid = fopen(fn);

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
            
            time_data=fine_data1+(coase2-coase1)*period-fine_data2;
            y(i,s)=time_data/1000;
%             if s==1
%                 ture_data(i,1)=coase1;
%                 ture_data(i,2)=coase2;
%                 ture_data(i,3)=fine1;
%                 ture_data(i,4)=fine2;
%             end
        end
        temp_array(i,1)=temp;
%         if temp > 32768
%             temp_array(i,1)=(temp/128-512)/2;
%         else 
%             temp_array(i,1)=temp/256;
%         end
            
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
        std_ave(s,1)=s;
        std_ave(s,2)=std(z(:,s))*1000;
%         sum=0;
%         for i=1:pnum
%             sum=sum+(z(i,s)-t25_mean(s,1))^2;
%         end
%         std_ave(s,2)=1000*sqrt(sum/pnum);
        single_ave(s,1)=s;
        single_ave(s,2)=std(y(:,s))*1000;
%         sum1=0;
%         for i=1:pnum
%             sum1=sum1+(y(i,s)-t25_mean(s,2))^2;
%         end
%         single_ave(s,2)=1000*sqrt(sum1/pnum);
    end
    mean_ch_crs(t,:)=mean_ave(:,2);
    std_ch_crs(t,:)=std_ave(:,2);
    mean_ch_n_crs(:,t)=mean_ave(:,2);
    std_ch_n_crs(:,t)=std_ave(:,2);
    single_ch(:,t)=single_ave(:,2);
    std_hist(:,t)=z(:,20);
    std_hist_single(:,t)=y(:,20);
    temperature_array(:,t)=temp_array(:,1);
end

for i=1:pnum
    std_avedata(i,1)=z(i,snum);
    std_data(i,2)=y(i,10);
end


% csvwrite(strcat(fn, '.csv'), [mean_ave(20, :), std_ave(20, 2)]);


fclose all;
  