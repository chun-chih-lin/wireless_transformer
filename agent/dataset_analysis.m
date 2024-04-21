clc
clear
close all
%%
set(0,'DefaultFigureVisible','on')

root_folder_name = "./wireless_data/";
dataset_folder = strcat("Dataset_", "2024_03_26_19_49_37", "/");
% dataset_folder = strcat("Dataset_", "2024_03_26_20_18_56", "/");

json_info = read_patch_info(strcat(root_folder_name, dataset_folder));
json_fieldnames = fieldnames(json_info);

for item_i = 1:numel(json_fieldnames)
    data_prefix = json_fieldnames{item_i};
    if data_prefix == "Description"
        continue
    end

    filename_seg = split(json_info.(data_prefix).Filename, '.');
    filename_cell = join(filename_seg(1:end-1), '.');
    
    mat_filename_full_name = strcat(root_folder_name, dataset_folder, "Trimmed.", filename_cell{1}, ".mat");
    dataset = load_from_mat(mat_filename_full_name);
    
    step_size = 2;
    steps = 0:step_size:0;
    start_sample = 400;

    color_steps = jet(length(steps));

    for sample_i = 1:size(dataset, 1)

        complex_data = dataset(sample_i, :);

        % figure();
        % plot(real(complex_data(1:128)))
        % hold on
        % plot(imag(complex_data(1:128)))
        % break


        % fig = figure();
        % subplot(2, 2, [2, 4])
        % for step_i = 1:length(steps)
        %     step = steps(step_i);
        % 
        %     d_len = 64;
        %     s = start_sample + step;
        %     e = s + d_len - 1;
        % 
        %     dft_ret = apply_dft(complex_data(s:e));
        %     plot(real(dft_ret), imag(dft_ret), "o", 'Color', color_steps(step_i, :))
        %     hold on
        % end
        % axis square
        % 
        % subplot(2, 2, 1)
        % plot(abs(dft_ret))
        % xlim([1, 64])
        % 
        % subplot(2, 2, 3)
        % plot(real(complex_data(4:67)))
        % hold on
        % plot(imag(complex_data(4:67)))
        % 
        % sgtitle(json_info.(data_prefix).MCS)
        


        %% 
        method_index = 5;
        [apply_ret, r] = apply_autocorr(complex_data(4:67), 63, method_index);
        show_autocorr(r, json_info.(data_prefix).MCS);
        
        break
    end
    % break
end





%% Function
function fig = show_autocorr(r, title_name)
    fig = figure();
    subplot(2, 2, 1)
    surf(real(r), 'EdgeColor', 'none')
    axis square
    title("Real")
    colorbar
    view(2)

    subplot(2, 2, 2)
    surf(imag(r), 'EdgeColor', 'none')
    axis square
    title("Imag")
    colorbar
    view(2)
    
    subplot(2, 2, 3)
    surf(abs(r), 'EdgeColor', 'none')
    axis square
    title("Absolute")
    colorbar
    view(2)

    subplot(2, 2, 4)
    surf(angle(r), 'EdgeColor', 'none')
    axis square
    title("Phase")
    colorbar
    view(2)

    fig.Position = [100, 200, 800, 600];
    sgtitle(title_name, Interpreter="none")
end

function [y, r, method_name] = apply_autocorr(samples, m, method_index)
    if method_index == 1
        method_name = "autocorrelation";
    elseif method_index == 2
        method_name = "prewindowed";
    elseif method_index == 3
        method_name = "postwindowed";
    elseif method_index == 4
        method_name = "covariance";
    else
        method_name = "modified";
    end
    [y, r] = corrmtx(samples, m, method_name);
end

function r = row_x_matrix(row_v, i_matrix)
    r = zeros(1, length(row_v));
    for i = 1:length(row_v)
        i_matrix_c = i_matrix(:, i);
        r(i) = sum(dot(row_v, i_matrix_c.', 1));
    end
end

function y = apply_dft(samples)
    dft_matrix = dftmtx(64);
    y = row_x_matrix(samples, dft_matrix);
end

function y = load_from_mat(mat_filename_full_name)
    y = load(mat_filename_full_name).legitimate_packet;
end

function json_info = read_patch_info(folder_name)
    % fid = fileread(strcat(folder_name, "patch_info.json"));
    % raw = fread(fid, inf);
    str = fileread(strcat(folder_name, "patch_info.json"));
    % fclose(fid);
    json_info = jsondecode(str);
end
