clc
clear
close 

%%

for e = 0:7
    filename = strcat("Simulated_signal_", num2str(e), ".mat")
    load(filename)
end