clc
clear
close all
%%
global root_folder_name dataset_folder

root_folder_name = "./wireless_data/";
dataset_folder = strcat("Dataset_", "2024_03_22_22_42_36", "/");

json_info = read_patch_info(strcat(root_folder_name, dataset_folder));
json_fieldnames = fieldnames(json_info);
for item_i = 1:numel(json_fieldnames)
    data_prefix = json_fieldnames{item_i};
    dataset = load_dataset(json_info, data_prefix);
    size(dataset)

    figure()
    plot(squeeze(dataset(1, 1, :)))
    hold on
    plot(squeeze(dataset(2, 1, :)))
    hold on
    plot(squeeze(dataset(3, 1, :)))
    hold on
    plot(squeeze(dataset(4, 1, :)))
    hold on
    plot(squeeze(dataset(5, 1, :)))



    break
end

%%
function dataset = load_dataset(json_info, data_prefix)
    global root_folder_name dataset_folder
    json_fieldname = getfield(json_info, data_prefix);
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


