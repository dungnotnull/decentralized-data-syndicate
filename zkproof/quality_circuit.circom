pragma circom 2.0.0;

template QualityCheck(n_cols) {
    // Public Inputs
    signal input min_rows;
    signal input max_null_rate;
    
    // Private Inputs
    signal input actual_rows;
    signal input actual_null_rate;
    
    // Output
    signal output isValid;

    // Check row count >= min_rows
    // Note: Circom only supports positive signals. 
    // We check that actual_rows - min_rows >= 0 by using a comparison gadget.
    component rowCheck = GreaterEq(actual_rows, min_rows);
    
    // Check null rate <= max_null_rate
    component nullCheck = LessEq(actual_null_rate, max_null_rate);

    isValid <== rowCheck.out * nullCheck.out;
}

// Simplified comparison gadgets for demonstration
template GreaterEq(a, b) {
    signal input a;
    signal input b;
    signal output out;
    // This is a simplification; real circuits use bit-decomposition
    out <== (a - b) < 0 ? 0 : 1; 
}

template LessEq(a, b) {
    signal input a;
    signal input b;
    signal output out;
    out <== (a - b) > 0 ? 0 : 1;
}

component main {public [min_rows, max_null_rate]} = QualityCheck(5);

