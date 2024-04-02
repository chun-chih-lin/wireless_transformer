function [l, u, d] = generate_am(input_signal, opt)
    %   input_signal    : The input continuous signal
    %   fc              : Carrier Frequency (540 kHz- 1600 kHz)
    %   fs              : Sample Frequency

    arguments
        input_signal double
        opt.fc double = 550e3
        opt.fs double = 44.1e3
    end

    fc = opt.fc;
    fs = opt.fs;

    s_t = input_signal;
    h_t = imag(hilbert(s_t));

    t_len = length(input_signal)/fs;
    t = (0:1/fs:t_len-1/fs);

    l = s_t.*cos(2*pi*fc*t) - h_t.*sin(2*pi*fc*t);
    u = s_t.*cos(2*pi*fc*t) + h_t.*sin(2*pi*fc*t);
    d = l + u;
end