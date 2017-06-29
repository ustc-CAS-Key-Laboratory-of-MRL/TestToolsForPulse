% 文件里的内容，第�?��是bin�?
% 第二列是该bin统计的个数，
% 第三列是其表示的码宽的大小（就是将个数换算为码宽对应的时间）�?
% 第四列是积分非线性修正以后的时间�?

% 实际用的时�?，进行积分非线�?修正，直接使用得到的细计数的数据�?
% 把他当做第一列的值来查找第四列对应的时间值，就可以表示细时间�?

for k=25
    temperature=25;
%     filename=['tdc_20ch_8ns_crs_b1_bit_data_retest_125M_balance_code.csv']
    [filename, path, filterindex] = uigetfile('*.*')
    fid = fopen(strcat(path,filename));

    pnum = 3000000;
    period = 4000;
    snum=20;
    bnum=28;
%     binnum=200;
    binnum=200;

    x1=zeros(binnum,2,snum);
    x2=zeros(binnum,2,snum);

    for s=1:snum
        for bn=1:binnum 
            x1(bn,1,s)=bn;
            x2(bn,1,s)=bn;
        end
    end

    for i=1:pnum
    %     ii=i
        for s=1:snum
    %         ss=s
            temp=fread(fid,1,'ubit16','b');
            coase1=fread(fid,1,'ubit32','b');
            coase2=fread(fid,1,'ubit32','b');
            fine1=fread(fid,1,'ubit20','b');
            fine2=fread(fid,1,'ubit12','b');
            x1(fine1,2,s)=x1(fine1,2,s)+1;
            x2(fine2,2,s)=x2(fine2,2,s)+1;
            if i == 100
                ture_data1(s,1)=coase1;
                ture_data1(s,2)=coase2;
                ture_data1(s,3)=fine1;
                ture_data1(s,4)=fine2;
            end
        end
    end

    for s=1:snum
        for a=1:binnum
            x1(a,3,s)=x1(a,2,s)*period/pnum;
            x2(a,3,s)=x2(a,2,s)*period/pnum;
            if a==1
                x1(a,4,s)=x1(a,3,s);
                x2(a,4,s)=x2(a,3,s);
            else 
                x1(a,4,s)=x1(a,3,s)+x1((a-1),4,s);
                x2(a,4,s)=x2(a,3,s)+x2((a-1),4,s);
            end
        end
    end

    for s=1:snum
        fname1=['tdc_20ch_8ns_crs_b1_bit_retest_125M_balance_ch' num2str(s) '_code1.csv'];
        fname2=['tdc_20ch_8ns_crs_b1_bit_retest_125M_balance_ch' num2str(s) '_code2.csv'];
        csvwrite(fname1,x1(:,:,s));
        csvwrite(fname2,x2(:,:,s));
    end
end

