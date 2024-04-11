clc
clear
close all
%%

Nsym = 6;           % Filter span in symbol durations
beta = 0.5;         % Roll-off factor
sampsPerSym = 8;    % Upsampling factor

rctFilt = comm.RaisedCosineTransmitFilter(...
  Shape='Normal', ...
  RolloffFactor=beta, ...
  FilterSpanInSymbols=Nsym, ...
  OutputSamplesPerSymbol=sampsPerSym);

mod_name = "BPSK.0";
rx_signal = load_mat(mod_name);

filter_signal = rctFilt(rx_signal(1, :));


figure();
plot(real(rx_signal(1, :)))
hold on
plot(real(filter_signal(1, :)))

%% Function
function y = load_mat(mod_name)
    global data_prefix folder_name
    mat_filename = strcat(data_prefix, ".", mod_name, ".dat.mat");
    full_filename = strcat(folder_name, mat_filename);

    l = load(full_filename);
    if isfield(l, 'data')
        y = l.data;
    else
        y = l.legitimate_packet;
    end
end
