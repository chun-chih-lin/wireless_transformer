clc
clear
close all
%%
addpath(genpath('./wireless_signal/'))

set(0,'DefaultFigureVisible','on')

ttl_waveform = get_all_signals();
ttl_waveform_name = fieldnames(ttl_waveform);

for n_mod = 1:numel(ttl_waveform_name)
    mod_name = ttl_waveform_name{n_mod};
    waveform = ttl_waveform.(mod_name);

    % [apply_ret, r] = apply_autocorr(waveform(481:480+64), 63, 1);
    % show_autocorr(r, mod_name)
    
    fig = figure();
    ax1 = subplot(4, 2, 1);
    ax2 = subplot(4, 2, 3);
    ax3 = subplot(4, 2, 5);
    ax4 = subplot(4, 2, 7);
    ax5 = subplot(4, 2, [2, 4, 6, 8]);
    
    start_sample = 481;
    step_size = 4;
    steps = 0:step_size:64;

    color_steps = jet(length(steps));

    for step_i = 1:length(steps)
        
        step = steps(step_i);

        marker_size = 6;
        if step_i == 1
            marker_size = 14;
        end

        d_len = 64;
        s = start_sample + step;
        e = s + d_len - 1;
        shift_waveform = waveform(s:e);

        %% Correlation Section
        if 0
            [apply_ret, r, method_name] = apply_autocorr(shift_waveform, 63, 5);
            save_filename = strcat(method_name, "_", mod_name, "_Shifted_", num2str(step), '.png');
            auto_corr_fig = show_autocorr(r, strcat(mod_name, "_Shifted_", num2str(step)));

            % Save Figures
            % saveas(auto_corr_fig, strcat('./results/Correlation/', save_filename))
        end

        %% DFT Section
        dft_ret = apply_dft(shift_waveform);
        correlation = frequency_correlation(abs(dft_ret));

        axes(ax1)
        hold on
        plot(real(dft_ret))
        hold on
        plot(imag(dft_ret))
        xlim([1, 64])
        title("DFT Results")
    
        axes(ax2)
        hold on
        plot(abs(dft_ret), ...
            'Color', color_steps(step_i, :))
        xlim([1, 64])
        title("DFT Amplitude")
    
        axes(ax3)
        hold on
        plot(real(shift_waveform), ...
            'Color', color_steps(step_i, :))
        hold on
        plot(imag(shift_waveform), ...
            'Color', color_steps(step_i, :))
        xlim([1, 64])
        title("Time Signal")

        axes(ax4)
        hold on
        bar(step, correlation, ...
            'FaceColor', color_steps(step_i, :), ...
            'BarWidth', 1.5)
        xlim([-1, 65])
        ylim([0.5, 1.05])
        title("Frequency Domain Amplitude Correlation")
    
        axes(ax5)
        hold on
        plot(real(dft_ret), imag(dft_ret), 'o', ...
            'MarkerFaceColor', color_steps(step_i, :), ...
            'MarkerEdgeColor', 'k', ...
            'MarkerSize', marker_size)
        axis square
        xlim([-15, 15])
        ylim([-15, 15])
        grid on
        title("Constellation")

        
        % break
    end

    sgtitle(mod_name, Interpreter="none")
    fig.Position = [100, 100, 1200, 500];

    save_filename = strcat("DFT_", mod_name, "_Shifted_", num2str(step), '.png');
    % saveas(fig, strcat('./results/DFT/', save_filename))

    % break
end


%% Functions
% ========== auto correlations ========================
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

function [y, r, method_name] = apply_autocorr(samples, m, method_index)
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
    [y, r] = corrmtx(samples, m, method_name);
end

% =========== DFT =================================

function y = apply_dft(samples)
    dft_matrix = dftmtx(64);
    y = row_x_matrix(samples, dft_matrix);
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

function ttl_wform = get_all_signals()
    % Discrete sample:
    %   BPSK; QPSK; 8PSK; 16QAM; 64QAM; 4PAM; CPFSK
    % Continue sample:
    %   WBFM; AM-SSB; SM-DSB

    % BPSK; QPSK; 16QAM; 64QAM
    psdu_length = 100;
    wifi_0_wform = generate_wifi(mod=0, psdu_length=psdu_length);
    wifi_1_wform = generate_wifi(mod=1, psdu_length=psdu_length);
    wifi_2_wform = generate_wifi(mod=2, psdu_length=psdu_length);
    wifi_3_wform = generate_wifi(mod=3, psdu_length=psdu_length);
    wifi_4_wform = generate_wifi(mod=4, psdu_length=psdu_length);
    wifi_5_wform = generate_wifi(mod=5, psdu_length=psdu_length);
    wifi_6_wform = generate_wifi(mod=6, psdu_length=psdu_length);
    wifi_7_wform = generate_wifi(mod=7, psdu_length=psdu_length);

    % 4PAM
    pam_mod = 4;
    pam_num_symbol = 1000;
    pam_wform = generate_pam(mod=pam_mod, num_symbol=pam_num_symbol);

    % CPFSK
    cpfsk_mod = 8;
    cpfsk_spf = 115;
    cpfsk_wform = generate_cpfsk(spf=cpfsk_spf, mod=cpfsk_mod);

    % FSK
    fsk_samp_rate = 32;
    fm_sps = 8;
    fm_mod = 4;
    fm_freqsep = 8;
    fm_data_length = 100;
    fsk_wform = generate_fsk(fs=fsk_samp_rate, sps=fm_sps, mod=fm_mod, freqsep=fm_freqsep, data_length=fm_data_length);

    % AM-SSB; AM-DSB
    am_fc = 550e3;
    am_fs = 44.1e3;

    am_t = (0:1/am_fs:.02);
    continue_signal = sin(2*pi*30*am_t) + 2*sin(2*pi*60*am_t);
    [am_l_wform, am_u_wform, am_d_wform] = generate_am(continue_signal, fc=am_fc, fs=am_fs);

    % WBFM
    fm_fs = 1e3;           % Sample Frequency
    fm_fc = 200;           % Carrier Frequency 88.1 MHz - 108.1 MHz
    fm_fDev = 50;          % Frequency Deviation (Hz)/Modulation index
    fm_t = (0:1/fm_fs:1);
    continue_signal = sin(2*pi*30*fm_t) + 2*sin(2*pi*60*fm_t);
    wbfm_wform = generate_wbfm(continue_signal, fc=fm_fc, fs=fm_fs, fDev=fm_fDev);

    % Collect all the waveforms.
    ttl_wform = {};
    ttl_wform.wifi_0 = correct_dimention(wifi_0_wform);
    ttl_wform.wifi_1 = correct_dimention(wifi_1_wform);
    ttl_wform.wifi_2 = correct_dimention(wifi_2_wform);
    ttl_wform.wifi_3 = correct_dimention(wifi_3_wform);
    ttl_wform.wifi_4 = correct_dimention(wifi_4_wform);
    ttl_wform.wifi_5 = correct_dimention(wifi_5_wform);
    ttl_wform.wifi_6 = correct_dimention(wifi_6_wform);
    ttl_wform.wifi_7 = correct_dimention(wifi_7_wform);
    ttl_wform.pam = correct_dimention(pam_wform);
    ttl_wform.cpfsk = correct_dimention(cpfsk_wform);
    ttl_wform.fsk = correct_dimention(fsk_wform);
    ttl_wform.am_l = correct_dimention(am_l_wform);
    ttl_wform.am_u = correct_dimention(am_u_wform);
    ttl_wform.am_d = correct_dimention(am_d_wform);
    ttl_wform.wbfm = correct_dimention(wbfm_wform);
end

function out_ary = correct_dimention(in_ary)
    out_ary = in_ary;
    if size(in_ary, 2) == 1
        out_ary = out_ary.';
    end
end













