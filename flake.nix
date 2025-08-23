{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
      ...
    }:
    let
      forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;
    in
    {
      packages = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          inherit (pkgs) lib; # stdenv
          pyproject = lib.trivial.importTOML ./pyproject.toml;
        in
        {
          default = pkgs.python3Packages.buildPythonApplication {
            pname = pyproject.project.name;
            version = pyproject.project.version;
            pyproject = true;

            src = ./.;

            build-system = with pkgs.python3Packages; [ setuptools ];

            dependencies = with pkgs.python3Packages; [
              websockets
              requests
            ];

            meta = {
              # ...
            };

            buildInputs = with pkgs; [
              ffmpeg-headless
            ];
          };
        }
      );

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/mpv_discord_rpc";
        };
      });

      formatter = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.nixfmt-tree
      );
    };
}
