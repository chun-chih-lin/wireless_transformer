clc
clear
close all
%%

message = randi([0, 1], 2056, 1);
bt_LE1M_waveform = bleWaveformGenerator(message, Mode="LE1M");

bt_LE2M_waveform = bleWaveformGenerator(message, Mode="LE2M");

bt_LE500k_waveform = bleWaveformGenerator(message, Mode="LE500K");

bt_LE125k_waveform = bleWaveformGenerator(message, Mode="LE125K");

figure()
subplot(2, 2, 1)
plot(real(bt_LE1M_waveform))
hold on
plot(imag(bt_LE1M_waveform))
xlim([0, 200])

subplot(2, 2, 2)
plot(real(bt_LE2M_waveform))
hold on
plot(imag(bt_LE2M_waveform))
xlim([0, 200])

subplot(2, 2, 3)
plot(real(bt_LE500k_waveform))
hold on
plot(imag(bt_LE500k_waveform))
xlim([0, 200])

subplot(2, 2, 4)
plot(real(bt_LE125k_waveform))
hold on
plot(imag(bt_LE125k_waveform))
xlim([0, 200])


zigbee_psdu_len = 127;
psdu = randi([0, 1], zigbee_psdu_len*8, 1);
spc = 8;
zigbee_cfg = lrwpanOQPSKConfig("Band", 2450, "SamplesPerChip", spc, "PSDULength", zigbee_psdu_len);
waveOQPSK = lrwpanWaveformGenerator(psdu, zigbee_cfg);

figure();
plot(real(waveOQPSK))
hold on
plot(imag(waveOQPSK))
xlim([0, 200])


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

BPSK_psdu = randi([0 1], 8*nonHT_BPSK_cfg.PSDULength, 1, 'int8');
QPSK_psdu = randi([0 1], 8*nonHT_QPSK_cfg.PSDULength, 1, 'int8');
QAM16_psdu = randi([0 1], 8*nonHT_16QAM_cfg.PSDULength, 1, 'int8');
QAM64_psdu = randi([0 1], 8*nonHT_64QAM_cfg.PSDULength, 1, 'int8');

[range, numBits] = scramblerRange(nonHT_BPSK_cfg);
BPSK_scramInit = randi(range);
nonHT_BPSK_waveform = wlanNonHTData(BPSK_psdu, nonHT_BPSK_cfg, BPSK_scramInit);

[range, numBits] = scramblerRange(nonHT_QPSK_cfg);
QPSK_scramInit = randi(range);
nonHT_QPSK_waveform = wlanNonHTData(QPSK_psdu, nonHT_QPSK_cfg, QPSK_scramInit);

[range, numBits] = scramblerRange(nonHT_16QAM_cfg);
QAM16_scramInit = randi(range);
nonHT_16QAM_waveform = wlanNonHTData(QAM16_psdu, nonHT_16QAM_cfg, QAM16_scramInit);

[range, numBits] = scramblerRange(nonHT_64QAM_cfg);
QAM64_scramInit = randi(range);
nonHT_64QAM_waveform = wlanNonHTData(QAM64_psdu, nonHT_64QAM_cfg, QAM64_scramInit);


size(nonHT_BPSK_waveform)
size(nonHT_QPSK_waveform)
size(nonHT_16QAM_waveform)
size(nonHT_64QAM_waveform)

size(waveOQPSK)

size(bt_LE1M_waveform)
size(bt_LE2M_waveform)
size(bt_LE500k_waveform)
size(bt_LE125k_waveform)



































