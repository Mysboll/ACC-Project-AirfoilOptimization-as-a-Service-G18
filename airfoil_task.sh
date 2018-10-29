#!/bin/bash

angle="$1"
n_nodes="$2"
n_levels="$3"
num_samples="$4"
viscosity="$5"
velocity="$4"
duration="$7"

docker exec -it airfoil murtazo/cloudnaca/runme.sh $angle $angle 1 $n_nodes $n_levels

docker exec -it airfoil dolfin-convert murtazo/cloudnaca/msh/r${n_levels}a${angle}n${n_nodes}.msh murtazo/cloudnaca/msh/r${levels}a${angle}n${n_nodes}.xml

docker exec -it airfoil murtazo/navier_stokes_solver/airfoil ${num_samples} ${viscosity} ${velocity} ${duration}. murtazo/cloudnaca/msh/r${levels}a${angle}n${n_nodes}.xml