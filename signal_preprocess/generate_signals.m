clc
clear
close all
%%
% Discrete sample:
%   BPSK; QPSK; 8PSK; 16QAM; 64QAM; 4PAM; CPFSK
% Continue sample:
%   WBFM; AM-SSB; SM-DSB

%% Wi-Fi


%% WBFM
% http://hyperphysics.phy-astr.gsu.edu/hbase/Audio/radio.html
fs = 1e3;           % Sample Frequency
fc = 200;           % Carrier Frequency 88.1 MHz - 108.1 MHz
fDev = 50;          % Frequency Deviation (Hz)/Modulation index

t = (0:1/fs:.1);
continue_signal = sin(2*pi*30*t) + 2*sin(2*pi*60*t);

fm_signal = fmmod(continue_signal, fc, fs, fDev);
fm_fig = figure();
plot(t, fm_signal)
hold on
plot(t, continue_signal)
legend("Modulated Signal", "Original Signal")


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
% http://hyperphysics.phy-astr.gsu.edu/hbase/Audio/radio.html
fs = 44.1e3;           % Sample Frequency
fc = 550e3;           % Carrier Frequency 540k - 1600k Hz
t = (0:1/fs:.01);
continue_signal = sin(2*pi*30*t) + 2*sin(2*pi*60*t);

s_t = continue_signal;
h_t = imag(hilbert(continue_signal));
s_lsb = s_t.*cos(2*pi*fc*t) - h_t.*sin(2*pi*fc*t);
s_usb = s_t.*cos(2*pi*fc*t) + h_t.*sin(2*pi*fc*t);
s_dsb = s_lsb + s_usb;

am_fig = figure();
plot(real(s_lsb))
hold on
plot(real(s_usb))
hold on
plot(s_dsb)
legend("AM-LowerSide", "AM-UpperSide", "AM-DSB")


% am_dsb = ammod(continue_signal, fc, fs);
% am_ssb = ssbmod(continue_signal, fc, fs);
% 
% am_fig = figure();
% plot(am_dsb)
% hold on
% plot(am_ssb)
% legend("AM-DSB", "AM-SSB")


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