clc
clear
close all
%%
mod_list = ["PAM4", "BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "CPFSK", "GFSK", "AM-SSB", "AM-DSB", "WBFM"];
% mod_list = ["PAM4", "AM-SSB", "AM-DSB", "WBFM"];

% data_folder = "..\RML2016.10a\";
data_folder = "..\IgnoreMAT_IoT\";
% data_folder = ".\";

% snr_lvl = "18";
set(0,'DefaultFigureVisible','off')

Nsym = 10;           % Filter span in symbol durations
beta = 0.35;         % Roll-off factor
sps = 8;    % Upsampling factor

rxfilter = comm.RaisedCosineReceiveFilter( ...
    RolloffFactor=beta, ...
    FilterSpanInSymbols=Nsym, ...
    InputSamplesPerSymbol=sps, ...
    DecimationFactor=sps);

for mod = mod_list
    % filename = strcat('Trimmed.', mod, '.mat');
    % filename = strcat(mod, '.', snr_lvl, '.mat');
    filename = strcat(mod, '.mat');
    loaddata = load(strcat(data_folder, filename)).data;

    % ori_raw_fig = figure();
    % subplot(2, 1, 1)
    % for p = 10:15
    %     plot(squeeze(loaddata(p, 1, :)), 'DisplayName', num2str(p))
    %     hold on
    % end
    % legend
    % ylim([-0.02, 0.02])
    % 
    % subplot(2, 1, 2)
    % for p = 10:15
    %     plot(squeeze(loaddata(p, 2, :)), 'DisplayName', num2str(p))
    %     hold on
    % end
    % legend
    % ylim([-0.02, 0.02])
    % sgtitle(filename, Interpreter="none")
    % ori_raw_fig.Position = [100, 100, 1000, 600];

    rand_i = randi([1, size(loaddata, 1)], 1, 1);
    % rand_i = 66;

    len_sig = 128;

    % rx_sig = loaddata(rand_i, 1, 1:len_sig) + 1j*loaddata(rand_i, 2, 1:len_sig);
    % rx_sig = squeeze(rx_sig).';
    rx_sig = loaddata(rand_i, :);

    %% Time Correlation


    %% DFT
    correlation = zeros(1, len_sig/2);
    ttl_dft_ret = zeros(len_sig/2, len_sig/2);
    for s_i = 1:len_sig/2
        s = s_i;
        e = s_i + len_sig/2 - 1;
    
        [dft_ret, dft_r] = apply_dft(rx_sig(s:e));
        correlation(s_i) = frequency_correlation(abs(dft_ret));
        ttl_dft_ret(s_i, :) = fftshift(dft_ret);
    end

    fig = figure();
    subplot(3, 3, 1)
    plot(real(rx_sig))
    hold on
    plot(imag(rx_sig))
    title('Total Time domain waveform')
    xlim([1, len_sig])

    subplot(3, 3, 4)
    yyaxis right
    plot(abs(fftshift(dft_ret)))
    yyaxis left
    plot(unwrap(angle(fftshift(dft_ret))))
    xlim([1, length(dft_ret)])
    title('FFT')

    subplot(3, 3, 7)
    bar(correlation)
    title('Half spectrum correlation')
    ylim([0.5, 1.1])

    max_amp = max(max(abs(real(ttl_dft_ret)), [], 'all'), max(abs(imag(ttl_dft_ret)), [], 'all'));

    subplot(3, 3, [2, 5, 8])
    step_size = 1;
    color_steps = jet(len_sig/2/step_size);
    % color_steps = winter(len_sig/2/step_size);
    for s_i = 1:step_size:len_sig/2
        plot(real(ttl_dft_ret(s_i, :)), imag(ttl_dft_ret(s_i, :)), '.', ...
            'Color', color_steps((s_i+step_size-1)/step_size, :), ...
            'MarkerSize', 10)
        hold on
    end
    % plot(real(rx_sig), imag(rx_sig), '.')
    axis square
    xlim([-1.1*max_amp, 1.1*max_amp])
    ylim([-1.1*max_amp, 1.1*max_amp])

    subplot(3, 3, [3, 6, 9])
    colormap hot
    surf(abs(ttl_dft_ret), 'EdgeColor', 'none')
    view(2)
    xlabel("Subcarriers")
    ylabel("Time Shift")
    title("Amplitude")
    axis square
    xlim([1, 64])
    ylim([1, 64])

    sgtitle(strcat("pkt: ", num2str(rand_i), '. ', filename), Interpreter="none")
    fig.Position = [100, 100, 1300, 400];


    %%
    dft_constellation_fig = figure();
    color_steps = jet(len_sig/2/step_size);
    for s_i = 1:step_size:len_sig/2
        plot(real(ttl_dft_ret(s_i, :)), imag(ttl_dft_ret(s_i, :)), '.', ...
            'Color', color_steps((s_i+step_size-1)/step_size, :), ...
            'MarkerSize', 10)
        hold on
    end
    axis square
    set(gca, 'Xticklabel', [], 'YTickLabel', []);
    xlim([-1.1*max_amp, 1.1*max_amp])
    ylim([-1.1*max_amp, 1.1*max_amp])
    dft_constellation_fig.Position = [100, 100, 300, 300];
    constellation_fig_name = strcat("DFT_", mod, "_Constellation_Example");
    save_figure(dft_constellation_fig, constellation_fig_name)

    dft_overall_fig = figure();
    colormap hot
    surf(abs(ttl_dft_ret), 'EdgeColor', 'none')
    view(2)
    set(gca, 'Xticklabel', [], 'YTickLabel', []);
    axis square
    xlim([1, 64])
    ylim([1, 64])
    dft_overall_fig.Position = [100, 100, 300, 300];
    dft_fig_name = strcat("DFT_", mod, "_OverSignal_Example");
    save_figure(dft_overall_fig, dft_fig_name)

    % break
end

%% Functions
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
% ------------------

function [y, r] = apply_dft(samples)
    dft_matrix = dftmtx(length(samples));

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

function save_figure(fig, figname)
    % global result_folder_name
    result_folder_name = "../results/";
    save_fig_name_png = strcat(result_folder_name, figname, '.png')
    save_fig_name_pdf = strcat(result_folder_name, figname, '.pdf')

    saveas(fig, save_fig_name_png)
    exportgraphics(fig, save_fig_name_pdf)
end











































