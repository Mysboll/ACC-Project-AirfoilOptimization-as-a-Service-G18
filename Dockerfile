FROM fenicsproject/stable

LABEL maintainers="Sudarsan Bhargavan; Tor Berglind; Andras Leander; Linnea Gunnarsson"

WORKDIR /AirFoil
COPY ./murtazo.tgz /AirFoil/murtazo.tgz
RUN apt-get -y update
RUN apt-get -y upgrade
RUN tar xvzf /AirFoil/murtazo.tgz
RUN tar xvzf /AirFoil/murtazo/cloudnaca.tgz
RUN tar xvf /AirFoil/murtazo/navier_stokes_solver.tar
WORKDIR /AirFoil/navier_stokes_solver/src
RUN ./compile_forms
WORKDIR /AirFoil/navier_stokes_solver
RUN cmake .
RUN make -j 2

WORKDIR /AirFoil/cloudnaca
RUN apt-get -y install gmsh python-numpy
RUN sed -i 's|GMSHBIN="/Applications/Gmsh.app/Contents/MacOS/gmsh"|GMSHBIN="/usr/bin/gmsh"|g' ./runme.sh

ENV TERM xterm

CMD ["/bin/sh"]
