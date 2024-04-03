clc
clear
close all

%%
% https://en.wikipedia.org/wiki/DFT_matrix
%%
dft_matrix = dftmtx(64);

save_fig_folder = "./results/";

sync_long = get_sync_long();

cfg = wlanHTConfig('ChannelBandwidth', 'CBW20');
HTLTF = wlanHTLTF(cfg);
HTSTF = wlanHTSTF(cfg);

sync_long_dot_ret = row_x_matrix(HTLTF(1:64).', dft_matrix);
sync_short_dot_ret = row_x_matrix(HTSTF(1:64).', dft_matrix);

figure();
subplot(2, 2, 1)
plot(real(HTLTF), 'b')
hold on
plot(imag(HTLTF), 'r')
xlim([1, 64])
title("Long-Training-Field")

subplot(2, 2, 2)
plot(real(HTSTF), 'b')
hold on
plot(imag(HTSTF), 'r')
xlim([1, 64])
title("Short-Training-Field")

subplot(2, 2, 3)
plot(real(sync_long_dot_ret), 'b')
hold on
plot(imag(sync_long_dot_ret), 'r')
xlim([1, 64])
title("DFT Long-Training-Field")

subplot(2, 2, 4)
plot(real(sync_short_dot_ret), 'b')
hold on
plot(imag(sync_short_dot_ret), 'r')
xlim([1, 64])
title("DFT Short-Training-Field")

for e = 0:7
    [dataset, len] = get_signal(e, 128);

    n_odfm_symbol = floor(len/80);

    for i_symbol = 1:n_odfm_symbol
        smp_s = (i_symbol-1)*80+1;
        smp_e = i_symbol*80;
        
        symbol_sample = dataset(:, smp_s:smp_e);
        symbol_complex = symbol_sample(1, :) + 1j*symbol_sample(2, :);

        % ------------------------------------------
        
        dot_ret_cyclic = zeros(64, 64);
        for i_sample = 1:64
            cyclic_sample = circshift(symbol_complex(1:64), i_sample-1);
            dot_ret = row_x_matrix(cyclic_sample, dft_matrix);
            dot_ret_cyclic(i_sample, :) = dot_ret;
        end
        
        % ------------------------------------------
        % fig = figure();
        % subplot(2, 2, 1)
        % surf(real(dot_ret_cyclic))
        % xlabel("subcarrier response")
        % ylabel("cyclic shift step")
        % title("Real")
        % view(2)
        % xlim([1, 64])
        % ylim([1, 64])
        % axis square
        % colorbar
        % 
        % subplot(2, 2, 2)
        % surf(imag(dot_ret_cyclic))
        % xlabel("subcarrier response")
        % ylabel("cyclic shift step")
        % title("Imag")
        % view(2)
        % xlim([1, 64])
        % ylim([1, 64])
        % axis square
        % colorbar
        % 
        % subplot(2, 2, 3)
        % surf(abs(dot_ret_cyclic))
        % xlabel("subcarrier response")
        % ylabel("cyclic shift step")
        % title("Amplitude")
        % view(2)
        % xlim([1, 64])
        % ylim([1, 64])
        % axis square
        % colorbar
        % 
        % subplot(2, 2, 4)
        % surf(angle(dot_ret_cyclic))
        % xlabel("subcarrier response")
        % ylabel("cyclic shift step")
        % title("Phase")
        % view(2)
        % xlim([1, 64])
        % ylim([1, 64])
        % axis square
        % colorbar
        % 
        % fig.Position = [100, 0, 1200, 900];
        % sgtitle(strcat("Encoding: ", num2str(e)))
        

        % Show the signal
        show_cyclic = 1;
        fig = figure();
        subplot(2, 2, 2)
        plot(symbol_sample(1, :), 'b-')
        hold on
        plot(symbol_sample(2, :), 'r-')
        title("Original Signal")
        xlim([1, 64])

        subplot(2, 2, 4)
        plot(real(dot_ret_cyclic(show_cyclic, :)), 'b-')
        hold on
        title("DFT Result")
        plot(imag(dot_ret_cyclic(show_cyclic, :)), 'r-')
        xlim([1, 64])
        ylim([-10, 10])

        subplot(2, 2, [1, 3])
        plot(real(dot_ret_cyclic(show_cyclic, :)), imag(dot_ret_cyclic(show_cyclic, :)), 'bo')
        axis square
        grid on
        hold on
        xlim([-15, 15])
        ylim([-15, 15])

        fig.Position = [0, 100, 1200, 500];

        filename = strcat('E', num2str(e), '_Rand.png')
        saveas(fig, strcat(save_fig_folder, filename))
        break
    end
    break
end


%% Functions
function r = row_x_matrix(row_v, i_matrix)
    r = zeros(1, length(row_v));
    for i = 1:length(row_v)
        i_matrix_c = i_matrix(:, i);
        r(i) = sum(dot(row_v, i_matrix_c.', 1));
    end
end


function [d, len] = get_signal(e, pdu_len)
    if pdu_len == 38
        len_tbl = [1521, 1201, 961, 801, 721, 641, 561, 561];   % 38
    elseif pdu_len == 48
        len_tbl = [1761, 1361, 1121, 881, 801, 641, 641, 561];   % 48
    elseif pdu_len == 68
        len_tbl = [2321, 1681, 1361, 1041, 881, 721, 641, 641];   % 68
    elseif pdu_len == 128
        len_tbl = [3921, 2801, 2161, 1601, 1281, 1041, 881, 801];   % 128
    end

    len = len_tbl(e+1);
    filename = strcat("Simulated_signal_", num2str(e), "_", num2str(pdu_len), "_rand.mat");
    d = squeeze(load(filename).data);
    d = d(:, 1:len);
end

function sync_long = get_sync_long()
    sync_long = [-0.0455 - 1.0679*1j, 0.3528 - 0.9865*1j, 0.8594 + 0.7348*1j, ...
                 0.1874 + 0.2475*1j, 0.5309 - 0.7784*1j, -1.0218 - 0.4897*1j, ...
                 -0.3401 - 0.9423*1j, 0.8657 - 0.2298*1j, 0.4734 + 0.0362*1j, ...
                 0.0088 - 1.0207*1j, -1.2142 - 0.4205*1j, 0.2172 - 0.5195*1j, ...
                 0.5207 - 0.1326*1j, -0.1995 + 1.4259*1j, 1.0583 - 0.0363*1j, ...
                 0.5547 - 0.5547*1j, 0.3277 + 0.8728*1j, -0.5077 + 0.3488*1j, ...
                 -1.1650 + 0.5789*1j, 0.7297 + 0.8197*1j, 0.6173 + 0.1253*1j, ...
                 -0.5353 + 0.7214*1j, -0.5011 - 0.1935*1j, -0.3110 - 1.3392*1j, ...
                 -1.0818 - 0.1470*1j, -1.1300 - 0.1820*1j, 0.6663 - 0.6571*1j, ...
                 -0.0249 + 0.4773*1j, -0.8155 + 1.0218*1j, 0.8140 + 0.9396*1j, ...
                 0.1090 + 0.8662*1j, -1.3868 - 0.0000*1j, 0.1090 - 0.8662*1j, ...
                 0.8140 - 0.9396*1j, -0.8155 - 1.0218*1j, -0.0249 - 0.4773*1j, ...
                 0.6663 + 0.6571*1j, -1.1300 + 0.1820*1j, -1.0818 + 0.1470*1j, ...
                 -0.3110 + 1.3392*1j, -0.5011 + 0.1935*1j, -0.5353 - 0.7214*1j, ...
                 0.6173 - 0.1253*1j, 0.7297 - 0.8197*1j, -1.1650 - 0.5789*1j, ...
                 -0.5077 - 0.3488*1j, 0.3277 - 0.8728*1j, 0.5547 + 0.5547*1j, ...
                 1.0583 + 0.0363*1j, -0.1995 - 1.4259*1j, 0.5207 + 0.1326*1j, ...
                 0.2172 + 0.5195*1j, -1.2142 + 0.4205*1j, 0.0088 + 1.0207*1j, ...
                 0.4734 - 0.0362*1j, 0.8657 + 0.2298*1j, -0.3401 + 0.9423*1j, ...
                 -1.0218 + 0.4897*1j, 0.5309 + 0.7784*1j, 0.1874 - 0.2475*1j, ...
                 0.8594 - 0.7348*1j, 0.3528 + 0.9865*1j, -0.0455 + 1.0679*1j, ...
                 1.3868 - 0.0000*1j];
end



































