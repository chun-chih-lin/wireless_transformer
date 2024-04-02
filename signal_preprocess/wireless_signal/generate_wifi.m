function y = generate_wifi(opt)
    arguments
        opt.mod double = 0
        opt.symbol_len double = 10
    end

    mod = opt.mod;
    symbol_len = opt.symbol_len;

    cfgHT = wlanHTConfig(...
        "ChannelBandwidth", "CBW20", ...
        "MCS", mod, ...
        "PSDULength", symbol_len);
    psdu = randi([0, 1], 8*symbol_len, 1);
    y = wlanWaveformGenerator(psdu, cfgHT);
end