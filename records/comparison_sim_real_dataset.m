clc
clear
close all
%%
% This script is used for section "MOTIVATION AND ASSUMPTIONS"
% Compare the defect with the old RML2016.10a dataset with the real over
% the air dataset we have.


% Doesn't make sense list:
% 0, 2, 4, 6, 8, 10. 12. 14, 16, 18

global result_folder_name

result_folder_name = "./results/";

simu_mod_list = ["PAM4", "BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "CPFSK", "GFSK", "AM-SSB", "AM-DSB", "WBFM"];
simu_mod_list = ["PAM4", "QAM64", "AM-SSB"];
simu_snr_list = (-20:2:18);

real_mod_list = ["PAM4", "BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "CPFSK", "GFSK", "AM-SSB", "AM-DSB", "WBFM"];
real_mod_list = ["PAM4", "QAM64", "AM-SSB"];

line_width = 1;
s_curve_position = [100, 100, 500, 150];
r_curve_position = [100, 500, 500, 150];

color_line = ["#0000FF", "#FF0000"];

save_fig = 0;
set(0,'DefaultFigureVisible','on')
if save_fig
    set(0,'DefaultFigureVisible','off')
end

for snr = [2]
for mod_i = 1:length(simu_mod_list)
    mod = simu_mod_list(mod_i)
    [s_data, r_data] = get_data(mod, snr);

    s_title = strcat("Simulated.", mod, ".snr", num2str(snr));
    r_title = strcat("Real.", mod, ".snr", num2str(snr));


    %% Analysis the Low Frequency fading
    
    color_face = ['b', 'r'];
    FaceAlpha = .1;

    s_rand_i = randi([1, size(s_data, 1)], 1, 1);
    r_rand_i = randi([1, size(r_data, 1)], 1, 1);

    s_lp_matrix = zeros(size(s_data, 1), size(s_data, 3));
    r_lp_matrix = zeros(size(r_data, 1), size(r_data, 3));

    lp_fpass = 1e2;
    fs = 200e3;

    s_sig = squeeze(s_data(:, 1, :)) + 1j*squeeze(s_data(:, 2, :));
    max_s_sig = max(max(abs(real(s_sig)), [], 'all'), max(abs(imag(s_sig)), [], 'all'));    
    s_sig = s_sig/max_s_sig;


    lp_s_sig = lowpass(s_sig.', lp_fpass, fs, "ImpulseResponse", "fir");
    s_r_mean = mean(real(lp_s_sig.'));
    s_r_var = var(real(lp_s_sig.'));
    s_i_mean = mean(imag(lp_s_sig.'));
    s_i_var = var(imag(lp_s_sig.'));

    
    fs = 400e3;
    r_sig = squeeze(r_data(:, 1, 5:260)) + 1j*squeeze(r_data(:, 2, 5:260));
    max_r_sig = max(max(abs(real(r_sig)), [], 'all'), max(abs(imag(r_sig)), [], 'all'));
    r_sig = r_sig/max_r_sig;

    lp_r_sig = lowpass(r_sig.', lp_fpass, fs, "ImpulseResponse", "fir");
    r_r_mean = mean(real(lp_r_sig.'));
    r_r_var = var(real(lp_r_sig.'));
    r_i_mean = mean(imag(lp_r_sig.'));
    r_i_var = var(imag(lp_r_sig.'));

    ylim_v = max([max(abs(s_r_mean), [], 'all'), max(abs(s_i_mean), [], 'all'), ...
                  max(abs(r_r_mean), [], 'all'), max(abs(r_i_mean), [], 'all')]);
    
    s_lowpass_title = strcat(s_title, ".lowpass");
    r_lowpass_title = strcat(r_title, ".lowpass");
    
    s_sample_title = strcat(s_title, ".sample");
    r_sample_title = strcat(r_title, ".sample");

    s_rand_i = randi([1, size(s_data, 1)], 1, 1);
    simu_samp_fig = figure();
    plot(real(s_sig(s_rand_i, :)), 'Color', color_line(1));
    hold on
    plot(imag(s_sig(s_rand_i, :)), 'Color', color_line(2));
    xlim([1, size(s_r_mean, 2)])
    set(gca, 'Xticklabel', []);
    legend("I", "Q", "NumColumns", 2)
    simu_samp_fig.Position = s_curve_position;

    r_rand_i = randi([1, size(r_data, 1)], 1, 1);
    real_samp_fig = figure();
    plot(real(r_sig(r_rand_i, :)), 'Color', color_line(1));
    hold on
    plot(imag(r_sig(r_rand_i, :)), 'Color', color_line(2));
    xlim([1, size(r_r_mean, 2)])
    set(gca, 'Xticklabel', []);
    legend("I", "Q", "NumColumns", 2)
    real_samp_fig.Position = r_curve_position;

    % save_figure(simu_samp_fig, s_sample_title)
    % save_figure(real_samp_fig, r_sample_title)

    if 1
        continue
    end

    lowpass_simu_fig = figure();
    p1 = plot(s_r_mean, 'Color', color_line(1));
    hold on
    p3 = patch([1:size(s_r_mean, 2), size(s_r_mean, 2):-1:1], [s_r_mean + s_r_var, s_r_mean(end:-1:1) - s_r_var(end:-1:1)], ...
        color_face(1), 'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    hold on
    p2 = plot(s_i_mean, 'Color', color_line(2));
    hold on
    p4 = patch([1:size(s_r_mean, 2), size(s_r_mean, 2):-1:1], [s_i_mean + s_i_var, s_i_mean(end:-1:1) - s_i_var(end:-1:1)], ...
        color_face(2), 'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    xlim([1, size(s_r_mean, 2)])
    ylim([-5*ylim_v, 5*ylim_v])
    legend([p1, p2, p3, p4], {"I-Avg.", "Q-Avg.", "I-Var.", "Q-Var."}, "NumColumns", 2)

    % title(s_lowpass_title, Interpreter="none")
    set(gca, 'Xticklabel', []);
    lowpass_simu_fig.Position = s_curve_position;


    lowpass_real_fig = figure();
    p1 = plot(r_r_mean, 'Color', color_line(1));
    hold on
    p3 = patch([1:size(r_r_mean, 2), size(r_r_mean, 2):-1:1], [r_r_mean + r_r_var, r_r_mean(end:-1:1) - r_r_var(end:-1:1)], ...
        color_face(1), 'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    hold on
    p2 = plot(r_i_mean, 'Color', color_line(2));
    hold on
    p4 = patch([1:size(r_r_mean, 2), size(r_r_mean, 2):-1:1], [r_i_mean + r_i_var, r_i_mean(end:-1:1) - r_i_var(end:-1:1)], ...
        color_face(2), 'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    xlim([1, size(r_r_mean, 2)])
    ylim([-5*ylim_v, 5*ylim_v])
    legend([p1, p2, p3, p4], {"I-Avg.", "Q-Avg.", "I-Var.", "Q-Var."}, "NumColumns", 2)

    % title(r_lowpass_title, Interpreter="none")
    set(gca, 'Xticklabel', []);
    lowpass_real_fig.Position = r_curve_position;
    
    % save_figure(lowpass_simu_fig, s_lowpass_title)
    % save_figure(lowpass_real_fig, r_lowpass_title)

    %% Plot Together
    % t_fig = figure();
    % rand_num = 5;
    % subplot(2, 1, 1)
    % rand_i_list = randi([1, size(s_data, 1)], 1, rand_num);
    % for k = 1:rand_num
    %     rand_i = rand_i_list(k);
    %     for i = 1:2
    %         plot(squeeze(s_data(rand_i, i, :)), ...
    %             'LineWidth', line_width)
    %         hold on
    %     end
    % end
    % xlim([1 size(s_data, 3)])
    % ylim([-0.02, 0.02])
    % set(gca, 'Xticklabel', [], 'YTickLabel', []);
    % title(s_title, Interpreter="none")
    % 
    % subplot(2, 1, 2)
    % rand_i_list = randi([1, size(r_data, 1)], 1, rand_num);
    % for k = 1:rand_num
    %     rand_i = rand_i_list(k);
    %     for i = 1:2
    %         plot(squeeze(r_data(rand_i, i, :)), ...
    %             'LineWidth', line_width)
    %         hold on
    %     end
    % end
    % xlim([1 size(r_data, 3)])
    % ylim([-1, 1])
    % r_fig.Position = r_curve_position;
    % title(r_title, Interpreter="none")
    % t_fig.Position = [100, 100, 1200, 600];
    
    if 1
        continue
    end

    %% Plot Separated
    s_fig = figure();
    for i = 1:2
        plot(squeeze(s_data(1, i, :)), ...
            'LineWidth', line_width, ...
            'Color', color_line(i))
        hold on
    end
    xlim([1 size(s_data, 3)])
    ylim([-0.02, 0.02])
    s_fig.Position = s_curve_position;
    set(gca, 'Xticklabel', [], 'YTickLabel', []);
    title(s_title, Interpreter="none")

    r_fig = figure();
    for i = 1:2
        plot(squeeze(r_data(1, i, :)), ...
            'LineWidth', line_width, ...
            'Color', color_line(i))
        hold on
    end
    xlim([1 size(r_data, 3)])
    ylim([-1, 1])
    r_fig.Position = r_curve_position;
    set(gca, 'Xticklabel', [], 'YTickLabel', []);
    title(r_title, Interpreter="none")
    
    if save_fig
        save_figure(s_fig, s_title)
        save_figure(r_fig, r_title)
    end
    % break
end
end


%% Function
function [s_data, r_data] = get_data(mod, snr)
    simu_folder = "./RML2016.10a/";
    real_folder = "./RML2016.10a.Real/";

    s_fn = get_simu_filename(mod, snr);
    r_fn = get_real_filename(mod);

    s_data = load(strcat(simu_folder, s_fn)).data;
    r_data = load(strcat(real_folder, r_fn)).data;
end

function f_n = get_simu_filename(mod, snr)
    f_n = strcat(mod, '.', num2str(snr), '.mat');
end

function f_n = get_real_filename(mod)
    f_n = strcat('Trimmed.', mod, '.mat');
end

function save_figure(fig, figname)
    global result_folder_name
    save_fig_name_png = strcat(result_folder_name, figname, '.png')
    save_fig_name_pdf = strcat(result_folder_name, figname, '.pdf')

    saveas(fig, save_fig_name_png)
    exportgraphics(fig, save_fig_name_pdf)
end

















































