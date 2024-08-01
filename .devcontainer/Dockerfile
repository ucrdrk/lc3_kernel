FROM mcr.microsoft.com/devcontainers/universal:2

RUN apt update && apt install -y cmake git build-essential

# RUN python3 -m pip install .

RUN git clone https://github.com/ucrdrk/lc3tools.git /usr/lc3tools

# Run cmake and build
WORKDIR /usr/lc3tools/build
RUN cmake -DCMAKE_BUILD_TYPE=Release ..
RUN cmake -DCMAKE_BUILD_TYPE=Release ..
RUN make lc3core common simulator assembler

# Copy executables to /usr/local/bin
RUN cp /usr/lc3tools/build/bin/* /usr/local/bin

