clc
clear 
close all
%%
global data_prefix folder_name color_steps
mod_list = ["BPSK.0", "BPSK.1", "QPSK.2", "QPSK.3", "16QAM.4", "16QAM.5", "64QAM.6", "64QAM.7", ...
            "am_dsb", "am_ssb", "cpfsk", "fsk", "pam", "wbfm"];
% mod_list = ["am_dsb", "am_ssb"];
data_prefix = "room_325_1m";
folder_name = strcat("./", data_prefix, "/");

cfg = wlanHTConfig('ChannelBandwidth', 'CBW20');
HTSTF = wlanLSTF(cfg).';
HTLTF = wlanLLTF(cfg).';
LLTF = wlanLLTF(cfg).';

% for mcs = 0:1:7
%     nonHTcfg = wlanNonHTConfig("ChannelBandwidth", "CBW20", ...
%                                "MCS", mcs, ...
%                                "PSDULength", 1000);
%     psdu = randi([0, 1], nonHTcfg.PSDULength*8, 1);
%     gen_signal = wlanNonHTData(psdu, nonHTcfg);
% 
%     s = 401;
%     dft_ret = apply_dft(gen_signal(s:s+64-1).');
%     size(dft_ret)
% 
%     fig = figure();
%     subplot(1, 2, 1)
%     plot(real(dft_ret(1:64)))
%     hold on
%     plot(imag(dft_ret(1:64)))
%     xlim([1, 64])
%     axis square
% 
%     subplot(1, 2, 2)
%     plot(real(dft_ret(1:64)), imag(dft_ret(1:64)), "*")
%     axis square
% 
%     sgtitle(strcat("MCS: ", num2str(mcs)))
%     fig.Position = [100, 100, 1000, 400]
% 
%     % return
% end

len_sample = 128;

step_sub_sample = 1;
len_sub_sample = 64;

% Sequence Step Size for one input
sub_seq = 0:step_sub_sample:len_sample-1;
color_steps = jet(length(sub_seq));

% for mod_i = 1:length(mod_list)
for mod_i = 1:8
    mod_name = mod_list(mod_i);
    
    nonHTcfg = wlanNonHTConfig("ChannelBandwidth", "CBW20", ...
                               "MCS", mod_i-1, ...
                               "PSDULength", 1000);
    psdu = randi([0, 1], nonHTcfg.PSDULength*8, 1);
    gen_signal = wlanWaveformGenerator(psdu, nonHTcfg);
    rx_signal = gen_signal.';

    rx_signal = load_mat(mod_name);
    if size(rx_signal, 1) ~= 1
        rx_signal = rx_signal(5, :);
    end
    size(rx_signal)

    h = rx_signal(161:320)./HTLTF;
    h1 = h(1:64);
    h2 = h(81:144);
    h = (h1 + h2)/2;

    symbol_1 = rx_signal(321:321+63)./h;
    dft_ret = apply_dft(symbol_1);

    % fig = figure();
    % subplot(1, 2, 1)
    % plot(real(rx_signal(321:321+15)), 'b-')
    % hold on
    % plot(imag(rx_signal(321:321+15)), 'r-')
    % hold on
    % plot(real(rx_signal(320+65:321+79)), 'b-.*')
    % hold on
    % plot(imag(rx_signal(320+65:321+79)), 'r-.*')
    % hold on
    % 
    % subplot(1, 2, 2)
    % plot(real(dft_ret), imag(dft_ret), 'o')
    % axis square
    % fig.Position = [100, 100, 1000, 400];

    
    start_sample = randi([1, length(rx_signal) - len_sample], 1, 1);
    start_sample = 400;

    % Actuall index for input
    sample_seq = start_sample+sub_seq;

    % Number of Steps
    len_sample_seq = length(sample_seq);
    
    s = start_sample;
    e = s + len_sample - 1;
    complex_sample = rx_signal(s:e);
    
    %% Time correlations
    if 0
        [corr_H, corr_R] = corrmtx(complex_sample, len_sub_sample - 1, "covariance");

        corr_fig = figure();
        subplot(2, 2, 1)
        surf(abs(corr_H))
        title("Amp H")
        view(2)
        axis square

        subplot(2, 2, 3)
        surf(angle(corr_H))
        title("Phase H")
        view(2)
        axis square

        subplot(2, 2, 2)
        surf(abs(corr_R))
        view(2)
        title("Amp R")
        axis square

        subplot(2, 2, 4)
        surf(angle(corr_R))
        view(2)
        title("Phase R")
        axis square
        
        corr_fig.Position = [100, 100, 1000, 800];
        sgtitle(strcat("Correlations Feature Extract: ", mod_name, "_Shifted_", num2str(start_sample)), Interpreter="none")
    end

    % break

    %% DFT Features
    if 1
        S_A = zeros(len_sub_sample, len_sub_sample);
        for n = 1:len_sub_sample
            S_A(n, :) = complex_sample(n:n + len_sub_sample - 1)./h;
        end
        DFT = dftmtx(64);
        S_F_A = S_A*DFT;
        F_A = S_A*DFT*S_A.';

        fig = figure();

        subplot(1, 3, 1)
        for s_i = 1:1
            plot(real(S_F_A(s_i, :)), imag(S_F_A(s_i, :)), "*")
            hold on
        end
        axis square

        subplot(1, 3, 2)
        for s_i = 1:1
            plot(real(F_A(s_i, :)), imag(F_A(s_i, :)), "*")
            hold on
        end
        axis square
    
        subplot(1, 3, 3)
        surf(angle(F_A))
        view(2)
        xlim([1, 64])
        ylim([1, 64])
        title("Feature ALL Phase")
        axis square
    
        fig.Position = [100, 100, 1000, 400];
        sgtitle(strcat("DFT Feature Extract: ", mod_name, "_Shifted_", num2str(start_sample)), Interpreter="none")
    end
end


%% Functions
function y = load_mat(mod_name)
    global data_prefix folder_name
    mat_filename = strcat(data_prefix, ".", mod_name, ".dat.mat");
    full_filename = strcat(folder_name, mat_filename);

    l = load(full_filename);
    if isfield(l, 'data')
        y = l.data;
    else
        y = l.legitimate_packet;
    end
end

function [y, r] = apply_dft(samples)
    dft_matrix = dftmtx(64);

    y = zeros(1, length(samples));
    for i = 1:length(samples)
        i_matrix_c = dft_matrix(:, i);
        y(i) = sum(dot(samples, i_matrix_c.', 1));
    end
    
    len_ary = length(y);
    l_ary = abs(y(2:len_ary/2+1));
    u_ary = abs(y(len_ary:-1:len_ary/2+1));

    uni_l_ary = l_ary/sqrt(sum(l_ary.^2));
    uni_u_ary = u_ary/sqrt(sum(u_ary.^2));

    r = dot(uni_l_ary, uni_u_ary);
end

function [y, r, method_name] = apply_autocorr(samples, m, method_index)
    if isnumeric(method_index)
        if method_index == 1
            method_name = "autocorrelation";
        elseif method_index == 2
            method_name = "prewindowed";
        elseif method_index == 3
            method_name = "postwindowed";
        elseif method_index == 4
            method_name = "covariance";
        else
            method_name = "modified";
        end
    else 
        method_name = method_index;
    end
    [y, r] = corrmtx(samples, m, method_name);
end

function fig = show_dft(ttl_dft_ret, ttl_dft_r, sub_seq, title_name)
    global color_steps
    len_seq = length(ttl_dft_r);

    fig = figure();

    subplot(3, 2, 1)
    for s_i = 1:len_seq
        plot(abs(ttl_dft_ret(s_i, :)))
        hold on
    end
    xlabel("Subcarriers")
    ylabel("Correlation Amplitude")
    xlim([1, 64])
    
    subplot(3, 2, 5)
    for s_i = 1:len_seq
        bar(sub_seq(s_i), ttl_dft_r(s_i), ...
            "FaceColor", color_steps(s_i, :))
        hold on
    end
    yline(1.0, 'r')
    ylabel("Correlation")
    ylim([0, 1.1])

    subplot(3, 2, [2, 4, 6])
    axis_max = max(max(real(ttl_dft_ret), [], "all"), max(real(ttl_dft_ret), [], "all"));
    for s_i = 1:len_seq
        plot(real(ttl_dft_ret(s_i, :)), imag(ttl_dft_ret(s_i, :)), ...
            "o", "Color", color_steps(s_i, :))
        hold on
    end
    axis square
    xlim([-1.1*axis_max 1.1*axis_max])
    ylim([-1.1*axis_max 1.1*axis_max])

    sgtitle(title_name, Interpreter="none")
    fig.Position = [400, 300, 1200, 500];
end

function fig = show_autocorr(r, title_name)
    fig = figure();
    subplot(2, 2, 1)
    surf(real(r), 'EdgeColor', 'none')
    axis square
    title("Real")
    colorbar
    view(2)

    subplot(2, 2, 2)
    surf(imag(r), 'EdgeColor', 'none')
    axis square
    title("Imag")
    colorbar
    view(2)
    
    subplot(2, 2, 3)
    surf(abs(r), 'EdgeColor', 'none')
    axis square
    title("Absolute")
    colorbar
    view(2)

    subplot(2, 2, 4)
    surf(angle(r), 'EdgeColor', 'none')
    axis square
    title("Phase")
    colorbar
    view(2)

    fig.Position = [100, 200, 800, 600];
    sgtitle(title_name, Interpreter="none")
end














































