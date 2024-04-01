clc
clear
close all
%%
% WBFM; BPSK; QPSK; 8PSK; 16QAM; 64QAM; 4PAM; CPFSK; AM-SSB; SM-DSB

%% WBFM


%% 4PAM
M = 4;          % Modulation order
input_symbol = randi([0 M-1], 100, 1);
pam_siangl = pammod(input_symbol, M);

pam_fig = figure();
plot(real(pam_siangl))
hold on
plot(imag(pam_siangl))

%% CPFSK
M = 8;          % Modulation order
k = log2(M);    % Bits per Symbol
spf = 115;      % Symbol per frame
input_bits = randi([0 1], k*spf, 1);

cpfskMod = comm.CPFSKModulator(M, "BitInput", true, "SymbolMapping", "Gray");
cpfsk_signal = cpfskMod(input_bits);

cpfsk_fig = figure();
plot(real(cpfsk_signal))
hold on
plot(imag(cpfsk_signal))


%% AM-SSB; AM-DSB
fs = 100;
fc = 10;
t = (0:1/fs:1);
x = sin(2*pi*t);

am_dsb = ammod(x, fc, fs);
am_ssb = ssbmod(x, fc, fs);

am_fig = figure();
plot(am_dsb)
hold on
plot(am_ssb)


%%
M = 4;          % Modulation order
freqsep = 8;    % Frequency Separation (Hz)
sps = 8;        % Number of sample per symbol
samp_rate = 32; % Sample rate (Hz)

input_symbol = randi([0 M-1], 10, 1);

y = fskmod(input_symbol, M, freqsep, sps, samp_rate);

fsk_fig = figure();
plot(real(y))
hold on
plot(imag(y))
xlim([1, 80])