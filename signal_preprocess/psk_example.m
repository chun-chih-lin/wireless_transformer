clc
clear
close all
%%
curve_di = [500, 170];

cfg = wlanNonHTConfig("MCS", 2, ...
                      'ChannelBandwidth', 'CBW20', ...
                      'Modulation', 'OFDM', ...
                      'PSDULength', 1);

psdu = randi([0 1],cfg.PSDULength*8,1);
% size(psdu)
% psdu.'

set(0,'DefaultFigureVisible','on')

wifi_waveform = wlanNonHTData(psdu, cfg);
% size(wifi_waveform)

wifi_waveform = wifi_waveform(1:64);

dft_ret = fftshift(fft(wifi_waveform));
dft_ret_i = zeros(1, length(dft_ret));
dft_ret_q = zeros(1, length(dft_ret));


wifi_time_waveform_fig = figure();
plot(real(wifi_waveform), 'b')
hold on
plot(imag(wifi_waveform), 'r')
legend("I", "Q", "NumColumns", 2)
set(gca, 'Xticklabel', [], 'YTickLabel', []);
xlim([1, 64])
ylim([-2, 2.5])
% title("WiFi Time Waveform")
wifi_time_waveform_fig.Position = [100, 500, curve_di(1), curve_di(2)];

wifi_time_waveform_fig_name = "WIFI_Time_Waveform_Example";
save_figure(wifi_time_waveform_fig, wifi_time_waveform_fig_name)


constellation_fig = figure();
color_ary = zeros(1, length(dft_ret));
for samp = 1:length(dft_ret)
    i = real(dft_ret(samp));
    q = imag(dft_ret(samp));
    if abs(i) < 0.1 || abs(q) < 0.1
        color = 'r';
        p1 = plot(i, q, 'o', 'Color', color, 'MarkerFaceColor', color);
        color_ary(samp) = 1;
    else
        color = 'b';
        p2 = plot(i, q, 'o', 'Color', color, 'MarkerFaceColor', color);
    end
    hold on
end
legend([p1, p2], "Pilot", "Info. Symbol")
axis square
xlim([-10, 15])
ylim([-10, 15])
grid on
% title("WiFi Constellation")
constellation_fig.Position = [1400, 200, 300, 300];
constellation_fig_name = "WIFI_Constellation_Example";
save_figure(constellation_fig, constellation_fig_name)

for i = 1:length(dft_ret)
    if abs(real(dft_ret(i))) < 0.1 || abs(imag(dft_ret(i))) < 0.1
    else
        if real(dft_ret(i)) > 0
            dft_ret_i(i) = 1;
        end
        if imag(dft_ret(i)) > 0
            dft_ret_q(i) = 1;
        end
    end
end
symbols = dft_ret_i + dft_ret_q*2;

color_ary(1:6) = 0;
color_ary(60:64) = 0;
MarkerSize = 4;

wifi_freq_waveform_fig = figure();
yyaxis left
plot(real(dft_ret), 'b-', 'LineWidth', 1.2)
hold on
plot(imag(dft_ret), 'r-')
hold on
for samp = 1:length(dft_ret)
    if color_ary(samp) == 1
        plot(samp, real(dft_ret(samp)), '^', ...
            'Color', 'b', ...
            'MarkerFaceColor', 'k', ...
            'MarkerSize', MarkerSize, ...
            'MarkerEdgeColor', 'none')
        hold on
        plot(samp, imag(dft_ret(samp)), '^', ...
            'Color', 'r', ...
            'MarkerFaceColor', 'k', ...
            'MarkerSize', MarkerSize, ...
            'MarkerEdgeColor', 'none')
        hold on
    end
end
xlim([1, 64])
ylim([-11, 18])
set(gca, 'YTickLabel', []);

hold on
yyaxis right
stem((7:59), symbols(7:59), '.', ...
    'Color', [.2, .2, .2])
ylabel("Symbol")
ylim([-0.5, 4.5])

ax = gca;
ax.YAxis(2).Color = 'k';
legend("I", "Q", "Pilot", "NumColumns", 3, 'Location', 'NW')
wifi_freq_waveform_fig.Position = [100, 800, curve_di(1), curve_di(2)];
wifi_freq_waveform_fig_name = "WIFI_Freq_Waveform_Example";
save_figure(wifi_freq_waveform_fig, wifi_freq_waveform_fig_name)
% title("WiFi Frequency Waveform")



M = 4;
DataLen = 64;
y = QPSK_signal(symbols);



%% Function
function st = QPSK_signal(symbols)
    curve_di = [500, 150];

    DataLen = length(symbols);

    I = zeros(DataLen, 1);
    I(find(symbols > 1)) = 1;
    Q = zeros(DataLen, 1);
    Q(find(mod(symbols, 2) == 0)) = 1;

    I = 2*I-1;
    Q = 2*Q-1;

    beta = 0.5;
    span = 6;
    sps = 8;

    [i_wt, i_waveform] = BPSK_signal(I, beta, sps, span);
    [q_wt, q_waveform] = BPSK_signal(Q, beta, sps, span);
    
    % symbols = 2*(symbols-2) + 1;
    
    st = 0:DataLen-1;
    fig = figure();
    yyaxis left
    plot(i_wt, i_waveform, 'b-')
    hold on
    plot(q_wt, q_waveform, 'r-')
    
    set(gca, 'Xticklabel', [], 'YTickLabel', []);
    ax = gca;
    ax.YAxis(2).Color = 'k';
    xlim([0 DataLen])
    ylim([-2, 2.8])
    
    yyaxis right
    stem(st, symbols, '.', ...
        'Color', [.2 .2 .2])
    ylim([-0.5, 4.5])
    ylabel("Symbol")


    legend("I", "Q", "NumColumns", 2, ...
        'Location', 'NW')
    % title("QPSK Waveform")

    fig.Position = [100, 200, curve_di(1), curve_di(2)];
    fig_name = "QPSK_Root_Raised_Cosine_Example";
    save_figure(fig, fig_name)
end

function [wt, waveform] = BPSK_signal(symbols, beta, sps, span)
    DataLen = length(symbols);
    
    DataRate = 1000;
    Fs = DataRate*sps;
    
    rctFilt = comm.RaisedCosineTransmitFilter(...
      Shape='Normal', ...
      RolloffFactor=beta, ...
      FilterSpanInSymbols=span, ...
      OutputSamplesPerSymbol=sps);
    
    b = coeffs(rctFilt);
    rctFilt.Gain = 1/max(b.Numerator);
    fltDelay = span / (2*DataRate);

    waveform = rctFilt([symbols;  zeros(span/2, 1)]);
    waveform = waveform(fltDelay*Fs + 1:end);
    wt = DataRate * (0:DataLen*sps - 1)/Fs;
end

function save_figure(fig, figname)
    % global result_folder_name
    result_folder_name = "./results/Preliminary/";
    save_fig_name_png = strcat(result_folder_name, figname, '.png')
    save_fig_name_pdf = strcat(result_folder_name, figname, '.pdf')
    % 
    % saveas(fig, save_fig_name_png)
    % exportgraphics(fig, save_fig_name_pdf)
end






































