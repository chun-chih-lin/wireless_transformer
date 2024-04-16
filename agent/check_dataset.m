clc
clear
close all
%%
global root_folder_name dataset_folder

set(0,'DefaultFigureVisible','on')

root_folder_name = "./wireless_data/";
dataset_folder = strcat("Dataset_", "2024_03_26_19_49_37", "/");
dataset_folder = strcat("Dataset_", "2024_03_26_20_18_56", "/");

cfg = wlanHTConfig('ChannelBandwidth', 'CBW20');
% HTLTF = wlanHTLTF(cfg);
HTSTF = wlanHTSTF(cfg);

% 
len_tbl = [1521, 1201, 961, 801, 721, 641, 561, 561];   % 38
len_tbl = [1280, 880, 880, 720, 640, 560, 560, 560];

json_info = read_patch_info(strcat(root_folder_name, dataset_folder));
json_fieldnames = fieldnames(json_info);

packet_length_minimum = 500;

for item_i = 1:numel(json_fieldnames)
    data_prefix = json_fieldnames{item_i};
    if data_prefix == "Description"
        continue
    end
    
    filename_seg = split(json_info.(data_prefix).Filename, '.');
    filename_cell = join(filename_seg(1:end-1), '.');
    mcs = json_info.(data_prefix).MCS;

    packet_length_minimum = len_tbl(mcs+1)-5;
    dataset = load_dataset(json_info, data_prefix);

    legitimate_packet = [];

    % for record_i = 1:size(dataset, 1)
    for record_i = 1:10
        sub_data = squeeze(dataset(record_i, :, :));
        complex_data = sub_data(1, :) + 1j*sub_data(2, :);
    
        %% Detecting the packets
        win_size = 2;
        energy_threshold = 0.01;
        [e_ret, t_ret, pkt_ret] = windowed_energy(complex_data, win_size, energy_threshold);
    
        fig = figure();
        subplot(3, 1, 1)
        plot(real(complex_data))
        hold on
        plot(imag(complex_data))
        
        for p_i = 1:size(pkt_ret, 1)
            packet_start = pkt_ret(p_i, 1);
            packet_end = pkt_ret(p_i, 2);

            xline(packet_start, 'r')
            hold on
            xline(packet_end, 'r')
            hold on
    
            pkt_len = pkt_ret(p_i, 2) - pkt_ret(p_i, 1);
            if pkt_len > packet_length_minimum
                legitimate_packet = cat(1, legitimate_packet, complex_data(packet_start:packet_start+len_tbl(mcs+1)));
            end
        end
    
        title("Overall")

        subplot(3, 1, 2)
        plot(real(complex_data))
        hold on
        plot(imag(complex_data))
        hold on
        if length(t_ret) >= 2
            xline(t_ret(1), 'r')
            hold on
            xline(t_ret(end), 'r')
            hold on
        end
        xlim([0, t_ret(1) + 100])

        subplot(3, 1, 3)
        plot(real(complex_data))
        hold on
        plot(imag(complex_data))
        hold on
        if length(t_ret) >= 2
            xline(t_ret(1), 'r')
            hold on
            xline(t_ret(end), 'r')
            hold on
        end
        xlim([t_ret(end) - 100, t_ret(end) + 100])
        fig.Position = [100, 100, 1400, 500];
        break
    end

    % figure();
    % for i = 1:size(legitimate_packet, 1)
    %     plot(real(legitimate_packet(i, :)))
    %     hold on
    % end
    
    size(legitimate_packet)
    
    % filename = strcat("Trimmed.", filename_cell{1}, ".mat");
    % full_filename = strcat(root_folder_name, dataset_folder, filename);
    % save(full_filename, 'legitimate_packet');
    % break
end

%% Functions
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

function y = correlation_to_STF(samples)
    cfg = wlanHTConfig('ChannelBandwidth', 'CBW20');
    % HTLTF = wlanHTLTF(cfg);
    HTSTF = wlanHTSTF(cfg);

    if size(HTSTF, 1) ~= 1
        HTSTF = HTSTF.';
    end
    HTSTF = [HTSTF, HTSTF];

    HTSTF_len = length(HTSTF);
    samples_len = length(samples);

    y = zeros(1, samples_len + HTSTF_len - 1);

    for i = 1:samples_len - HTSTF_len
        s = i;
        e = s + HTSTF_len - 1;
        y(i) = sum(samples(s:e).*HTSTF);
    end

    y = y / max(abs(y));
end

% ===================================

function dataset = load_dataset(json_info, data_prefix)
    global root_folder_name dataset_folder
    json_fieldname = json_info.(data_prefix);
    pkl_filename = json_fieldname.Filename;
    pkl_filename_seg = split(pkl_filename, ".");
    mat_filename = strcat(join(pkl_filename_seg(1:3), "."), ".mat");
    mat_filename_full_name = strcat(root_folder_name, dataset_folder, mat_filename);
    dataset = load(mat_filename_full_name).data;
end

function json_info = read_patch_info(folder_name)
    % fid = fileread(strcat(folder_name, "patch_info.json"));
    % raw = fread(fid, inf);
    str = fileread(strcat(folder_name, "patch_info.json"));
    % fclose(fid);
    json_info = jsondecode(str);
end



















































