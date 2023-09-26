# Python 3 in Podman with requirements.txt

Started from https://github.com/GoogleContainerTools/distroless/tree/main/examples/python3-requirements.

This is a Python 3 application that specifies third-party dependencies using requirements.txt. The
psutil module it uses is a C module that must be compiled. This is the most annoying kind of
dependency, since you need to build it in an environment where the C library and Python version
match where it will run.

It builds the final container in three stages:

1. `build`: Set up a Debian build environment that can compile Python C modules.
2. `build-venv`: Create a virtualenv using `requirements.txt`.
3. Output: Copy the venv and the code and build the final image.

The first step is only re-executed if you edit `Dockerfile`. The second step is only re-executed
if you change requirements.txt. The final step is very fast and will change on every code edit.


## Build and run

1. Build the image: `podman build . --tag=evolver`
2. Run it! `podman run --rm evolver`

