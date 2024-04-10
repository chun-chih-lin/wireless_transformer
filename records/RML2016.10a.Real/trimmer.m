clc
clear
close all
%%
mod_list = ["PAM4", "QAM64", "BPSK", "QPSK", "8PSK", "QAM16", ...
            "AM-DSB", "AM-SSB", "CPFSK", "GFSK", "WBFM"];

packet_len = 128*2;

win_size = 3;
energy_threshold = 0.02;
len_tor = 10;

for mod_name = mod_list
    filename = strcat(mod_name, ".dat.mat")

    loaddata = load(filename).data;
    % data = data(22.59e4:22.67e4);

    [e_ret, t_ret, pkt_ret] = windowed_energy(loaddata, win_size, energy_threshold);

    packets = [];
    c = 0;
    % size(pkt_ret)

    % figure();
    % subplot(2, 1, 1)
    % plot(real(loaddata))
    % hold on
    % plot(imag(loaddata))
    % hold on
    % xlim([1, length(loaddata)])
    % 
    % subplot(2, 1, 2)
    % plot(e_ret)
    % hold on
    % yline(energy_threshold, 'r')
    % xlim([1, length(loaddata)])


    % figure();
    for p_i = 1:size(pkt_ret, 1)
        s = pkt_ret(p_i, 1);
        e = pkt_ret(p_i, 2);
        len = e-s+1;
        [len_check, pad_len] = check_len(len, packet_len+len_tor);
        if len_check
            c = c + 1;

            packet = [loaddata(s:e), zeros(1, pad_len)];

            % plot(real(packet))

            packet_r = reshape(real(packet), 1, 1, packet_len+len_tor);
            packet_i = reshape(imag(packet), 1, 1, packet_len+len_tor);
            packet = cat(2, packet_r, packet_i);
            if isempty(packets)
                packets = packet;
            else
                packets = cat(1, packets, packet);
            end
        end
    end
    
    data = packets;
    save_pkl_name = strcat("Trimmed.", mod_name, '.mat');
    save(save_pkl_name, 'data');
    % break
end


%% Function
function [ret, pad_len] = check_len(len, packet_len)
    ret = 1;
    pad_len = 0;
    if len < 255
        ret = 0;
    elseif len >= packet_len
        ret = 0;
    end
    pad_len = packet_len - len;
end

function [y, t, packets] = windowed_energy(samples, win_size, threshold)
    samples_len = length(samples);
    y = zeros(1, samples_len - win_size + 1);

    energy_index = -1;

    least_dis_from_start_to_end = 30;

    packets = [];

    pkt_start = -1;
    pkt_end = -1;

    for i = 1:samples_len - win_size + 1
        e =sum(abs(samples(i:i + win_size - 1).^2));
        
        if e > threshold
            distance = i - energy_index;
            % disp(strcat(num2str(e), ' > ', num2str(threshold)))

            if pkt_start == -1 && distance > 5
                pkt_start = i;
                % disp(strcat("!!!!!!!!!!!!! Packet start: ", num2str(i)))
            else
                % disp(strcat(num2str(i), " Enough Energy but distance is too short: ", num2str(distance)))
            end
            
            energy_index = i;
        elseif pkt_start ~= -1 && i - energy_index > least_dis_from_start_to_end
            % disp(strcat("################### Packet Ends: ", num2str(i), " Length: ", num2str(i-pkt_start)))
            pkt_end = energy_index;
        end

        if pkt_start ~= -1 && pkt_end ~= -1
            packets = cat(1, packets, [pkt_start, pkt_end]);
            pkt_start = -1;
            pkt_end = -1;
            % disp(strcat(num2str(i), "Reset packet detections, pkt_start: ", num2str(pkt_start), " pkt_end: ", num2str(pkt_end)))
        end
        y(i) = e;
    end
    t = find(y > threshold);
    t(end) = t(end) + 1;
end