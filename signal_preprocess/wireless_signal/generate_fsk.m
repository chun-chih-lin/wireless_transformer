function y = generate_fsk(opt)
    %   fs          : Sample Frequency
    %   sps         : Sample per symbol
    %   mod         : Modulation order
    %   freqsep     : Frequency Separation (Hz)

    arguments
        opt.fs double = 32
        opt.sps double = 8
        opt.mod double = 4
        opt.freqsep double = 8
        opt.data_length double = 10
    end

    fs = opt.fs;
    sps = opt.sps;
    mod = opt.mod;
    freqsep = opt.freqsep;
    data_length = opt.data_length;

    input_symbol = randi([0, mod-1], data_length, 1);
    y = fskmod(input_symbol, mod, freqsep, sps, fs);
end