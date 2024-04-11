clc
clear
close all
%%
mod_list = ["BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "CPFSK", "WBFM", "AM-SSB", "AM-DSB", "GFSK", "PAM4"];
% mod_list = ["AM-SSB", "AM-DSB", "WBFM", "PAM4"];

data_folder = "..\RML2016.10a\";
% data_folder = ".\";

snr_lvl = "18";

M = 64;
y = qammod((0:M-1), M)/7
if 1
    return
end

for mod = mod_list
    % filename = strcat('Trimmed.', mod, '.mat');
    filename = strcat(mod, '.', snr_lvl, '.mat');
    loaddata = load(strcat(data_folder, filename)).data;

    time_fig = figure();
    subplot(2, 1, 1)
    for p = 10:15
        plot(squeeze(loaddata(p, 1, :)), 'DisplayName', num2str(p))
        hold on
    end
    legend
    ylim([-0.02, 0.02])

    subplot(2, 1, 2)
    for p = 10:15
        plot(squeeze(loaddata(p, 2, :)), 'DisplayName', num2str(p))
        hold on
    end
    legend
    ylim([-0.02, 0.02])
    sgtitle(filename, Interpreter="none")
    time_fig.Position = [100, 100, 1000, 600];

    if 1
        continue
    end
    % rand_i = randi([1, size(loaddata, 1)], 1, 1);
    rand_i = 30;

    len_sig = 128;

    rx_sig = loaddata(rand_i, 1, 1:len_sig) + 1j*loaddata(rand_i, 2, 1:len_sig);
    rx_sig = squeeze(rx_sig).';
    

    %% Time Correlation
    % for s_i = 1:len_sig/2
    for s_i = 50:53
        s = s_i;
        e = s_i + len_sig/2 - 1;
        [apply_ret, r, method_name] = apply_autocorr(rx_sig(s:e), len_sig/2 - 1, 5);
        auto_corr_fig = show_autocorr(r, strcat(filename, '.Shift.', num2str(s_i)));
    end

    if 0
        continue
    end
    %% DFT
    correlation = zeros(1, len_sig/2);
    for s_i = 1:len_sig/2
        s = s_i;
        e = s_i + len_sig/2 - 1;
    
        [dft_ret, dft_r] = apply_dft(rx_sig(s:e));
        correlation(s_i) = frequency_correlation(abs(dft_ret));
    end

    fig = figure();
    subplot(3, 2, 1)
    plot(real(rx_sig))
    hold on
    plot(imag(rx_sig))
    xlim([1, len_sig])

    subplot(3, 2, 3)
    plot(abs(fftshift(dft_ret)))
    xlim([1, length(dft_ret)])

    subplot(3, 2, 5)
    bar(correlation)
    ylim([0.5, 1.1])

    max_amp = max(max(abs(real(rx_sig))), max(abs(imag(rx_sig))));
    subplot(3, 2, [2, 4, 6])
    plot(real(rx_sig), imag(rx_sig), '.')
    axis square
    xlim([-1.1*max_amp, 1.1*max_amp])
    ylim([-1.1*max_amp, 1.1*max_amp])

    sgtitle(filename, Interpreter="none")
    fig.Position = [100, 100, 800, 400];

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













































