clc
clear
close all
%%
% This script is used for section "MOTIVATION AND ASSUMPTIONS"
% Compare the defect with the old RML2016.10a dataset with the real over
% the air dataset we have.



simu_mod_list = ["PAM4", "BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "CPFSK", "GFSK", "AM-SSB", "AM-DSB", "WBFM"];
simu_snr_list = (-20:2:18);

real_mod_list = ["PAM4", "BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "CPFSK", "GFSK", "AM-SSB", "AM-DSB", "WBFM"];


for mod_i = 1:length(simu_mod_list)
    mod = simu_mod_list(mod_i);
    [s_data, r_data] = get_data(mod, -2);
    size(s_data);
    size(r_data);

    break
end


%% Function
function [s_data, r_data] = get_data(mod, snr)
    simu_folder = "./RML2016.10a/";
    real_folder = "./RML2016.10a.Real/";

    s_fn = get_simu_filename(mod, snr);
    r_fn = get_real_filename(mod);

    s_data = load(strcat(simu_folder, s_fn)).data;
    r_data = load(strcat(real_folder, r_fn)).data;
end

function f_n = get_simu_filename(mod, snr)
    f_n = strcat(mod, '.', num2str(snr), '.mat');
end

function f_n = get_real_filename(mod)
    f_n = strcat('Trimmed.', mod, '.mat');
end


















































