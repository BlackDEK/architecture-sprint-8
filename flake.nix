{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flakeUtils.url = "github:numtide/flake-utils";
  };
  outputs =
    { self
    , nixpkgs
    , flakeUtils
    }:
    flakeUtils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        overlays = [
        ];
      };

      shellInput = with pkgs; [
        # nix
        nixpkgs-fmt
        nil
        statix
        deadnix

        # pyhton
        (python311.withPackages (ps: with ps; [
          autopep8
          flask
          flask-cors
          python-keycloak
          gunicorn
        ]))
      ];

      shell = pkgs.mkShell rec {
        packages = shellInput;
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath packages;

        shellHook = ''
        '';
      };
    in
    {
      devShells.default = shell;
    }
    );
}
