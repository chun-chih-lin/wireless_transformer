function y = generate_cpfsk(opt)
    %   spf     : Symbol per frame
    %   mod     : Modulation order

    arguments
        opt.spf double = 115
        opt.mod double = 8
    end
    spf = opt.spf;
    mod = opt.mod;

    cpfskMod = comm.CPFSKModulator(mod, "BitInput", true, "SymbolMapping", "Gray");
    bits = randi([0, 1], log2(mod)*spf, 1);
    y = cpfskMod(bits);
end