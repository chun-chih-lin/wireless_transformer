function y = generate_pam(opt)
    %   mod             : Modulation order
    %   data_length     : number of symbols
   
    arguments
        opt.mod double = 4
        opt.num_symbol double = 100
    end
    
    mod = opt.mod;
    num_symbol = opt.num_symbol;

    input_symbol = randi([0, mod-1], num_symbol, 1);
    y = pammod(input_symbol, mod);
end