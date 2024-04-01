clc
clear
close all

%%
dft_matrix = dftmtx(64);

for e = 0:7
    [dataset, len] = get_signal(e, 128);

    n_odfm_symbol = floor(len/80);

    for i_symbol = 9:n_odfm_symbol
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
        figure();
        subplot(3, 1, 1)
        plot(symbol_sample(1, :), 'b-')
        hold on
        plot(symbol_sample(2, :), 'r-')
        xlim([1, 80])

        subplot(3, 1, 2)
        plot(real(dot_ret_cyclic(1, :)), imag(dot_ret_cyclic(1, :)), 'bo')
        hold on
        % xlim([1, 16])

        subplot(3, 1, 3)
        plot(real(dot_ret_cyclic(1, :)), 'b-')
        hold on
        plot(imag(dot_ret_cyclic(1, :)), 'r-')
        xlim([1, 64])
        break
    end
    % break
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
    filename = strcat("Simulated_signal_", num2str(e), "_", num2str(pdu_len), ".mat");
    d = squeeze(load(filename).data);
    d = d(:, 1:len);
end





































