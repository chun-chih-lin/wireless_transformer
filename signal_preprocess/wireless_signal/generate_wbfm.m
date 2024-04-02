function y = generate_wbfm(input_signal, opt)
    % http://hyperphysics.phy-astr.gsu.edu/hbase/Audio/radio.html
    %   input_signal        : The input continuous signal
    %   fc                  : Carrier Freqiency (88.1 MHz - 108.1 MHz)
    %   fs                  : Sample Frequency
    %   fDev                : Modulation index/Frequency Deviation (Hz)

    arguments
        input_signal double
        opt.fc double = 200
        opt.fs double = 1e3
        opt.fDev double = 50
    end

    fc = opt.fc;
    fs = opt.fs;
    fDev = opt.fDev;

    y = fmmod(input_signal, fc, fs, fDev);
end