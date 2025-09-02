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
              numpy
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

      apps = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          inherit (pkgs) lib; # stdenv
          pyproject = lib.trivial.importTOML ./pyproject.toml;
          pyprojectScripts = builtins.mapAttrs (name: value: {
            type = "app";
            program = "${self.packages.${system}.default}/bin/${name}";
          }) pyproject.project.scripts;
        in
        lib.recursiveUpdate pyprojectScripts { default = pyprojectScripts.mpv_discord_rpc; }
      );

      formatter = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.nixfmt-tree
      );
    };
}
