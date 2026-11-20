
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
    console.log("Memulai deployment Sistem Verifikasi Ijazah Akademik...");

    const ContractFactory =
        await hre.ethers.getContractFactory("SistemVerifikasiIjazah");

    // Constructor tidak membutuhkan argumen
    const contract = await ContractFactory.deploy();

    await contract.waitForDeployment();

    const contractAddress = await contract.getAddress();

    console.log("Deployment berhasil!");
    console.log("Nama Smart Contract: SistemVerifikasiIjazah");
    console.log("Alamat kontrak:", contractAddress);

    // Simpan informasi deployment ke deployment.json
    const deploymentData = {
        contractName: "SistemVerifikasiIjazah",
        address: contractAddress,
        network: "localhost",
        chainId: 31337,
    };

    const deploymentPath = path.join(
        __dirname,
        "..",
        "deployment.json"
    );

    fs.writeFileSync(
        deploymentPath,
        JSON.stringify(deploymentData, null, 2)
    );

    console.log("Informasi deployment berhasil disimpan ke deployment.json");
}

main().catch((error) => {
    console.error("Deployment gagal:", error);
    process.exitCode = 1;
});
