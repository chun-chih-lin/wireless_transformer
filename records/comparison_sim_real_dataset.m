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
% simu_mod_list = ["AM-DSB", "AM-SSB", "WBFM", "QAM16"];
simu_mod_list = ["WBFM", "AM-DSB", "QAM16"];
simu_snr_list = (-20:2:18);

real_mod_list = ["PAM4", "BPSK", "QPSK", "8PSK", "QAM16", "QAM64", "CPFSK", "GFSK", "AM-SSB", "AM-DSB", "WBFM"];
real_mod_list = ["AM-DSB", "AM-SSB", "WBFM"];

line_width = 1.5;
lgd_font_size = 10;
lbl_font_size = 11;
s_curve_position = [100, 100, 700, 110];
r_curve_position = [100, 500, 700, 110];

color_line = ["#0072BD", "#77AC30"];
color_face = color_line;
% color_line = ["#111111", "#EE0000"];

save_fig = 1;
set(0,'DefaultFigureVisible','on')
if save_fig
    set(0,'DefaultFigureVisible','off')
end

for mod_i = 1:length(simu_mod_list)
for snr = [0]
    mod = simu_mod_list(mod_i)
    [s_data, r_data] = get_data(mod, snr);

    s_title = strcat("Simulated.", mod, ".snr", num2str(snr));
    r_title = strcat("Real.", mod, ".snr", num2str(snr));


    %% Analysis the Low Frequency fading
    FaceAlpha = .1;

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
    ylim_s_v = max([max(abs(s_r_var), [], 'all'), max(abs(s_i_var), [], 'all')]);
    ylim_r_v = max([max(abs(r_r_var), [], 'all'), max(abs(r_i_var), [], 'all')]);
    
    s_lowpass_title = strcat(s_title, ".lowpass");
    r_lowpass_title = strcat(r_title, ".lowpass");
    
    s_sample_title = strcat(s_title, ".sample");
    r_sample_title = strcat(r_title, ".sample");

    % s_sample_title = strcat(s_title, ".sample.noAxis");
    % r_sample_title = strcat(r_title, ".sample.noAxis");

    s_rand_i = randi([1, size(s_data, 1)], 1, 1);

    simu_samp_fig = figure('Name', s_sample_title, 'NumberTitle', 'off');
    plot(real(s_sig(s_rand_i, :)), ...
        'Color', color_line(1), ...
        'LineWidth', line_width);
    hold on
    plot(imag(s_sig(s_rand_i, :)), ...
        'Color', color_line(2), ...
        'LineWidth', line_width);

    xlim([1, size(s_r_mean, 2)])
    set(gca, 'Xticklabel', [], 'Yticklabel', []);
    ax = gca(simu_samp_fig);
    ax.YAxis.FontSize = lbl_font_size;
    % set(get(ax, "XAxis"), 'Visible', 'off')
    % set(get(ax, "YAxis"), 'Visible', 'off')
    % legend("I", "Q", "NumColumns", 2)
    simu_samp_fig.Position = s_curve_position;

    r_rand_i = randi([1, size(r_data, 1)], 1, 1);
    real_samp_fig = figure('Name', r_sample_title, 'NumberTitle', 'off');
    plot(real(r_sig(r_rand_i, :)), ...
        'Color', color_line(1), ...
        'LineWidth', line_width);
    hold on
    plot(imag(r_sig(r_rand_i, :)), ...
        'Color', color_line(2), ...
        'LineWidth', line_width);

    xlim([1, size(r_r_mean, 2)])
    set(gca, 'Xticklabel', [], 'Yticklabel', []);
    ax = gca(real_samp_fig);
    ax.YAxis.FontSize = lbl_font_size;
    % set(get(ax, "XAxis"), 'Visible', 'off')
    % set(get(ax, "YAxis"), 'Visible', 'off')
    % legend("I", "Q", "NumColumns", 2)
    real_samp_fig.Position = r_curve_position;

    if save_fig
        save_figure(simu_samp_fig, s_sample_title)
        save_figure(real_samp_fig, r_sample_title)
    end


    %% Lowpass Result
    if 0

    ylim_v_max = max([max(s_r_mean, [], 'all'), max(s_i_mean, [], 'all'), ...
                      max(r_r_mean, [], 'all'), max(r_i_mean, [], 'all')]);
    ylim_v_min = min([min(s_r_mean, [], 'all'), min(s_i_mean, [], 'all'), ...
                      min(r_r_mean, [], 'all'), min(r_i_mean, [], 'all')]);


    lowpass_simu_fig = figure('Name', s_lowpass_title, 'NumberTitle', 'off');
    p1 = plot(s_r_mean, 'Color', color_line(1), 'LineWidth', line_width);
    hold on
    p3 = patch([1:size(s_r_mean, 2), size(s_r_mean, 2):-1:1], ...
               [s_r_mean + s_r_var, s_r_mean(end:-1:1) - s_r_var(end:-1:1)], ...
                'r', 'FaceColor', color_face(1), ...
                'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    hold on
    p2 = plot(s_i_mean, 'Color', color_line(2), 'LineWidth', line_width);
    hold on
    p4 = patch([1:size(s_r_mean, 2), size(s_r_mean, 2):-1:1], ...
               [s_i_mean + s_i_var, s_i_mean(end:-1:1) - s_i_var(end:-1:1)], ...
                'r', 'FaceColor', color_face(2), ...
                'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    xlim([1, size(s_r_mean, 2)])
    ylim([5*ylim_v_min, 5*ylim_v_max])
    ax = gca(lowpass_simu_fig);
    ax.YAxis.FontSize = lbl_font_size;
    legend([p1, p2, p3, p4], {"I-Mean.", "Q-Mean.", "I-Var.", "Q-Var."}, ...
        "NumColumns", 4, ...
        'FontSize', lgd_font_size, ...
        'Location', 'Best')

    % title(s_lowpass_title, Interpreter="none")
    set(gca, 'Xticklabel', []);
    lowpass_simu_fig.Position = s_curve_position;


    lowpass_real_fig = figure('Name', r_lowpass_title, 'NumberTitle', 'off');
    p1 = plot(r_r_mean, 'Color', color_line(1), 'LineWidth', line_width);
    hold on
    p3 = patch([1:size(r_r_mean, 2), size(r_r_mean, 2):-1:1], ...
               [r_r_mean + r_r_var, r_r_mean(end:-1:1) - r_r_var(end:-1:1)], ...
                'r', 'FaceColor', color_face(1), ...
                'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    hold on
    p2 = plot(r_i_mean, 'Color', color_line(2), 'LineWidth', line_width);
    hold on
    p4 = patch([1:size(r_r_mean, 2), size(r_r_mean, 2):-1:1], ...
               [r_i_mean + r_i_var, r_i_mean(end:-1:1) - r_i_var(end:-1:1)], ...
                'r', 'FaceColor', color_face(2), ...
                'EdgeColor', 'none', 'FaceAlpha', FaceAlpha);
    xlim([1, size(r_r_mean, 2)])
    ylim([5*ylim_v_min, 5*ylim_v_max])
    ax = gca(lowpass_real_fig);
    ax.YAxis.FontSize = lbl_font_size;
    legend([p1, p2, p3, p4], {"I-Mean.", "Q-Mean.", "I-Var.", "Q-Var."}, ...
        "NumColumns", 4, ...
        'FontSize', lgd_font_size, ...
        'Location', 'Best')

    % title(r_lowpass_title, Interpreter="none")
    set(gca, 'Xticklabel', []);
    lowpass_real_fig.Position = r_curve_position;


    if save_fig
        save_figure(lowpass_simu_fig, s_lowpass_title)
        save_figure(lowpass_real_fig, r_lowpass_title)
    end
    end
    
    

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
    s_fig = figure('Name', s_title, 'NumberTitle', 'off');
    for i = 1:2
        plot(squeeze(s_data(1, i, :)), ...
            'LineWidth', line_width, ...
            'Color', color_line(i))
        hold on
    end
    xlim([1 size(s_data, 3)])
    ylim([-1, 1])
    s_fig.Position = s_curve_position;
    set(gca, 'Xticklabel', []);
    ax = gca(s_fig);
    ax.YAxis.FontSize = lbl_font_size;
    % title(s_title, Interpreter="none")

    r_fig = figure('Name', r_title, 'NumberTitle', 'off');
    for i = 1:2
        plot(squeeze(r_data(1, i, :)), ...
            'LineWidth', line_width, ...
            'Color', color_line(i))
        hold on
    end
    xlim([1 size(r_data, 3)])
    ylim([-1, 1])
    r_fig.Position = r_curve_position;
    set(gca, 'Xticklabel', []);
    ax = gca(r_fig);
    ax.YAxis.FontSize = lbl_font_size;
    % title(r_title, Interpreter="none")
    
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

















































