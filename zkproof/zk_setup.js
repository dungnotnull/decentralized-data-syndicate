const snarkjs = require("snarkjs");
const fs = require("fs");

async function run() {
    const ptauName = "pot12_final.ptau";
    if (!fs.existsSync(ptauName)) {
        console.log("pot12_final.ptau not found. Run: npx snarkjs powersoftau new bn128 12 pot12_0000.ptau && npx snarkjs powersoftau prepare phase2 pot12_0000.ptau pot12_final.ptau");
        process.exit(1);
    }

    console.log("Generating zkey...");
    await snarkjs.zKey.newZKey("build/minproof.r1cs", ptauName, "build/minproof_0000.zkey");

    const vKey = await snarkjs.zKey.exportVerificationKey("build/minproof_0000.zkey");
    fs.writeFileSync("build/verification_key.json", JSON.stringify(vKey, null, 2));

    const input = { a: 15 };
    const { proof, publicSignals } = await snarkjs.groth16.fullProve(
        input,
        "build/minproof_js/minproof.wasm",
        "build/minproof_0000.zkey"
    );

    console.log("Proof generated:");
    console.log(JSON.stringify(proof, null, 2));
    console.log("Public signals:", publicSignals);

    const verified = await snarkjs.groth16.verify(vKey, publicSignals, proof);
    console.log("Verification result:", verified ? "VALID" : "INVALID");
}

run().catch(e => { console.error(e); process.exit(1); });
