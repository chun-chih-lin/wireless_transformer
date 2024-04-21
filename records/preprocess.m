clc
clear 
close all
%%
global data_prefix folder_name color_steps mod_name fig_folder_name
mod_list = ["BPSK.0", "BPSK.1", "QPSK.2", "QPSK.3", "16QAM.4", "16QAM.5", "64QAM.6", "64QAM.7", ...
            "pam", "wbfm", "cpfsk", "fsk", "am_ssb", "am_dsb"];
% mod_list = ["cpfsk"];
data_prefix = "room_325_1m";
folder_name = strcat("./", data_prefix, "/");
fig_folder_name = strcat(folder_name, "figures/");

cfg = wlanHTConfig('ChannelBandwidth', 'CBW20');
HTSTF = wlanLSTF(cfg).';
HTLTF = wlanLLTF(cfg).';
LLTF = wlanLLTF(cfg).';

len_sample = 128;

step_sub_sample = 1;
len_sub_sample = 64;

% Sequence Step Size for one input
sub_seq = 0:step_sub_sample:len_sample-1;
color_steps = jet(length(sub_seq));

for mod_i = 1:length(mod_list)
% for mod_i = 1:2
    mod_name = mod_list(mod_i);
    
    % nonHTcfg = wlanNonHTConfig("ChannelBandwidth", "CBW20", ...
    %                            "MCS", mod_i-1, ...
    %                            "PSDULength", 1000);
    % psdu = randi([0, 1], nonHTcfg.PSDULength*8, 1);
    % gen_signal = wlanWaveformGenerator(psdu, nonHTcfg);
    % rx_signal = gen_signal.';

    rx_signal = load_mat(mod_name);
    if size(rx_signal, 1) ~= 1
        rx_signal = rx_signal(2, :);
    end

    % h = rx_signal(161:320)./HTLTF;
    % h1 = h(1:64);
    % h2 = h(81:144);
    % h = (h1 + h2)/2;

    % symbol_1 = rx_signal(321:321+63)./h;
    % dft_ret = apply_dft(symbol_1);

    % fig = figure();
    % % subplot(1, 2, 1)
    % plot(real(rx_signal(161:320)), 'b-')
    % hold on
    % plot(imag(rx_signal(161:320)), 'r-')
    % hold on
    % plot(real(LLTF), 'b*')
    % hold on
    % plot(imag(LLTF), 'r*')

    % subplot(1, 2, 2)
    % % plot(real(dft_ret), imag(dft_ret), 'o')
    % plot(abs(dft_ret))
    % axis square
    % fig.Position = [100, 100, 800, 600];

    
    start_sample = randi([1, length(rx_signal) - len_sample], 1, 1);
    % start_sample = 400;

    % Actuall index for input
    sample_seq = start_sample+sub_seq;

    % Number of Steps
    len_sample_seq = length(sample_seq);
    
    s = start_sample;
    % s = 4;
    e = s + len_sample - 1;
    complex_sample = rx_signal(s:e);
    
    %% Time correlations
    [corr_H, corr_R] = apply_autocorr(complex_sample(1:len_sub_sample), len_sub_sample - 1, "modified");
    if 1
        
        % [corr_H, corr_R] = corrmtx(complex_sample, len_sub_sample - 1, "modified");
        title_str = strcat("Correlations Feature Extract: ", mod_name, "_Shifted_", num2str(start_sample));
        save_fig = 0;
        show_autocorr(corr_R, title_str, save_fig);
    end

    break

    %% DFT Features
    if 1
        S_A = zeros(len_sub_sample, len_sub_sample);
        for n = 1:len_sub_sample
            S_A(n, :) = complex_sample(n:n + len_sub_sample - 1);
        end
        DFT = dftmtx(64);
        S_F_A = DFT*S_A.';
        F_A = S_A*DFT*S_A.';

        freq_corr = zeros(1, len_sub_sample);
        for n = 1:len_sub_sample
            freq_corr(1, n) = frequency_correlation(abs(S_F_A(n, :)));
        end

        fig = figure();

        subplot(2, 2, 1)
        for n = 1:len_sub_sample
            dft_ret = apply_dft(complex_sample(n:n + len_sub_sample - 1));
            correlation = frequency_correlation(abs(dft_ret));
            bar(n, correlation)
            hold on
        end
        % bar(freq_corr)
        xlim([-1, 65])
        ylim([0.5, 1.05])
        axis square

        subplot(2, 2, 2)
        for n = 1:len_sub_sample
            plot(abs(fftshift(fft(complex_sample(n:n + len_sub_sample - 1), len_sub_sample))))
            hold on
        end
        % xlim([-1, 65])
        % ylim([0.5, 1.05])
        axis square

        subplot(2, 2, 3)
        for s_i = 1:len_sub_sample
            plot(real(S_F_A(s_i, :)), imag(S_F_A(s_i, :)), "o")
            hold on
            % plot(real(F_A(s_i, :)), imag(F_A(s_i, :)), "o")
            % hold on
        end
        axis square
    
        % subplot(2, 2, 3)
        % surf(angle(F_A), 'EdgeColor', 'none')
        % view(2)
        % xlim([1, 64])
        % ylim([1, 64])
        % title("Feature ALL Phase")
        % axis square

        subplot(2, 2, 4)
        surf(abs(F_A), 'EdgeColor', 'none')
        view(2)
        xlim([1, 64])
        ylim([1, 64])
        title("Feature ALL Amplitude")
        axis square
    
        fig.Position = [100, 100, 800, 800];
        sgtitle(strcat("DFT Feature Extract: ", mod_name, "_Shifted_", num2str(start_sample)), Interpreter="none")
    end
    break
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

function y = frequency_correlation(f_ary)
    len_ary = length(f_ary);
    if mod(len_ary, 2) ~= 0
        y = null;
    end
    l_ary = f_ary(2:len_ary/2+1);
    u_ary = f_ary(len_ary:-1:len_ary/2+1);

    uni_l_ary = l_ary/sqrt(sum(l_ary.^2));
    uni_u_ary = u_ary/sqrt(sum(u_ary.^2));

    y = dot(uni_l_ary, uni_u_ary);
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

function fig = show_autocorr(r, title_name, save_fig)
    global data_prefix mod_name fig_folder_name

    if save_fig
        set(0,'DefaultFigureVisible','off')
        fig_amp = figure();
        colormap hot
        surf(abs(r), 'EdgeColor', 'none')
        axis square
        xlim([1, 64])
        ylim([1, 64])
        % title("Amplitude")
        view(2)
        fig_amp.Position = [100, 100, 450, 400];
        save_fig_name = strcat(fig_folder_name, data_prefix, '.', mod_name, '.cross_amp');
        save_figure(fig_amp, save_fig_name)

        fig_phase = figure();
        colormap hot
        surf(angle(r), 'EdgeColor', 'none')
        axis square
        xlim([1, 64])
        ylim([1, 64])
        % title("Phase")
        view(2)
        fig_phase.Position = [100, 100, 450, 400];
        save_fig_name = strcat(fig_folder_name, data_prefix, '.', mod_name, '.cross_phase');
        save_figure(fig_phase, save_fig_name)
    else
        set(0,'DefaultFigureVisible','on')
        fig = figure();
        colormap hot
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
end

function save_figure(fig, figname)
    save_fig_name_png = strcat(figname, '.png');
    save_fig_name_pdf = strcat(figname, '.pdf');

    saveas(fig, save_fig_name_png)
    exportgraphics(fig, save_fig_name_pdf)
end














































