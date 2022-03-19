{ pkgs ? import <nixpkgs> {} }:
let
  mypy = pkgs.python3;
  python-with-packages = mypy.withPackages (p: with p; [
    requests
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-with-packages
  ];
  shellHook = ''
    PYTHONPATH=${python-with-packages}/${python-with-packages.sitePackages}
  '';
}
