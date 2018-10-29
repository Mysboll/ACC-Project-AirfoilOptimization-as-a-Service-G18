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
RUN ./runme.sh 0 30 10 200 3
WORKDIR /AirFoil/cloudnaca/msh
RUN dolfin-convert r2a15n200.msh r2a15n200.xml

ENV TERM xterm

WORKDIR /AirFoil/navier_stokes_solver

CMD ["/bin/sh"]

# RUN THE FOLLOWING INSIDE THE CONTAINER AFTER IT STARTS 
#
# sudo ./airfoil 10 0.0001 10. 1 /AirFoil/cloudnaca/msh/r2a15n200.xml
