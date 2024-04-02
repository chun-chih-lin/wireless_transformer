function r = row_x_matrix(row_v, i_matrix)
    r = zeros(1, length(row_v));
    for i = 1:length(row_v)
        i_matrix_c = i_matrix(:, i);
        r(i) = sum(dot(row_v, i_matrix_c.', 1));
    end
end