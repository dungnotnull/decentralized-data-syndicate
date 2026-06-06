template Main() {
    signal input a;
    signal output b;
    signal diff;
    diff <-- a - 10;
    diff === a - 10;
    b <== diff;
}

component main = Main();
