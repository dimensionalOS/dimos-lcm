{
  description = "dimOS LCM message types and code generation";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    lcm.url = "github:dimensionalOS/lcm";
  };

  outputs = { self, nixpkgs, flake-utils, lcm }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lcmgen = lcm.packages.${system}.lcmgen;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            lcmgen
            pkgs.python3
          ];
        };
      });
}
