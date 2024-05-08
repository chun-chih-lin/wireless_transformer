clc
clear
close all
%%

% message = randi([0, 1], 2056, 1);
% bt_LE1M_waveform = bleWaveformGenerator(message, Mode="LE1M");
% 
% bt_LE2M_waveform = bleWaveformGenerator(message, Mode="LE2M");
% 
% bt_LE500k_waveform = bleWaveformGenerator(message, Mode="LE500K");
% 
% bt_LE125k_waveform = bleWaveformGenerator(message, Mode="LE125K");

% figure()
% subplot(2, 2, 1)
% plot(real(bt_LE1M_waveform))
% hold on
% plot(imag(bt_LE1M_waveform))
% xlim([0, 200])
% 
% subplot(2, 2, 2)
% plot(real(bt_LE2M_waveform))
% hold on
% plot(imag(bt_LE2M_waveform))
% xlim([0, 200])
% 
% subplot(2, 2, 3)
% plot(real(bt_LE500k_waveform))
% hold on
% plot(imag(bt_LE500k_waveform))
% xlim([0, 200])
% 
% subplot(2, 2, 4)
% plot(real(bt_LE125k_waveform))
% hold on
% plot(imag(bt_LE125k_waveform))
% xlim([0, 200])


% zigbee_psdu_len = 127;
% psdu = randi([0, 1], zigbee_psdu_len*8, 1);
% spc = 8;
% zigbee_cfg = lrwpanOQPSKConfig("Band", 2450, "SamplesPerChip", spc, "PSDULength", zigbee_psdu_len);
% waveOQPSK = lrwpanWaveformGenerator(psdu, zigbee_cfg);

% figure();
% plot(real(waveOQPSK))
% hold on
% plot(imag(waveOQPSK))
% xlim([0, 200])

num_bpsk_data = 1;

nonHT_BPSK_cfg = wlanNonHTConfig(...
    "ChannelBandwidth", "CBW20", ...
    "MCS", 0, ...
    "PSDULength", 4095);
nonHT_QPSK_cfg = wlanNonHTConfig(...
    "ChannelBandwidth", "CBW20", ...
    "MCS", 2, ...
    "PSDULength", 4095);
nonHT_16QAM_cfg = wlanNonHTConfig(...
    "ChannelBandwidth", "CBW20", ...
    "MCS", 4, ...
    "PSDULength", 4095);
nonHT_64QAM_cfg = wlanNonHTConfig(...
    "ChannelBandwidth", "CBW20", ...
    "MCS", 6, ...
    "PSDULength", 4095);

% BPSK_psdu = randi([0 1], 8*nonHT_BPSK_cfg.PSDULength, 1, 'int8');
% QPSK_psdu = randi([0 1], 8*nonHT_QPSK_cfg.PSDULength, 1, 'int8');
% QAM16_psdu = randi([0 1], 8*nonHT_16QAM_cfg.PSDULength, 1, 'int8');
% QAM64_psdu = randi([0 1], 8*nonHT_64QAM_cfg.PSDULength, 1, 'int8');

[range, numBits] = scramblerRange(nonHT_BPSK_cfg);
BPSK_scramInit = randi(range);
BPSK_psdu = randi([0 1], 8*nonHT_BPSK_cfg.PSDULength, 1, 'int8');
nonHT_BPSK_waveform = wlanNonHTData(BPSK_psdu, nonHT_BPSK_cfg, BPSK_scramInit);
disp("BPSK Length:")
size(nonHT_BPSK_waveform, 1)
cnt_bpsk = 1;
while cnt_bpsk < num_bpsk_data
    [range, numBits] = scramblerRange(nonHT_BPSK_cfg);
    BPSK_scramInit = randi(range);
    BPSK_psdu = randi([0 1], 8*nonHT_BPSK_cfg.PSDULength, 1, 'int8');
    temp = wlanNonHTData(BPSK_psdu, nonHT_BPSK_cfg, BPSK_scramInit);
    nonHT_BPSK_waveform = cat(1, nonHT_BPSK_waveform, temp);
    disp("BPSK Length: ")
    size(nonHT_BPSK_waveform, 1)
    cnt_bpsk = cnt_bpsk + 1;
end

disp("QPSK")
[range, numBits] = scramblerRange(nonHT_QPSK_cfg);
QPSK_scramInit = randi(range);
QPSK_psdu = randi([0 1], 8*nonHT_QPSK_cfg.PSDULength, 1, 'int8');
nonHT_QPSK_waveform = wlanNonHTData(QPSK_psdu, nonHT_QPSK_cfg, QPSK_scramInit);
disp("QPSK Length:")
size(nonHT_QPSK_waveform, 1)
while length(nonHT_QPSK_waveform) < length(nonHT_BPSK_waveform)
    [range, numBits] = scramblerRange(nonHT_QPSK_cfg);
    QPSK_scramInit = randi(range);
    QPSK_psdu = randi([0 1], 8*nonHT_QPSK_cfg.PSDULength, 1, 'int8');
    temp = wlanNonHTData(QPSK_psdu, nonHT_QPSK_cfg, QPSK_scramInit);
    nonHT_QPSK_waveform = cat(1, nonHT_QPSK_waveform, temp);
    disp("QPSK Length: ")
    size(nonHT_QPSK_waveform, 1)
end


disp("16QAM")
[range, numBits] = scramblerRange(nonHT_16QAM_cfg);
QAM16_scramInit = randi(range);
QAM16_psdu = randi([0 1], 8*nonHT_16QAM_cfg.PSDULength, 1, 'int8');
nonHT_16QAM_waveform = wlanNonHTData(QAM16_psdu, nonHT_16QAM_cfg, QAM16_scramInit);
disp("16QAM Length:")
size(nonHT_16QAM_waveform, 1)
while length(nonHT_16QAM_waveform) < length(nonHT_BPSK_waveform)
    [range, numBits] = scramblerRange(nonHT_16QAM_cfg);
    QAM16_scramInit = randi(range);
    QAM16_psdu = randi([0 1], 8*nonHT_16QAM_cfg.PSDULength, 1, 'int8');
    temp = wlanNonHTData(QAM16_psdu, nonHT_16QAM_cfg, QAM16_scramInit);
    nonHT_16QAM_waveform = cat(1, nonHT_16QAM_waveform, temp);
    disp("16QAM Length: ")
    size(nonHT_16QAM_waveform, 1)
end

disp("64QAM")
[range, numBits] = scramblerRange(nonHT_64QAM_cfg);
QAM64_scramInit = randi(range);
QAM64_psdu = randi([0 1], 8*nonHT_64QAM_cfg.PSDULength, 1, 'int8');
nonHT_64QAM_waveform = wlanNonHTData(QAM64_psdu, nonHT_64QAM_cfg, QAM64_scramInit);
disp("64QAM Length:")
size(nonHT_16QAM_waveform, 1)
while length(nonHT_64QAM_waveform) < length(nonHT_BPSK_waveform)
    [range, numBits] = scramblerRange(nonHT_64QAM_cfg);
    QAM64_scramInit = randi(range);
    QAM64_psdu = randi([0 1], 8*nonHT_64QAM_cfg.PSDULength, 1, 'int8');
    temp = wlanNonHTData(QAM64_psdu, nonHT_64QAM_cfg, QAM64_scramInit);
    nonHT_64QAM_waveform = cat(1, nonHT_64QAM_waveform, temp);
    disp("64QAM Length: ")
    size(nonHT_64QAM_waveform, 1)
end
disp("----------------------------")

size(nonHT_BPSK_waveform, 1)
size(nonHT_QPSK_waveform, 1)
size(nonHT_16QAM_waveform, 1)
size(nonHT_64QAM_waveform, 1)


% save("BPSK_data_only.mat", 'nonHT_BPSK_waveform')
% save("QPSK_data_only.mat", 'nonHT_QPSK_waveform')
% save("16QAM_data_only.mat", 'nonHT_16QAM_waveform')
% save("64QAM_data_only.mat", 'nonHT_64QAM_waveform')




n_sym = 1;
s = 100*80 + 1;
e = s + 63;

plt_nonHT_BPSK_waveform = nonHT_BPSK_waveform(s:e);
plt_nonHT_QPSK_waveform = nonHT_QPSK_waveform(s:e);
plt_nonHT_16QAM_waveform = nonHT_16QAM_waveform(s:e);
plt_nonHT_64QAM_waveform = nonHT_64QAM_waveform(s:e);

BPSK_fft_ret = fftshift(fft(plt_nonHT_BPSK_waveform));
QPSK_fft_ret = fftshift(fft(plt_nonHT_QPSK_waveform));
QAM16_fft_ret = fftshift(fft(plt_nonHT_16QAM_waveform));
QAM64_fft_ret = fftshift(fft(plt_nonHT_64QAM_waveform));

BPSK_pilot = [BPSK_fft_ret(12), BPSK_fft_ret(26), BPSK_fft_ret(40), BPSK_fft_ret(54)]
QPSK_pilot = [QPSK_fft_ret(12), QPSK_fft_ret(26), QPSK_fft_ret(40), QPSK_fft_ret(54)];
QAM16_pilot = [QAM16_fft_ret(12), QAM16_fft_ret(26), QAM16_fft_ret(40), QAM16_fft_ret(54)];
QAM64_pilot = [QAM64_fft_ret(12), QAM64_fft_ret(26), QAM64_fft_ret(40), QAM64_fft_ret(54)];


x = 1
h = exp(j*pi/3)
y = x*h
hh = x/y
xx = hh*y

% figure()
% subplot(2, 2, 1)
% plot(real(BPSK_fft_ret))
% hold on
% plot(imag(BPSK_fft_ret))
% xlim([1, 64])
% 
% subplot(2, 2, 2)
% plot(real(QPSK_fft_ret))
% hold on
% plot(imag(QPSK_fft_ret))
% xlim([1, 64])
% 
% subplot(2, 2, 3)
% plot(real(QAM16_fft_ret))
% hold on
% plot(imag(QAM16_fft_ret))
% xlim([1, 64])
% 
% subplot(2, 2, 4)
% plot(real(QAM64_fft_ret))
% hold on
% plot(imag(QAM64_fft_ret))
% xlim([1, 64])

% 
% figure()
% subplot(2, 2, 1)
% plot(real(BPSK_fft_ret), imag(BPSK_fft_ret), '.')
% 
% subplot(2, 2, 2)
% plot(real(QPSK_fft_ret), imag(QPSK_fft_ret), '.')
% 
% subplot(2, 2, 3)
% plot(real(QAM16_fft_ret), imag(QAM16_fft_ret), '.')
% 
% subplot(2, 2, 4)
% plot(real(QAM64_fft_ret), imag(QAM64_fft_ret), '.')
% 
% 
% 
% size(waveOQPSK)
% 
% size(bt_LE1M_waveform)
% size(bt_LE2M_waveform)
% size(bt_LE500k_waveform)
% size(bt_LE125k_waveform)



































