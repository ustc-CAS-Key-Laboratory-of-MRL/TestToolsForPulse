for s=1:snum
    filename1=['tdc_20ch_8ns_crs_b1_bit_retest_125M_balance_ch' num2str(s) '_code1.csv'];                                                                                                                    
    filename2=['tdc_20ch_8ns_crs_b1_bit_retest_125M_balance_ch' num2str(s) '_code2.csv'];
    yy1=csvread(filename1);
    yy2=csvread(filename2);
    x1(:,:,s)=yy1;
    x2(:,:,s)=yy2;
end